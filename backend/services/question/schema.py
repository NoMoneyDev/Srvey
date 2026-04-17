from pydantic import BaseModel
from typing import List, Optional


class QuestionCreate(BaseModel):
    # survey_id: str
    question: str
    type: str
    choices: List[str]
    required: bool
    order: int


class QuestionUpdate(BaseModel):
    question: Optional[str] = None
    type: Optional[str] = None
    choices: Optional[List[str]] = None
    required: Optional[bool] = None
    order: Optional[int] = None
