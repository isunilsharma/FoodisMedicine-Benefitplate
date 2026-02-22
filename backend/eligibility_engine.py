"""Deterministic eligibility evaluation engine"""
from typing import List, Dict, Any
from models import (
    QuestionnaireAnswers, 
    ProgramMatch, 
    EligibilityStatus,
    BenefitType,
    Program,
    ProgramRule
)
from motor.motor_asyncio import AsyncIOMotorDatabase

def evaluate_condition(condition: Dict[str, Any], answers: Dict[str, Any]) -> bool:
    """Evaluate a single eligibility condition"""
    operator = condition.get("operator")
    field = condition.get("field")
    value = condition.get("value")
    
    answer_value = answers.get(field)
    
    if operator == "eq":
        return answer_value == value
    elif operator == "neq":
        return answer_value != value
    elif operator == "in":
        return answer_value in value
    elif operator == "not_in":
        return answer_value not in value
    elif operator == "gt":
        return answer_value > value
    elif operator == "gte":
        return answer_value >= value
    elif operator == "lt":
        return answer_value < value
    elif operator == "lte":
        return answer_value <= value
    elif operator == "exists":
        return (field in answers) == value
    elif operator == "contains":
        if isinstance(answer_value, list):
            return value in answer_value
        return False
    elif operator == "any_true":
        # For checkbox arrays - at least one value from the list is in answer
        if isinstance(answer_value, list):
            return any(v in answer_value for v in value)
        return False
    
    return False

def evaluate_rule_logic(logic: Dict[str, Any], answers: Dict[str, Any]) -> tuple[bool, List[str], List[str]]:
    """Evaluate complex rule logic (all_of, any_of, none_of)"""
    matched_conditions = []
    unmet_conditions = []
    
    # Evaluate all_of conditions
    if "all_of" in logic:
        for condition in logic["all_of"]:
            if evaluate_condition(condition, answers):
                matched_conditions.append(f"{condition['field']} {condition['operator']} {condition['value']}")
            else:
                unmet_conditions.append(f"{condition['field']} {condition['operator']} {condition['value']}")
                return False, matched_conditions, unmet_conditions
    
    # Evaluate any_of conditions
    if "any_of" in logic:
        any_matched = False
        for condition in logic["any_of"]:
            if evaluate_condition(condition, answers):
                matched_conditions.append(f"{condition['field']} {condition['operator']} {condition['value']}")
                any_matched = True
        if not any_matched:
            unmet_conditions.append("None of the any_of conditions met")
            return False, matched_conditions, unmet_conditions
    
    # Evaluate none_of conditions
    if "none_of" in logic:
        for condition in logic["none_of"]:
            if evaluate_condition(condition, answers):
                unmet_conditions.append(f"Should not have: {condition['field']} {condition['operator']} {condition['value']}")
                return False, matched_conditions, unmet_conditions
    
    return True, matched_conditions, unmet_conditions

async def evaluate_eligibility(
    zip_code: str,
    county: str,
    state: str,
    state_code: str,
    answers: QuestionnaireAnswers,
    db: AsyncIOMotorDatabase
) -> Dict[str, List[ProgramMatch]]:
    """Deterministic eligibility evaluation"""
    
    # Convert answers to dict for evaluation
    answers_dict = answers.model_dump()
    
    # Query programs matching geography
    geo_filter = {
        "status": "active",
        "$or": [
            {"geo_scope": "national"},
            {"geo_scope": "state", "state": state},
            {"geo_scope": "county", "state": state, "county": county},
        ]
    }
    
    programs = await db.programs.find(geo_filter, {"_id": 0}).to_list(1000)
    
    # OPTIMIZATION: Batch fetch all program rules at once (avoid N+1 queries)
    program_ids = [p["program_id"] for p in programs]
    rules_cursor = await db.program_rules.find(
        {"program_id": {"$in": program_ids}},
        {"_id": 0}
    ).to_list(1000)
    rules_by_id = {r["program_id"]: r for r in rules_cursor}
    
    likely_eligible = []
    possibly_eligible = []
    community = []
    
    for program_doc in programs:
        program = Program(**program_doc)
        
        # Get program rules from pre-fetched dict
        rule_doc = rules_by_id.get(program.program_id)
        
        if not rule_doc:
            # No rules = community program
            match = ProgramMatch(
                program_id=program.program_id,
                program_name=program.program_name,
                benefit_type=program.benefit_type,
                match_score=0.5,
                eligibility_status=EligibilityStatus.community,
                matched_conditions=[],
                unmet_conditions=[],
                why_you_match="This is a community program with minimal eligibility requirements.",
                document_checklist={},
                how_to_apply_url=program.how_to_apply_url,
                contact_phone=program.contact_phone,
                source_urls=program.source_urls
            )
            community.append(match)
            continue
        
        rule = ProgramRule(**rule_doc)
        
        # Evaluate eligibility conditions
        conditions = rule.eligibility_conditions_json
        
        # Simple case: no complex logic, just check basic requirements
        if not conditions or "match_logic" not in conditions:
            # Check basic requirements
            is_match = True
            matched = []
            unmet = []
            
            if rule.requires_medicaid and answers.enrolled_medicaid != "Yes":
                is_match = False
                unmet.append("Requires Medicaid enrollment")
            elif rule.requires_medicaid:
                matched.append("Enrolled in Medicaid")
            
            if rule.requires_snap and answers.enrolled_snap != "Yes":
                is_match = False
                unmet.append("Requires SNAP enrollment")
            elif rule.requires_snap:
                matched.append("Enrolled in SNAP")
            
            # Check age range
            if rule.min_age or rule.max_age:
                age_matched = False
                if answers.age_range == "Under 18" and (rule.min_age is None or rule.min_age <= 0):
                    age_matched = True
                elif answers.age_range == "18-59" and (rule.min_age is None or rule.min_age <= 18) and (rule.max_age is None or rule.max_age >= 59):
                    age_matched = True
                elif answers.age_range == "60+" and (rule.max_age is None or rule.max_age >= 60):
                    age_matched = True
                
                if age_matched:
                    matched.append(f"Age range: {answers.age_range}")
                else:
                    is_match = False
                    unmet.append(f"Age requirement not met")
            
            # Check income bands
            if rule.income_fpl_bands_allowed:
                if answers.income_band in rule.income_fpl_bands_allowed or answers.income_band == "Not sure":
                    matched.append(f"Income band: {answers.income_band}")
                else:
                    is_match = False
                    unmet.append(f"Income requirement not met")
            
            # Determine status
            if is_match:
                if answers.enrolled_medicaid == "Not sure" or answers.enrolled_snap == "Not sure" or answers.income_band == "Not sure":
                    status = EligibilityStatus.possibly_eligible
                else:
                    status = EligibilityStatus.likely_eligible
            else:
                if rule.referral_required:
                    status = EligibilityStatus.possibly_eligible
                else:
                    continue  # Skip this program
            
            match = ProgramMatch(
                program_id=program.program_id,
                program_name=program.program_name,
                benefit_type=program.benefit_type,
                match_score=len(matched) / max(len(matched) + len(unmet), 1),
                eligibility_status=status,
                matched_conditions=matched,
                unmet_conditions=unmet,
                why_you_match=" ".join(matched) if matched else "May be eligible with provider referral",
                document_checklist=rule.document_checklist_json,
                how_to_apply_url=program.how_to_apply_url,
                contact_phone=program.contact_phone,
                source_urls=program.source_urls
            )
            
            if status == EligibilityStatus.likely_eligible:
                likely_eligible.append(match)
            else:
                possibly_eligible.append(match)
        
        else:
            # Complex rule evaluation
            match_logic = conditions.get("match_logic", {})
            is_match, matched, unmet = evaluate_rule_logic(match_logic, answers_dict)
            
            # Check classification
            classification = conditions.get("classification", {})
            
            if is_match:
                # Check if likely or possible
                if "possible_if" in classification:
                    possible_logic = classification["possible_if"]
                    is_possible, _, _ = evaluate_rule_logic(possible_logic, answers_dict)
                    status = EligibilityStatus.possibly_eligible if is_possible else EligibilityStatus.likely_eligible
                else:
                    status = EligibilityStatus.likely_eligible
                
                match = ProgramMatch(
                    program_id=program.program_id,
                    program_name=program.program_name,
                    benefit_type=program.benefit_type,
                    match_score=len(matched) / max(len(matched) + len(unmet), 1),
                    eligibility_status=status,
                    matched_conditions=matched,
                    unmet_conditions=unmet,
                    why_you_match=" ".join(matched[:3]) if matched else "Matches eligibility criteria",
                    document_checklist=rule.document_checklist_json,
                    how_to_apply_url=program.how_to_apply_url,
                    contact_phone=program.contact_phone,
                    source_urls=program.source_urls
                )
                
                if status == EligibilityStatus.likely_eligible:
                    likely_eligible.append(match)
                else:
                    possibly_eligible.append(match)
    
    # Sort by match score
    likely_eligible.sort(key=lambda x: x.match_score, reverse=True)
    possibly_eligible.sort(key=lambda x: x.match_score, reverse=True)
    
    return {
        "likely_eligible": likely_eligible,
        "possibly_eligible": possibly_eligible,
        "community": community
    }
