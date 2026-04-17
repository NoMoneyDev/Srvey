from fastapi import APIRouter, Depends
from services.analytic.service import AnalyticService
from utils import get_current_user

router = APIRouter(
    prefix="/survey/{survey_id}/analytics",
    tags=["Analytics"],
    dependencies=[Depends(get_current_user)]
)

@router.get("")
async def get_survey_analytics(survey_id: str):
    return await AnalyticService.get_survey_analytics(survey_id)