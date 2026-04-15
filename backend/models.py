from beanie import Document
from pydantic import Field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4


class User(Document):
    email: str
    name: str
    google_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"


class Survey(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: Optional[str] = None
    created_by: str
    is_published: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "surveys"


class Question(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    survey_id: str
    question: str
    type: str  # e.g. "text", "multiple_choice", "checkbox", "rating"
    choices: list[str] = []
    required: bool = False
    order: int

    class Settings:
        name = "questions"


class Response(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    survey_id: str
    user_id: Optional[str] = None  # optional if you allow anonymous responses
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "responses"


class Answer(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    response_id: str
    question_id: str
    answer: list[str] = []

    class Settings:
        name = "answers"