from pydantic import BaseModel


class GoogleTokenRequest(BaseModel):
    access_token: str