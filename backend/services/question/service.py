from models import Question
from services.question.schema import QuestionCreate, QuestionUpdate
from logger import log_service_operation, log_error, debug_logger
import time


class QuestionService:

    @staticmethod
    async def create_question(question: str, type: str, choices: list, required: bool, order: int, survey_id: str):
        start_time = time.time()
        try:
            question_obj = Question(
                question=question,
                type=type,
                choices=choices,
                required=required,
                order=order,
                survey_id=survey_id
            )
            await question_obj.insert()
            duration = (time.time() - start_time) * 1000
            log_service_operation("QuestionService", "create_question", True, duration)
            debug_logger.debug(f"Question created: {question_obj.id}")
            return question_obj
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("QuestionService", "create_question", False, duration, str(e))
            log_error(e, "create_question")
            raise

    @staticmethod
    async def get_all_questions(survey_id: str):
        start_time = time.time()
        try:
            questions = await Question.find({"survey_id": survey_id}).to_list()
            duration = (time.time() - start_time) * 1000
            log_service_operation("QuestionService", "get_all_questions", True, duration)
            debug_logger.debug(f"Retrieved {len(questions)} questions for survey {survey_id}")
            return questions
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("QuestionService", "get_all_questions", False, duration, str(e))
            log_error(e, f"get_all_questions:{survey_id}")
            raise

    @staticmethod
    async def get_question(question_id: str):
        start_time = time.time()
        try:
            question = await Question.get(question_id)
            duration = (time.time() - start_time) * 1000
            log_service_operation("QuestionService", "get_question", True, duration)
            return question
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("QuestionService", "get_question", False, duration, str(e))
            log_error(e, f"get_question:{question_id}")
            raise

    @staticmethod
    async def update_question(question_id: str, data: QuestionUpdate):
        start_time = time.time()
        try:
            question = await Question.get(question_id)
            if not question:
                debug_logger.warning(f"Question not found: {question_id}")
                return None

            update_data = data.model_dump(exclude_unset=True)
            for k, v in update_data.items():
                setattr(question, k, v)

            await question.save()
            duration = (time.time() - start_time) * 1000
            log_service_operation("QuestionService", "update_question", True, duration)
            debug_logger.debug(f"Question updated: {question_id}")
            return question
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("QuestionService", "update_question", False, duration, str(e))
            log_error(e, f"update_question:{question_id}")
            raise

    @staticmethod
    async def delete_question(question_id: str):
        start_time = time.time()
        try:
            question = await Question.get(question_id)
            if not question:
                debug_logger.warning(f"Question not found for deletion: {question_id}")
                return False

            await question.delete()
            duration = (time.time() - start_time) * 1000
            log_service_operation("QuestionService", "delete_question", True, duration)
            debug_logger.debug(f"Question deleted: {question_id}")
            return True
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            log_service_operation("QuestionService", "delete_question", False, duration, str(e))
            log_error(e, f"delete_question:{question_id}")
            raise
