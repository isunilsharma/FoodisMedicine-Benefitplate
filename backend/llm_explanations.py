"""LLM-powered plain English explanations (controlled - no eligibility logic)"""
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
from typing import List, Dict, Any
from models import ProgramMatch

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')

async def generate_why_you_match_explanation(
    program_name: str,
    benefit_type: str,
    matched_conditions: List[str],
    unmet_conditions: List[str]
) -> str:
    """Generate plain-English explanation using LLM (GPT-5.2)"""
    
    if not matched_conditions:
        return "You may be eligible for this program based on your location and general eligibility criteria."
    
    # Create LLM chat instance
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"explain_{program_name[:20]}",
        system_message=(
            "You are a helpful assistant that explains program eligibility in plain, friendly language. "
            "ONLY use the provided matched conditions. Do NOT invent programs or requirements. "
            "Keep explanations under 2 sentences and user-friendly."
        )
    ).with_model("openai", "gpt-5.2")
    
    # Create prompt
    prompt = (
        f"Explain in 1-2 friendly sentences why someone matches the '{program_name}' program ({benefit_type}). "
        f"Base your explanation ONLY on these matched criteria: {', '.join(matched_conditions)}. "
        f"Do not mention unmet conditions. Start with 'You match this program because...'"
    )
    
    user_message = UserMessage(text=prompt)
    
    try:
        response = await chat.send_message(user_message)
        return response.strip()
    except Exception as e:
        # Fallback to simple concatenation
        return f"You match this program because: {', '.join(matched_conditions[:3])}"
