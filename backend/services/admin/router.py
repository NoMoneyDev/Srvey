# routes/admin.py
from fastapi import APIRouter, Depends
from typing import List
from models import Survey, User, Question
from utils import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/surveys")
async def get_all_surveys(page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size

    surveys = (
        await Survey.find()
        .sort("-created_at")
        .skip(skip)
        .limit(page_size)
        .to_list()
    )

    total = await Survey.find().count()

    result = []

    for s in surveys:
        user = await User.find_one(User.email == s.created_by)
        result.append({
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "is_published": s.is_published,
            "created_at": s.created_at,
            "owner_name": user.name if user else "Unknown"
        })

    return {
        "surveys": result,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": -(-total // page_size)
    }

@router.get("/users")
async def get_all_users(page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size

    users = (
        await User.find()
        .skip(skip)
        .limit(page_size)
        .to_list()
    )

    total = await User.find().count()

    return {
        "users": [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email
            }
            for u in users
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": -(-total // page_size)
    }

from fastapi import HTTPException

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    user = await User.get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()

    return {"message": "User deleted"}

@router.delete("/surveys/{survey_id}")
async def delete_survey(survey_id: str):
    survey = await Survey.get(survey_id)

    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    await survey.delete()

    return {"message": "Survey deleted"}

@router.get("/surveys/{survey_id}/questions")
async def get_survey_questions_admin(survey_id: str):
    # check survey exists
    survey = await Survey.get(survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    # get all questions for this survey
    questions = (
        await Question.find(Question.survey_id == survey_id)
        .sort("order")
        .to_list()
    )

    return {
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "type": q.type,
                "choices": q.choices if hasattr(q, "choices") else [],
                "required": getattr(q, "required", False),
                "order": getattr(q, "order", 0)
            }
            for q in questions
        ]
    }