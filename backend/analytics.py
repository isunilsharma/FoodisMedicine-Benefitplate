"""Analytics tracking for user events"""
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
from typing import Optional
import uuid

async def track_event(
    db: AsyncIOMotorDatabase,
    event_type: str,
    user_id: Optional[str] = None,
    metadata: dict = None
):
    """Track analytics event"""
    event = {
        "event_id": f"event_{uuid.uuid4().hex[:12]}",
        "event_type": event_type,
        "user_id": user_id,
        "metadata": metadata or {},
        "timestamp": datetime.now(timezone.utc)
    }
    
    await db.analytics_events.insert_one(event)

# Event types
EVENT_ZIP_SUBMITTED = "zip_submitted"
EVENT_QUESTIONNAIRE_STARTED = "questionnaire_started"
EVENT_QUESTIONNAIRE_COMPLETED = "questionnaire_completed"
EVENT_PROGRAMS_SHOWN = "programs_shown"
EVENT_PROGRAM_DETAIL_CLICKED = "program_detail_clicked"
EVENT_CHECKLIST_DOWNLOADED = "checklist_downloaded"
EVENT_RESULT_SAVED = "result_saved"
EVENT_PROGRAM_BROWSED = "program_browsed"
