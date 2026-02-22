"""Seed California ZIP codes into database"""
import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def seed_california_zips():
    """Load California ZIP codes from JSON file and seed into database"""
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Check if already seeded
    existing_count = await db.zip_county_mapping.count_documents({"state_code": "CA"})
    if existing_count > 900:  # Already have comprehensive CA data
        print(f"✓ California ZIP codes already seeded ({existing_count} records)")
        return
    
    # Load California ZIP data
    json_file = '/tmp/california_zips.json'
    if not os.path.exists(json_file):
        print("✗ California ZIP data file not found. Run the generator script first.")
        return
    
    with open(json_file, 'r') as f:
        ca_zips = json.load(f)
    
    print(f"Loading {len(ca_zips)} California ZIP codes...")
    
    # Delete existing CA data to avoid duplicates
    delete_result = await db.zip_county_mapping.delete_many({"state_code": "CA"})
    print(f"Deleted {delete_result.deleted_count} existing CA records")
    
    # Insert new CA ZIP codes
    if ca_zips:
        await db.zip_county_mapping.insert_many(ca_zips)
        
        # Create index for fast lookups
        await db.zip_county_mapping.create_index("zip_code")
        await db.zip_county_mapping.create_index("state_code")
        
        print(f"✓ Successfully seeded {len(ca_zips)} California ZIP codes")
        
        # Verify
        total_count = await db.zip_county_mapping.count_documents({})
        ca_count = await db.zip_county_mapping.count_documents({"state_code": "CA"})
        print(f"✓ Total ZIP codes in database: {total_count}")
        print(f"✓ California ZIP codes: {ca_count}")
        
        # Show sample
        sample = await db.zip_county_mapping.find_one({"state_code": "CA"}, {"_id": 0})
        print(f"✓ Sample record: {sample}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_california_zips())
