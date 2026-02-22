from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

# Enums
class BenefitType(str, Enum):
    produce_rx = "produce_rx"
    mtg = "mtg"  # Medically Tailored Groceries
    mtm = "mtm"  # Medically Tailored Meals
    pantry = "pantry"
    snap_support = "snap_support"
    nutrition_coaching = "nutrition_coaching"
    other = "other"

class GeoScope(str, Enum):
    national = "national"
    state = "state"
    county = "county"
    city = "city"
    zip = "zip"

class ProgramStatus(str, Enum):
    active = "active"
    paused = "paused"
    deprecated = "deprecated"

class EligibilityStatus(str, Enum):
    likely_eligible = "likely_eligible"
    possibly_eligible = "possibly_eligible"
    community = "community"

# User Models
class User(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    created_at: datetime

class UserSession(BaseModel):
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime

# Geography Models
class ZipLookupRequest(BaseModel):
    zip_code: str

class ZipLookupResponse(BaseModel):
    zip_code: str
    county: str
    state: str
    state_code: str

# Program Models
class Program(BaseModel):
    program_id: str = Field(default_factory=lambda: f"prog_{uuid.uuid4().hex[:12]}")
    program_name: str
    benefit_type: BenefitType
    geo_scope: GeoScope
    state: Optional[str] = None
    county: Optional[str] = None
    zip_prefixes: Optional[List[str]] = None
    how_to_apply_url: Optional[str] = None
    contact_phone: Optional[str] = None
    source_urls: List[str] = []
    status: ProgramStatus = ProgramStatus.active
    effective_start: datetime
    effective_end: Optional[datetime] = None
    last_verified_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProgramRule(BaseModel):
    program_id: str
    eligibility_conditions_json: Dict[str, Any]
    document_checklist_json: Dict[str, Any]
    referral_required: bool = False
    requires_medicaid: bool = False
    requires_snap: bool = False
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    income_fpl_bands_allowed: List[str] = []
    diagnosis_categories_allowed: List[str] = []
    notes: Optional[str] = None

class ProgramCreate(BaseModel):
    program_name: str
    benefit_type: BenefitType
    geo_scope: GeoScope
    state: Optional[str] = None
    county: Optional[str] = None
    zip_prefixes: Optional[List[str]] = None
    how_to_apply_url: Optional[str] = None
    contact_phone: Optional[str] = None
    source_urls: List[str] = []
    eligibility_conditions_json: Dict[str, Any]
    document_checklist_json: Dict[str, Any]
    referral_required: bool = False
    requires_medicaid: bool = False
    requires_snap: bool = False
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    income_fpl_bands_allowed: List[str] = []
    diagnosis_categories_allowed: List[str] = []
    notes: Optional[str] = None

# Eligibility Models
class QuestionnaireAnswers(BaseModel):
    enrolled_medicaid: str  # Yes/No/Not sure
    enrolled_snap: str  # Yes/No/Not sure
    household_size: int  # 1-8+
    income_band: str  # Under 100% FPL, 100-138% FPL, etc.
    age_range: str  # Under 18, 18-59, 60+
    pregnancy: str  # Yes/No/Prefer not to say
    health_conditions: List[str] = []  # Diabetes, Heart disease, etc.
    has_case_manager: str  # Yes/No

class EligibilityRequest(BaseModel):
    zip_code: str
    answers: QuestionnaireAnswers

class ProgramMatch(BaseModel):
    program_id: str
    program_name: str
    benefit_type: BenefitType
    match_score: float
    eligibility_status: EligibilityStatus
    matched_conditions: List[str]
    unmet_conditions: List[str]
    why_you_match: str
    document_checklist: Dict[str, Any]
    how_to_apply_url: Optional[str]
    contact_phone: Optional[str]
    source_urls: List[str]

class EligibilityResponse(BaseModel):
    zip_code: str
    county: str
    state: str
    likely_eligible: List[ProgramMatch]
    possibly_eligible: List[ProgramMatch]
    community: List[ProgramMatch]

# User Saved Results
class UserSavedResult(BaseModel):
    id: str = Field(default_factory=lambda: f"result_{uuid.uuid4().hex[:12]}")
    user_id: str
    zip_code: str
    county: str
    state: str
    answers_json: Dict[str, Any]
    matched_program_ids: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SaveResultRequest(BaseModel):
    zip_code: str
    county: str
    state: str
    answers: QuestionnaireAnswers
    matched_program_ids: List[str]

# Auth Models
class SessionExchangeRequest(BaseModel):
    session_id: str

class SessionExchangeResponse(BaseModel):
    user: User
    session_token: str
