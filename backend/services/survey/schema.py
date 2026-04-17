from pydantic import BaseModel, EmailStr
from typing import Optional

class SurveyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    # created_by: str
    is_published: bool


class SurveyUpdate(BaseModel):
    is_published: bool

