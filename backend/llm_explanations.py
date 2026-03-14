"""LLM-powered plain English explanations (controlled - no eligibility logic)"""
from openai import AsyncOpenAI
import os
from typing import List, Dict, Any
from models import ProgramMatch

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
LLM_MODEL = os.environ.get('LLM_MODEL', 'gpt-4o')

async def generate_why_you_match_explanation(
    program_name: str,
    benefit_type: str,
    matched_conditions: List[str],
    unmet_conditions: List[str]
) -> str:
    """Generate plain-English explanation using LLM"""

    if not matched_conditions:
        return "You may be eligible for this program based on your location and general eligibility criteria."

    if not OPENAI_API_KEY:
        return f"You match this program because: {', '.join(matched_conditions[:3])}"

    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    prompt = (
        f"Explain in 1-2 friendly sentences why someone matches the '{program_name}' program ({benefit_type}). "
        f"Base your explanation ONLY on these matched criteria: {', '.join(matched_conditions)}. "
        f"Do not mention unmet conditions. Start with 'You match this program because...'"
    )

    try:
        response = await client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that explains program eligibility in plain, friendly language. "
                        "ONLY use the provided matched conditions. Do NOT invent programs or requirements. "
                        "Keep explanations under 2 sentences and user-friendly."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return f"You match this program because: {', '.join(matched_conditions[:3])}"
