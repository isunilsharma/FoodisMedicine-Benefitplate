"""Seed updated research-backed programs into database"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Import program data
from updated_programs_data import ALL_PROGRAMS, CALIFORNIA_PROGRAMS
from updated_programs_rules import PROGRAM_RULES

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def seed_updated_programs():
    """Replace existing programs with research-backed dataset"""
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("=== Seeding Updated Programs ===\n")
    
    # Step 1: Backup existing programs (optional)
    existing_programs = await db.programs.find({}, {"_id": 0}).to_list(1000)
    existing_rules = await db.program_rules.find({}, {"_id": 0}).to_list(1000)
    print(f"Found {len(existing_programs)} existing programs")
    print(f"Found {len(existing_rules)} existing rules\n")
    
    # Step 2: Delete existing programs and rules
    delete_programs = await db.programs.delete_many({})
    delete_rules = await db.program_rules.delete_many({})
    print(f"Deleted {delete_programs.deleted_count} programs")
    print(f"Deleted {delete_rules.deleted_count} rules\n")
    
    # Step 3: Convert datetime objects to ISO strings for MongoDB
    programs_to_insert = []
    for program in ALL_PROGRAMS:
        prog_doc = program.copy()
        prog_doc["effective_start"] = prog_doc["effective_start"].isoformat()
        if prog_doc.get("effective_end"):
            prog_doc["effective_end"] = prog_doc["effective_end"].isoformat()
        prog_doc["last_verified_at"] = prog_doc["last_verified_at"].isoformat()
        prog_doc["created_at"] = prog_doc.get("created_at", prog_doc["effective_start"])
        prog_doc["updated_at"] = prog_doc.get("updated_at", prog_doc["last_verified_at"])
        programs_to_insert.append(prog_doc)
    
    # Step 4: Insert new programs
    if programs_to_insert:
        await db.programs.insert_many(programs_to_insert)
        print(f"✓ Inserted {len(programs_to_insert)} programs")
        print(f"  - California programs: {len(CALIFORNIA_PROGRAMS)}")
        print(f"  - Other state programs: {len(ALL_PROGRAMS) - len(CALIFORNIA_PROGRAMS)}\n")
    
    # Step 5: Insert program rules
    if PROGRAM_RULES:
        await db.program_rules.insert_many(PROGRAM_RULES)
        print(f"✓ Inserted {len(PROGRAM_RULES)} program rules\n")
    
    # Step 6: Create indexes
    await db.programs.create_index("program_id", unique=True)
    await db.programs.create_index("status")
    await db.programs.create_index("state")
    await db.programs.create_index("county")
    await db.program_rules.create_index("program_id", unique=True)
    print("✓ Created indexes\n")
    
    # Step 7: Verify
    total_programs = await db.programs.count_documents({})
    ca_programs = await db.programs.count_documents({"state": "California"})
    active_programs = await db.programs.count_documents({"status": "active"})
    paused_programs = await db.programs.count_documents({"status": "paused"})
    
    print("=== Verification ===")
    print(f"Total programs: {total_programs}")
    print(f"California programs: {ca_programs}")
    print(f"Active programs: {active_programs}")
    print(f"Paused programs: {paused_programs}\n")
    
    # Step 8: Show sample programs
    print("=== Sample Programs ===")
    samples = await db.programs.find({"state": "California"}, {"_id": 0, "program_name": 1, "benefit_type": 1, "county": 1}).limit(5).to_list(5)
    for i, prog in enumerate(samples, 1):
        county_info = f" ({prog.get('county', 'Statewide')})" if prog.get('county') else " (Statewide)"
        print(f"{i}. {prog['program_name']}{county_info}")
        print(f"   Type: {prog['benefit_type']}\n")
    
    print("✓ Seeding complete!\n")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_updated_programs())
