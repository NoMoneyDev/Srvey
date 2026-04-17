from pydantic import BaseModel
from typing import List, Optional


class ResponseCreate(BaseModel):
    survey_id: str
    user_id: str
