"""Seed sample Food Is Medicine programs"""
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase

SAMPLE_PROGRAMS = [
    {
        "program_id": "prog_ca_produce_rx_1",
        "program_name": "California Fresh Produce Prescription Program",
        "benefit_type": "produce_rx",
        "geo_scope": "state",
        "state": "California",
        "county": None,
        "zip_prefixes": None,
        "how_to_apply_url": "https://www.cdph.ca.gov/produce-rx",
        "contact_phone": "1-800-555-0100",
        "source_urls": ["https://www.cdph.ca.gov/produce-rx"],
        "status": "active",
        "effective_start": datetime.now(timezone.utc) - timedelta(days=180),
        "effective_end": None,
        "last_verified_at": datetime.now(timezone.utc) - timedelta(days=15),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "program_id": "prog_ca_mtm_1",
        "program_name": "LA County Medically Tailored Meals",
        "benefit_type": "mtm",
        "geo_scope": "county",
        "state": "California",
        "county": "Los Angeles County",
        "zip_prefixes": None,
        "how_to_apply_url": "https://lacounty.gov/mtm",
        "contact_phone": "1-800-555-0101",
        "source_urls": ["https://lacounty.gov/mtm"],
        "status": "active",
        "effective_start": datetime.now(timezone.utc) - timedelta(days=90),
        "effective_end": None,
        "last_verified_at": datetime.now(timezone.utc) - timedelta(days=10),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "program_id": "prog_national_snap_1",
        "program_name": "SNAP Nutrition Incentive Program",
        "benefit_type": "snap_support",
        "geo_scope": "national",
        "state": None,
        "county": None,
        "zip_prefixes": None,
        "how_to_apply_url": "https://www.fns.usda.gov/snap",
        "contact_phone": "1-800-555-0102",
        "source_urls": ["https://www.fns.usda.gov/snap"],
        "status": "active",
        "effective_start": datetime.now(timezone.utc) - timedelta(days=365),
        "effective_end": None,
        "last_verified_at": datetime.now(timezone.utc) - timedelta(days=30),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "program_id": "prog_ny_diabetes_1",
        "program_name": "NYC Diabetes Prevention Nutrition Program",
        "benefit_type": "nutrition_coaching",
        "geo_scope": "county",
        "state": "New York",
        "county": "New York County",
        "zip_prefixes": None,
        "how_to_apply_url": "https://www1.nyc.gov/site/doh/health/health-topics/diabetes-prevention.page",
        "contact_phone": "1-800-555-0103",
        "source_urls": ["https://www1.nyc.gov/site/doh/health/health-topics/diabetes-prevention.page"],
        "status": "active",
        "effective_start": datetime.now(timezone.utc) - timedelta(days=120),
        "effective_end": None,
        "last_verified_at": datetime.now(timezone.utc) - timedelta(days=20),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "program_id": "prog_tx_pantry_1",
        "program_name": "Harris County Food Bank - Medicaid Program",
        "benefit_type": "pantry",
        "geo_scope": "county",
        "state": "Texas",
        "county": "Harris County",
        "zip_prefixes": None,
        "how_to_apply_url": "https://www.houstonfoodbank.org/",
        "contact_phone": "1-800-555-0104",
        "source_urls": ["https://www.houstonfoodbank.org/"],
        "status": "active",
        "effective_start": datetime.now(timezone.utc) - timedelta(days=200),
        "effective_end": None,
        "last_verified_at": datetime.now(timezone.utc) - timedelta(days=5),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "program_id": "prog_ma_mtg_1",
        "program_name": "Massachusetts Healthy Incentives Program",
        "benefit_type": "mtg",
        "geo_scope": "state",
        "state": "Massachusetts",
        "county": None,
        "zip_prefixes": None,
        "how_to_apply_url": "https://www.mass.gov/healthy-incentives-program",
        "contact_phone": "1-800-555-0105",
        "source_urls": ["https://www.mass.gov/healthy-incentives-program"],
        "status": "active",
        "effective_start": datetime.now(timezone.utc) - timedelta(days=300),
        "effective_end": None,
        "last_verified_at": datetime.now(timezone.utc) - timedelta(days=25),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
]

SAMPLE_RULES = [
    {
        "program_id": "prog_ca_produce_rx_1",
        "eligibility_conditions_json": {
            "version": "1.0",
            "match_logic": {
                "all_of": [
                    {"field": "enrolled_medicaid", "operator": "eq", "value": "Yes"},
                ],
                "any_of": [
                    {"field": "health_conditions", "operator": "contains", "value": "Diabetes"},
                    {"field": "health_conditions", "operator": "contains", "value": "Hypertension"},
                    {"field": "health_conditions", "operator": "contains", "value": "Heart disease"},
                ]
            }
        },
        "document_checklist_json": {
            "required": [
                "Medicaid ID card",
                "Doctor's referral or diagnosis confirmation",
                "Proof of residency in California"
            ],
            "optional": [
                "Recent medical records"
            ]
        },
        "referral_required": True,
        "requires_medicaid": True,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL", "139-200% FPL"],
        "diagnosis_categories_allowed": ["Diabetes", "Hypertension", "Heart disease"],
        "notes": "Requires physician referral. Fresh produce vouchers distributed monthly."
    },
    {
        "program_id": "prog_ca_mtm_1",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "Medicaid ID (LA County plan)",
                "Medical documentation of chronic condition",
                "Physician referral for medically tailored meals"
            ],
            "optional": []
        },
        "referral_required": True,
        "requires_medicaid": True,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": ["Diabetes", "Heart disease", "Kidney disease"],
        "notes": "LA County Medicaid managed care only. Requires serious chronic condition."
    },
    {
        "program_id": "prog_national_snap_1",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "Proof of income",
                "Photo ID",
                "Proof of address"
            ],
            "optional": [
                "Utility bills",
                "Household member information"
            ]
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL", "139-200% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "National SNAP program with nutrition incentives for fresh produce."
    },
    {
        "program_id": "prog_ny_diabetes_1",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "NYC residency proof",
                "Diabetes diagnosis or pre-diabetes screening",
                "Health insurance information"
            ],
            "optional": [
                "A1C test results"
            ]
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": False,
        "min_age": 18,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL", "139-200% FPL", "201-300% FPL"],
        "diagnosis_categories_allowed": ["Diabetes"],
        "notes": "Free nutrition counseling and diabetes prevention program for NYC residents."
    },
    {
        "program_id": "prog_tx_pantry_1",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "Medicaid ID or proof of low income",
                "Harris County residency"
            ],
            "optional": [
                "SNAP enrollment proof for additional benefits"
            ]
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL", "139-200% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Food bank with special services for Medicaid members. No strict health requirements."
    },
    {
        "program_id": "prog_ma_mtg_1",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "SNAP EBT card",
                "Massachusetts residency"
            ],
            "optional": []
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": True,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Automatic SNAP benefit enhancement for purchasing fruits and vegetables. Must be enrolled in SNAP."
    },
]

async def seed_programs(db: AsyncIOMotorDatabase):
    """Seed sample programs and rules"""
    # Check if already seeded
    count = await db.programs.count_documents({})
    if count > 0:
        print(f"Programs already seeded ({count} programs)")
        return
    
    # Insert programs
    await db.programs.insert_many(SAMPLE_PROGRAMS)
    await db.programs.create_index("program_id", unique=True)
    await db.programs.create_index("status")
    await db.programs.create_index("state")
    await db.programs.create_index("county")
    
    # Insert rules
    await db.program_rules.insert_many(SAMPLE_RULES)
    await db.program_rules.create_index("program_id", unique=True)
    
    print(f"Seeded {len(SAMPLE_PROGRAMS)} programs and {len(SAMPLE_RULES)} rules")
