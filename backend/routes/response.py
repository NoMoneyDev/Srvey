from fastapi import APIRouter, HTTPException, Depends
from services.response_service import ResponseService
from services.answer_service import AnswerService
from schemas.response import ResponseCreate
from schemas.answer import AnswerCreate
from typing import List
from routes.utils import get_current_user

router = APIRouter(prefix="/survey/{survey_id}/response", tags=["Responses"],
                       dependencies=[Depends(get_current_user)]  # protects all routes in this router
)

@router.get("/")
async def get_all_responses(survey_id: str):
    return await ResponseService.get_all_responses(survey_id)


@router.post("/")
async def create_response(
    survey_id: str,
    answer_data: List[AnswerCreate],
    user_id: str = Depends(get_current_user)
):
    response = await ResponseService.create_response({
        "survey_id": survey_id,
        "user_id": user_id
    })

    created_answers = []
    for answer in answer_data:
        created_answers.append(
            await AnswerService.create_answer({
                **answer.dict(),
                "response_id": str(response.id)  # ✅ backend handles this
            })
        )

    return created_answers

@router.delete("/{response_id}")
async def delete_response(response_id: str):
    success = await ResponseService.delete_response(response_id)
    if not success:
        raise HTTPException(404, "Response not found")
    return {"message": "Deleted"}