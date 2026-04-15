from fastapi import APIRouter, Depends, HTTPException
from routes.utils import get_current_user
from services.survey_service import SurveyService
from schemas.survey import SurveyCreate, SurveyUpdate

router = APIRouter(prefix="/survey", 
                   tags=["Surveys"],
                   dependencies=[Depends(get_current_user)]
)

@router.get("")
async def get_all_surveys(page: int = 1, page_size: int = 10):
    return await SurveyService.get_all_surveys(page, page_size)

@router.get("/me")
async def get_my_surveys(page: int = 1, page_size: int = 10, user_id: str = Depends(get_current_user)):
    return await SurveyService.get_user_surveys(page, page_size, user_id)

@router.get("/{survey_id}")
async def get_survey(survey_id: str):
    survey = await SurveyService.get_survey(survey_id)
    if not survey:
        raise HTTPException(404, "Survey not found")
    return {"survey": survey}

@router.post("/")
async def create_survey(survey_data: SurveyCreate, user_id: str = Depends(get_current_user)):
    survey = await SurveyService.create_survey(survey_data, user_id)
    return survey

@router.put("/{survey_id}")
async def update_survey(survey_id: str, is_published: SurveyUpdate):
    survey = await SurveyService.update_survey(survey_id, is_published)
    return survey

@router.delete("/{survey_id}")
async def delete_survey(survey_id: str):
    success = await SurveyService.delete_survey(survey_id)
    if not success:
        raise HTTPException(404, "Survey not found")
    return {"message": "Deleted"}