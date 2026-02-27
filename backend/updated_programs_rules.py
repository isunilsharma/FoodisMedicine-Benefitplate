"""Program eligibility rules - Research-backed dataset"""

PROGRAM_RULES = [
    # 1. Fresh Rx Produce Prescription (Monterey County)
    {
        "program_id": "prog_ca_fresh_rx_monterey",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "Medi-Cal ID card",
                "Chronic condition documentation"
            ],
            "optional": [
                "Provider note",
                "Recent discharge summary"
            ]
        },
        "referral_required": False,
        "requires_medicaid": True,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": ["Diabetes", "Hypertension", "Heart disease"],
        "notes": "Free medically supportive produce box for 12-24 weeks for Medi-Cal members with eligible health conditions. Enrollment via online form or by phone."
    },
    
    # 2-6. Alliance Community Supports MTM (all 5 counties)
    {
        "program_id": "prog_ca_alliance_mtm_mariposa",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "Medi-Cal ID card",
                "Provider or care-team referral"
            ],
            "optional": [
                "Documentation of medical or social need"
            ]
        },
        "referral_required": True,
        "requires_medicaid": True,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Community Supports Meals benefit accessed via plan authorization. Referrals accepted from providers, care managers, hospitals, community agencies, and social workers."
    },
    {
        "program_id": "prog_ca_alliance_mtm_merced",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "Medi-Cal ID card",
                "Provider or care-team referral"
            ],
            "optional": [
                "Documentation of medical or social need"
            ]
        },
        "referral_required": True,
        "requires_medicaid": True,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Community Supports Meals benefit accessed via plan authorization. Referrals accepted from providers, care managers, hospitals, community agencies, and social workers."
    },
    {
        "program_id": "prog_ca_alliance_mtm_monterey",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "Medi-Cal ID card",
                "Provider or care-team referral"
            ],
            "optional": [
                "Documentation of medical or social need"
            ]
        },
        "referral_required": True,
        "requires_medicaid": True,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Community Supports Meals benefit accessed via plan authorization. Referrals accepted from providers, care managers, hospitals, community agencies, and social workers."
    },
    {
        "program_id": "prog_ca_alliance_mtm_santa_cruz",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "Medi-Cal ID card",
                "Provider or care-team referral"
            ],
            "optional": [
                "Documentation of medical or social need"
            ]
        },
        "referral_required": True,
        "requires_medicaid": True,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Community Supports Meals benefit accessed via plan authorization. Referrals accepted from providers, care managers, hospitals, community agencies, and social workers."
    },
    {
        "program_id": "prog_ca_alliance_mtm_san_benito",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "Medi-Cal ID card",
                "Provider or care-team referral"
            ],
            "optional": [
                "Documentation of medical or social need"
            ]
        },
        "referral_required": True,
        "requires_medicaid": True,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Community Supports Meals benefit accessed via plan authorization. Referrals accepted from providers, care managers, hospitals, community agencies, and social workers."
    },
    
    # 7. Market Match (California)
    {
        "program_id": "prog_ca_market_match",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "CalFresh EBT card"
            ],
            "optional": []
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": True,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL", "139-200% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Use CalFresh EBT at participating farmers markets and farm-direct outlets to receive Market Match tokens or vouchers for fruits and vegetables. No separate application needed."
    },
    
    # 8. CalFresh Fruit & Vegetable EBT Pilot
    {
        "program_id": "prog_ca_calfresh_fv_pilot",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "CalFresh EBT card"
            ],
            "optional": []
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": True,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL", "139-200% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Relaunched Nov 17, 2025. Eligible CalFresh households automatically earn dollar-for-dollar match up to $60/month when buying eligible produce at participating locations. No sign-up required."
    },
    
    # Out-of-state programs (for when we expand beyond CA)
    {
        "program_id": "prog_wa_snap_market_match",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": ["SNAP EBT card"],
            "optional": []
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": True,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "At participating farmers markets, SNAP benefits matched $10+ per day starting Jan 1, 2026. No separate application."
    },
    {
        "program_id": "prog_wa_snap_produce_match",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": ["SNAP EBT card"],
            "optional": []
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": True,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Starting Oct 1, 2025. Buy $10+ eligible produce with EBT to get $5 coupon/discount."
    },
    {
        "program_id": "prog_co_double_up_food_bucks",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": ["EBT card"],
            "optional": []
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": True,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Dollar-for-dollar match on produce up to $20/day at participating locations. No sign-ups necessary."
    },
    {
        "program_id": "prog_co_snap_produce_bonus",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": ["EBT card"],
            "optional": []
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": True,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "100% reimbursement of qualifying produce purchases back to EBT at time of purchase, up to $60/month. No sign-up required."
    },
    {
        "program_id": "prog_mi_double_up_food_bucks",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": ["EBT/Bridge Card"],
            "optional": []
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": True,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "Use Bridge Card to get dollar-for-dollar match on produce. Some locations may require quick sign-up at checkout."
    },
    {
        "program_id": "prog_or_double_up_food_bucks",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": ["EBT card"],
            "optional": []
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": True,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "SNAP shoppers earn Double Up at participating CSAs, farmers markets, farm stands, and groceries. Some sites require quick sign-up."
    },
    {
        "program_id": "prog_ny_health_bucks",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": ["SNAP EBT card"],
            "optional": []
        },
        "referral_required": False,
        "requires_medicaid": False,
        "requires_snap": True,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "For every $2 spent with SNAP at NYC farmers markets, receive $2 Health Bucks up to $10/day for fruits and vegetables."
    },
    {
        "program_id": "prog_nc_healthy_opportunities",
        "eligibility_conditions_json": {},
        "document_checklist_json": {
            "required": [
                "Medicaid member ID",
                "Care management authorization"
            ],
            "optional": [
                "Member consent form"
            ]
        },
        "referral_required": True,
        "requires_medicaid": True,
        "requires_snap": False,
        "min_age": None,
        "max_age": None,
        "income_fpl_bands_allowed": ["Under 100% FPL", "100-138% FPL"],
        "diagnosis_categories_allowed": [],
        "notes": "PAUSED: Program services stopped July 1, 2025 due to lack of state budget funding. Verify current status before referral."
    },
]

print(f"Total program rules: {len(PROGRAM_RULES)}")
