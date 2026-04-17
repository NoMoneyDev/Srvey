from pydantic import BaseModel
from typing import List, Optional


class AnswerCreate(BaseModel):
    question_id: str
    answer: List[str]


class AnswerUpdate(BaseModel):
    answer: List[str]
