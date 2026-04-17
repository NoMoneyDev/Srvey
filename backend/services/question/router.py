from fastapi import APIRouter, HTTPException, Depends, Body
from services.question.service import QuestionService
from services.question.schema import QuestionUpdate, QuestionCreate
from typing import List
from utils import get_current_user

router = APIRouter(prefix="/survey/{survey_id}/question", tags=["Questions"],
                   dependencies=[Depends(get_current_user)]  # protects all routes in this router
)

@router.get("")
async def get_all_questions(survey_id: str):
    return await QuestionService.get_all_questions(survey_id)

@router.post("")
async def create_question(survey_id: str, question_data: List[QuestionCreate] = Body(...)):
    questions = []
    for question in question_data:
        questions.append(await QuestionService.create_question(**question.model_dump(), survey_id=survey_id))
    return questions
