from fastapi import APIRouter, HTTPException, Depends
from services.answer.service import AnswerService
from services.answer.schema import AnswerCreate, AnswerUpdate
from typing import List
from utils import get_current_user

router = APIRouter(prefix="/survey/{survey_id}/question/{question_id}/answer", tags=["Answers"],
                   dependencies=[Depends(get_current_user)]
)

@router.get("/")
async def get_all_answers(question_id: str):
    return await AnswerService.get_all_answers(question_id)

@router.post("/")
async def create_answer(answer_data: List[AnswerCreate]):
    answers = []
    for answer in answer_data:
        answers.append(await AnswerService.create_answer(**answer.model_dump()))
    return answers
