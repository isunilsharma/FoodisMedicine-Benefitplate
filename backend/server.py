from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timezone

# Import models and utilities
from models import (
    User, SessionExchangeRequest, SessionExchangeResponse,
    ZipLookupRequest, ZipLookupResponse,
    EligibilityRequest, EligibilityResponse,
    Program, ProgramCreate, ProgramMatch,
    SaveResultRequest, UserSavedResult
)
from auth import exchange_session_id, get_current_user, require_admin, logout_user
from geography import lookup_zip, seed_zip_data
from eligibility_engine import evaluate_eligibility
from seed_data import seed_programs
from pdf_generator import generate_checklist_pdf
from llm_explanations import generate_why_you_match_explanation
from analytics import (
    track_event, EVENT_ZIP_SUBMITTED, EVENT_QUESTIONNAIRE_STARTED,
    EVENT_QUESTIONNAIRE_COMPLETED, EVENT_PROGRAMS_SHOWN, EVENT_PROGRAM_DETAIL_CLICKED,
    EVENT_CHECKLIST_DOWNLOADED, EVENT_RESULT_SAVED, EVENT_PROGRAM_BROWSED
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="BenefitPlate API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============== STARTUP ==============
@app.on_event("startup")
async def startup_event():
    """Seed database on startup"""
    logger.info("Starting up application...")
    await seed_zip_data(db)
    await seed_programs(db)
    logger.info("Startup complete")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# ============== HEALTH CHECK ==============
@api_router.get("/")
async def root():
    return {"message": "BenefitPlate API", "version": "1.0.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy"}

# ============== AUTH ENDPOINTS ==============
@api_router.post("/auth/session", response_model=SessionExchangeResponse)
async def create_session(request: SessionExchangeRequest, response: Response):
    """Exchange session_id for session_token and user data"""
    result = await exchange_session_id(request.session_id, db)
    
    # Set httpOnly cookie
    response.set_cookie(
        key="session_token",
        value=result["session_token"],
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=7 * 24 * 60 * 60  # 7 days
    )
    
    return SessionExchangeResponse(
        user=User(**result["user"]),
        session_token=result["session_token"]
    )

@api_router.get("/auth/me", response_model=User)
async def get_current_user_endpoint(request: Request):
    """Get current authenticated user"""
    user = await get_current_user(request, db)
    return user

@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    """Logout user"""
    session_token = request.cookies.get("session_token")
    if session_token:
        await logout_user(session_token, db)
    
    # Clear cookie
    response.delete_cookie(key="session_token", path="/")
    return {"message": "Logged out successfully"}

# ============== GEOGRAPHY ENDPOINTS ==============
@api_router.post("/geography/lookup", response_model=ZipLookupResponse)
async def lookup_zip_code(request: ZipLookupRequest):
    """Lookup county and state for a ZIP code"""
    result = await lookup_zip(request.zip_code, db)
    
    if not result:
        raise HTTPException(status_code=404, detail="ZIP code not found")
    
    # Track analytics
    await track_event(db, EVENT_ZIP_SUBMITTED, metadata={"zip_code": request.zip_code})
    
    return ZipLookupResponse(**result)

# ============== ELIGIBILITY ENDPOINTS ==============
@api_router.post("/eligibility/evaluate", response_model=EligibilityResponse)
async def evaluate_eligibility_endpoint(request: EligibilityRequest):
    """Evaluate eligibility for programs based on ZIP and questionnaire"""
    # Lookup geography
    geo_result = await lookup_zip(request.zip_code, db)
    
    if not geo_result:
        raise HTTPException(status_code=404, detail="ZIP code not found")
    
    # Track analytics - questionnaire completed
    await track_event(db, EVENT_QUESTIONNAIRE_COMPLETED, metadata={
        "zip_code": request.zip_code,
        "county": geo_result["county"],
        "state": geo_result["state"]
    })
    
    # Evaluate eligibility
    results = await evaluate_eligibility(
        zip_code=request.zip_code,
        county=geo_result["county"],
        state=geo_result["state"],
        state_code=geo_result["state_code"],
        answers=request.answers,
        db=db
    )
    
    # Track programs shown
    total_programs = len(results["likely_eligible"]) + len(results["possibly_eligible"]) + len(results["community"])
    await track_event(db, EVENT_PROGRAMS_SHOWN, metadata={
        "zip_code": request.zip_code,
        "total_programs": total_programs,
        "likely_eligible": len(results["likely_eligible"]),
        "possibly_eligible": len(results["possibly_eligible"]),
        "community": len(results["community"])
    })
    
    return EligibilityResponse(
        zip_code=request.zip_code,
        county=geo_result["county"],
        state=geo_result["state"],
        likely_eligible=results["likely_eligible"],
        possibly_eligible=results["possibly_eligible"],
        community=results["community"]
    )

# ============== PROGRAM ENDPOINTS ==============
@api_router.get("/programs", response_model=List[Program])
async def list_programs(
    state: Optional[str] = None,
    county: Optional[str] = None,
    benefit_type: Optional[str] = None,
    status: str = "active"
):
    """List all programs with optional filters"""
    query = {"status": status}
    
    if state:
        query["$or"] = [
            {"geo_scope": "national"},
            {"state": state}
        ]
    
    if county:
        query["county"] = county
    
    if benefit_type:
        query["benefit_type"] = benefit_type
    
    programs = await db.programs.find(query, {"_id": 0}).to_list(1000)
    return [Program(**p) for p in programs]

@api_router.get("/programs/{program_id}", response_model=Program)
async def get_program(program_id: str):
    """Get program details"""
    program = await db.programs.find_one({"program_id": program_id}, {"_id": 0})
    
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Track analytics
    await track_event(db, EVENT_PROGRAM_DETAIL_CLICKED, metadata={"program_id": program_id})
    
    return Program(**program)

@api_router.post("/programs/{program_id}/generate-explanation")
async def generate_explanation(program_id: str, matched_conditions: List[str], unmet_conditions: List[str] = []):
    """Generate plain-English explanation for program match"""
    program = await db.programs.find_one({"program_id": program_id}, {"_id": 0})
    
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    explanation = await generate_why_you_match_explanation(
        program_name=program["program_name"],
        benefit_type=program["benefit_type"],
        matched_conditions=matched_conditions,
        unmet_conditions=unmet_conditions
    )
    
    return {"explanation": explanation}

# ============== USER ENDPOINTS (AUTHENTICATED) ==============
@api_router.post("/user/save-result", response_model=UserSavedResult)
async def save_result(request: SaveResultRequest, http_request: Request):
    """Save user's eligibility result"""
    user = await get_current_user(http_request, db)
    
    saved_result = UserSavedResult(
        user_id=user.user_id,
        zip_code=request.zip_code,
        county=request.county,
        state=request.state,
        answers_json=request.answers.model_dump(),
        matched_program_ids=request.matched_program_ids
    )
    
    result_doc = saved_result.model_dump()
    result_doc["created_at"] = result_doc["created_at"].isoformat()
    
    await db.user_saved_results.insert_one(result_doc)
    
    # Track analytics
    await track_event(db, EVENT_RESULT_SAVED, user_id=user.user_id, metadata={
        "zip_code": request.zip_code,
        "programs_count": len(request.matched_program_ids)
    })
    
    return saved_result

@api_router.get("/user/saved-results", response_model=List[UserSavedResult])
async def get_saved_results(request: Request):
    """Get user's saved results"""
    user = await get_current_user(request, db)
    
    results = await db.user_saved_results.find(
        {"user_id": user.user_id},
        {"_id": 0}
    ).sort("created_at", -1).to_list(100)
    
    # Convert ISO strings back to datetime
    for result in results:
        if isinstance(result["created_at"], str):
            result["created_at"] = datetime.fromisoformat(result["created_at"])
    
    return [UserSavedResult(**r) for r in results]

@api_router.post("/user/generate-checklist-pdf")
async def generate_pdf_checklist(
    program_ids: List[str],
    zip_code: str,
    county: str,
    state: str,
    request: Request
):
    """Generate PDF checklist for matched programs"""
    user = await get_current_user(request, db)
    
    # Fetch programs
    programs = []
    for program_id in program_ids:
        program_doc = await db.programs.find_one({"program_id": program_id}, {"_id": 0})
        rule_doc = await db.program_rules.find_one({"program_id": program_id}, {"_id": 0})
        
        if program_doc:
            # Create ProgramMatch object (simplified)
            program_match = ProgramMatch(
                program_id=program_doc["program_id"],
                program_name=program_doc["program_name"],
                benefit_type=program_doc["benefit_type"],
                match_score=1.0,
                eligibility_status="likely_eligible",
                matched_conditions=[],
                unmet_conditions=[],
                why_you_match="Based on your eligibility screening",
                document_checklist=rule_doc.get("document_checklist_json", {}) if rule_doc else {},
                how_to_apply_url=program_doc.get("how_to_apply_url"),
                contact_phone=program_doc.get("contact_phone"),
                source_urls=program_doc.get("source_urls", [])
            )
            programs.append(program_match)
    
    # Track analytics
    await track_event(db, EVENT_CHECKLIST_DOWNLOADED, user_id=user.user_id, metadata={
        "zip_code": zip_code,
        "programs_count": len(program_ids)
    })
    
    # Generate PDF
    pdf_buffer = generate_checklist_pdf(
        user_name=user.name,
        zip_code=zip_code,
        county=county,
        state=state,
        programs=programs
    )
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=benefits_checklist_{datetime.now().strftime('%Y%m%d')}.pdf"}
    )

# ============== ADMIN ENDPOINTS ==============
@api_router.get("/admin/programs", response_model=List[Program])
async def admin_list_programs(request: Request):
    """Admin: List all programs"""
    user = await get_current_user(request, db)
    await require_admin(user)
    
    programs = await db.programs.find({}, {"_id": 0}).to_list(1000)
    return [Program(**p) for p in programs]

@api_router.post("/admin/programs", response_model=Program)
async def admin_create_program(program_data: ProgramCreate, request: Request):
    """Admin: Create new program"""
    user = await get_current_user(request, db)
    await require_admin(user)
    
    # Create program
    program = Program(
        program_name=program_data.program_name,
        benefit_type=program_data.benefit_type,
        geo_scope=program_data.geo_scope,
        state=program_data.state,
        county=program_data.county,
        zip_prefixes=program_data.zip_prefixes,
        how_to_apply_url=program_data.how_to_apply_url,
        contact_phone=program_data.contact_phone,
        source_urls=program_data.source_urls,
        effective_start=datetime.now(timezone.utc),
        last_verified_at=datetime.now(timezone.utc)
    )
    
    program_doc = program.model_dump()
    program_doc["effective_start"] = program_doc["effective_start"].isoformat()
    program_doc["last_verified_at"] = program_doc["last_verified_at"].isoformat()
    program_doc["created_at"] = program_doc["created_at"].isoformat()
    program_doc["updated_at"] = program_doc["updated_at"].isoformat()
    if program_doc.get("effective_end"):
        program_doc["effective_end"] = program_doc["effective_end"].isoformat()
    
    await db.programs.insert_one(program_doc)
    
    # Create program rules
    from models import ProgramRule
    rule = ProgramRule(
        program_id=program.program_id,
        eligibility_conditions_json=program_data.eligibility_conditions_json,
        document_checklist_json=program_data.document_checklist_json,
        referral_required=program_data.referral_required,
        requires_medicaid=program_data.requires_medicaid,
        requires_snap=program_data.requires_snap,
        min_age=program_data.min_age,
        max_age=program_data.max_age,
        income_fpl_bands_allowed=program_data.income_fpl_bands_allowed,
        diagnosis_categories_allowed=program_data.diagnosis_categories_allowed,
        notes=program_data.notes
    )
    
    await db.program_rules.insert_one(rule.model_dump())
    
    return program

@api_router.put("/admin/programs/{program_id}", response_model=Program)
async def admin_update_program(program_id: str, program_data: ProgramCreate, request: Request):
    """Admin: Update program"""
    user = await get_current_user(request, db)
    await require_admin(user)
    
    # Update program
    update_data = {
        "program_name": program_data.program_name,
        "benefit_type": program_data.benefit_type,
        "geo_scope": program_data.geo_scope,
        "state": program_data.state,
        "county": program_data.county,
        "zip_prefixes": program_data.zip_prefixes,
        "how_to_apply_url": program_data.how_to_apply_url,
        "contact_phone": program_data.contact_phone,
        "source_urls": program_data.source_urls,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.programs.update_one(
        {"program_id": program_id},
        {"$set": update_data}
    )
    
    # Update rules
    rule_update = {
        "eligibility_conditions_json": program_data.eligibility_conditions_json,
        "document_checklist_json": program_data.document_checklist_json,
        "referral_required": program_data.referral_required,
        "requires_medicaid": program_data.requires_medicaid,
        "requires_snap": program_data.requires_snap,
        "min_age": program_data.min_age,
        "max_age": program_data.max_age,
        "income_fpl_bands_allowed": program_data.income_fpl_bands_allowed,
        "diagnosis_categories_allowed": program_data.diagnosis_categories_allowed,
        "notes": program_data.notes
    }
    
    await db.program_rules.update_one(
        {"program_id": program_id},
        {"$set": rule_update}
    )
    
    # Get updated program
    program = await db.programs.find_one({"program_id": program_id}, {"_id": 0})
    return Program(**program)

@api_router.delete("/admin/programs/{program_id}")
async def admin_delete_program(program_id: str, request: Request):
    """Admin: Delete program"""
    user = await get_current_user(request, db)
    await require_admin(user)
    
    await db.programs.delete_one({"program_id": program_id})
    await db.program_rules.delete_one({"program_id": program_id})
    
    return {"message": "Program deleted successfully"}

@api_router.get("/admin/programs/needs-review")
async def admin_programs_needing_review(request: Request):
    """Admin: Get programs needing review (>90 days since last verification)"""
    user = await get_current_user(request, db)
    await require_admin(user)
    
    from datetime import timedelta
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=90)
    
    programs = await db.programs.find(
        {"last_verified_at": {"$lt": cutoff_date.isoformat()}},
        {"_id": 0}
    ).to_list(1000)
    
    return [Program(**p) for p in programs]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)
