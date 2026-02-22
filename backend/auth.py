from fastapi import HTTPException, Request, Depends
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import os
import httpx
import uuid
from typing import Optional

from models import User, UserSession

# REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH

EMERGENT_AUTH_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'sunilbg100@gmail.com')

async def exchange_session_id(session_id: str, db) -> dict:
    """Exchange session_id for user data and session_token from Emergent Auth"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                EMERGENT_AUTH_URL,
                headers={"X-Session-ID": session_id},
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            # Create or update user in database
            user_id = f"user_{uuid.uuid4().hex[:12]}"
            
            # Check if user exists by email
            existing_user = await db.users.find_one({"email": data["email"]}, {"_id": 0})
            
            if existing_user:
                user_id = existing_user["user_id"]
                # Update user data
                await db.users.update_one(
                    {"user_id": user_id},
                    {"$set": {
                        "name": data["name"],
                        "picture": data.get("picture")
                    }}
                )
            else:
                # Create new user
                user_doc = {
                    "user_id": user_id,
                    "email": data["email"],
                    "name": data["name"],
                    "picture": data.get("picture"),
                    "created_at": datetime.now(timezone.utc)
                }
                await db.users.insert_one(user_doc)
            
            # Create session
            session_token = data["session_token"]
            expires_at = datetime.now(timezone.utc) + timedelta(days=7)
            
            session_doc = {
                "user_id": user_id,
                "session_token": session_token,
                "expires_at": expires_at,
                "created_at": datetime.now(timezone.utc)
            }
            await db.user_sessions.insert_one(session_doc)
            
            # Get user data
            user_doc = await db.users.find_one({"user_id": user_id}, {"_id": 0})
            
            return {
                "user": user_doc,
                "session_token": session_token
            }
            
        except httpx.HTTPError as e:
            raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

async def get_current_user(request: Request, db) -> Optional[User]:
    """Get current user from session_token (cookie or Authorization header)"""
    # Try to get token from cookie first
    session_token = request.cookies.get("session_token")
    
    # Fallback to Authorization header
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.replace("Bearer ", "")
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Find session
    session_doc = await db.user_sessions.find_one({"session_token": session_token}, {"_id": 0})
    
    if not session_doc:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    # Check expiry
    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")
    
    # Get user
    user_doc = await db.users.find_one({"user_id": session_doc["user_id"]}, {"_id": 0})
    
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(**user_doc)

async def require_admin(user: User) -> User:
    """Require user to be admin"""
    if user.email != ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

async def logout_user(session_token: str, db) -> bool:
    """Logout user by deleting session"""
    result = await db.user_sessions.delete_one({"session_token": session_token})
    return result.deleted_count > 0
