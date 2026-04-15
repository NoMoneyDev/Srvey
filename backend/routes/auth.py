from services.user_service import UserService
from fastapi import APIRouter, HTTPException
from schemas.auth import GoogleTokenRequest
from google.oauth2 import id_token
from google.auth.transport import requests
from logger import log_auth_event, log_error, debug_logger
import httpx
from jose import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os 

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "google-client-id-placeholder")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-placeholder")
ALGORITHM = "HS256"


@router.post("/google")
async def google_auth(body: GoogleTokenRequest):
    # 1. Verify token with Google & get user info
    try:
        google_user = id_token.verify_oauth2_token(
            body.access_token,  # this is actually ID token
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
        debug_logger.debug(f"Google token verified for user: {google_user.get('email')}")

    except ValueError as e:
        debug_logger.warning(f"Google token verification failed: {str(e)}")
        log_auth_event("google_auth", success=False)
        log_error(e, "google_auth")
        raise HTTPException(status_code=401, detail="Invalid Google token")

    # google_user = response.json()
    # google_user has: sub, email, name, picture, email_verified

    # 2. Find or create user in MongoDB
    user_email = google_user["email"]
    try:
        user = await UserService.find_one({"email": user_email})
        if not user:
            debug_logger.debug(f"Creating new user: {user_email}")
            user = await UserService.create_user({
                "email": user_email,
                "name": google_user["name"],
                "google_id": google_user["sub"],
            })
            debug_logger.info(f"New user registered: {user_email}")
        else:
            debug_logger.debug(f"User found: {user_email}")
    except Exception as e:
        log_auth_event("google_auth", user_email, False)
        log_error(e, "google_auth - user lookup/creation")
        raise HTTPException(status_code=500, detail="User management error")

    # 3. Issue your own JWT
    try:
        payload = {
            "sub": google_user["email"],
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        log_auth_event("google_auth", user_email, True)
        debug_logger.debug(f"JWT token issued for: {user_email}")
    except Exception as e:
        log_auth_event("google_auth", user_email, False)
        log_error(e, "google_auth - token generation")
        raise HTTPException(status_code=500, detail="Token generation error")

    return {
        "access_token": token,
        "token_type": "bearer",
        "picture": google_user.get("picture", ""),
        "name": google_user.get("name", ""),
    }

