import time
from models import Survey
from services.survey.schema import SurveyCreate, SurveyUpdate
from logger import log_service_operation, log_error, debug_logger


class SurveyService:

    @staticmethod
    async def create_survey(data: SurveyCreate, user_id: str):
        start_time = time.time()
        try:
            survey = Survey(**data.model_dump(), created_by=user_id)
            await survey.insert()
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "create_survey", True, duration)
            debug_logger.debug(f"Survey created: {survey.id}")
            return survey
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "create_survey", False, duration, str(e))
            log_error(e, "create_survey")
            raise

    @staticmethod
    async def get_user_surveys(page: int = 1, page_size: int = 10, user_id: str = None):
        start_time = time.time()
        try:
            skip = (page - 1) * page_size

            # fetch surveys created by this user
            surveys = (
                await Survey.find(Survey.created_by == user_id)
                .sort('-created_at')
                .skip(skip)
                .limit(page_size)
                .to_list()
            )

            total = await Survey.find(Survey.created_by == user_id).count()

            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "get_user_surveys", True, duration)
            debug_logger.debug(f"User {user_id} surveys: {len(surveys)} (total: {total})")

            return {
                "surveys": surveys,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": -(-total // page_size)
            }

        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "get_user_surveys", False, duration, str(e))
            log_error(e, f"get_user_surveys:{user_id}")
            raise

    @staticmethod
    async def get_all_surveys(page: int = 1, page_size: int = 10):
        start_time = time.time()
        try:
            skip = (page - 1) * page_size
            surveys = await Survey.find(Survey.is_published == True).sort('-created_at').skip(skip).limit(page_size).to_list()
            total = await Survey.find(Survey.is_published == True).count()
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "get_all_surveys", True, duration)
            debug_logger.debug(f"Retrieved {len(surveys)} surveys (total: {total})")
            return {
                "surveys": surveys,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": -(-total // page_size)  # ceiling division
            }
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "get_all_surveys", False, duration, str(e))
            log_error(e, "get_all_surveys")
            raise

    @staticmethod
    async def find_one(query):
        start_time = time.time()
        try:
            result = await Survey.find_one(query)
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "find_one", True, duration)
            return result
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "find_one", False, duration, str(e))
            log_error(e, "find_one")
            raise

    @staticmethod
    async def get_survey(survey_id: str):
        start_time = time.time()
        try:
            survey = await Survey.get(survey_id)
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "get_survey", True, duration)
            debug_logger.debug(f"Retrieved survey: {survey_id}")
            return survey
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "get_survey", False, duration, str(e))
            log_error(e, f"get_survey:{survey_id}")
            raise

    @staticmethod
    async def update_survey(survey_id: str, data: SurveyUpdate):
        start_time = time.time()
        try:
            survey = await Survey.get(survey_id)
            if not survey:
                debug_logger.warning(f"Survey not found: {survey_id}")
                return None

            update_data = data.model_dump(exclude_unset=True)
            for k, v in update_data.items():
                setattr(survey, k, v)

            await survey.save()
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "update_survey", True, duration)
            debug_logger.debug(f"Survey updated: {survey_id}")
            return survey
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "update_survey", False, duration, str(e))
            log_error(e, f"update_survey:{survey_id}")
            raise

    @staticmethod
    async def delete_survey(survey_id: str):
        start_time = time.time()
        try:
            survey = await Survey.get(survey_id)
            if not survey:
                debug_logger.warning(f"Survey not found for deletion: {survey_id}")
                return False

            await survey.delete()
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "delete_survey", True, duration)
            debug_logger.debug(f"Survey deleted: {survey_id}")
            return True
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("SurveyService", "delete_survey", False, duration, str(e))
            log_error(e, f"delete_survey:{survey_id}")
            raise
    
