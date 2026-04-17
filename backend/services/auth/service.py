from google.oauth2 import id_token
from google.auth.transport import requests
from models import User
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "google-client-id-placeholder")


class AuthService:

    @staticmethod
    async def login_with_google(token: str):
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                GOOGLE_CLIENT_ID
            )

            google_id = idinfo["sub"]
            email = idinfo["email"]
            name = idinfo.get("name", "")

            user = await User.find_one(User.google_id == google_id)

            if not user:
                user = User(
                    email=email,
                    name=name,
                    google_id=google_id
                )
                await user.insert()

            return user

        except Exception as e:
            raise Exception("Invalid Google token")