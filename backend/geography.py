"""Geography mapping: ZIP code to County and State"""
import csv
import os
from typing import Optional, Dict
from motor.motor_asyncio import AsyncIOMotorDatabase

# HUD USPS ZIP-County crosswalk data
# Format: ZIP,COUNTY,STATE,STATE_CODE
SAMPLE_ZIP_DATA = [
    {"zip_code": "10001", "county": "New York County", "state": "New York", "state_code": "NY"},
    {"zip_code": "10002", "county": "New York County", "state": "New York", "state_code": "NY"},
    {"zip_code": "90001", "county": "Los Angeles County", "state": "California", "state_code": "CA"},
    {"zip_code": "90002", "county": "Los Angeles County", "state": "California", "state_code": "CA"},
    {"zip_code": "94102", "county": "San Francisco County", "state": "California", "state_code": "CA"},
    {"zip_code": "94103", "county": "San Francisco County", "state": "California", "state_code": "CA"},
    {"zip_code": "60601", "county": "Cook County", "state": "Illinois", "state_code": "IL"},
    {"zip_code": "60602", "county": "Cook County", "state": "Illinois", "state_code": "IL"},
    {"zip_code": "77001", "county": "Harris County", "state": "Texas", "state_code": "TX"},
    {"zip_code": "77002", "county": "Harris County", "state": "Texas", "state_code": "TX"},
    {"zip_code": "19019", "county": "Philadelphia County", "state": "Pennsylvania", "state_code": "PA"},
    {"zip_code": "19102", "county": "Philadelphia County", "state": "Pennsylvania", "state_code": "PA"},
    {"zip_code": "02101", "county": "Suffolk County", "state": "Massachusetts", "state_code": "MA"},
    {"zip_code": "02108", "county": "Suffolk County", "state": "Massachusetts", "state_code": "MA"},
    {"zip_code": "33101", "county": "Miami-Dade County", "state": "Florida", "state_code": "FL"},
    {"zip_code": "33109", "county": "Miami-Dade County", "state": "Florida", "state_code": "FL"},
    {"zip_code": "30301", "county": "Fulton County", "state": "Georgia", "state_code": "GA"},
    {"zip_code": "30303", "county": "Fulton County", "state": "Georgia", "state_code": "GA"},
    {"zip_code": "98101", "county": "King County", "state": "Washington", "state_code": "WA"},
    {"zip_code": "98104", "county": "King County", "state": "Washington", "state_code": "WA"},
]

async def seed_zip_data(db: AsyncIOMotorDatabase):
    """Seed sample ZIP code data into database"""
    # Check if already seeded
    count = await db.zip_county_mapping.count_documents({})
    if count > 0:
        print(f"ZIP data already seeded ({count} records)")
        return
    
    # Insert sample data
    await db.zip_county_mapping.insert_many(SAMPLE_ZIP_DATA)
    await db.zip_county_mapping.create_index("zip_code")
    print(f"Seeded {len(SAMPLE_ZIP_DATA)} ZIP code mappings")

async def lookup_zip(zip_code: str, db: AsyncIOMotorDatabase) -> Optional[Dict[str, str]]:
    """Lookup county and state for a ZIP code"""
    # Normalize ZIP (remove spaces, hyphens, take first 5 digits)
    zip_normalized = zip_code.replace(" ", "").replace("-", "")[:5]
    
    # Query database
    result = await db.zip_county_mapping.find_one(
        {"zip_code": zip_normalized},
        {"_id": 0}
    )
    
    return result
