from models import Answer, Survey
from schemas.answer import AnswerCreate, AnswerUpdate

class AnswerService:

    @staticmethod
    async def create_answer(data: AnswerCreate):
        answer = Answer(**data)
        await answer.insert()
        return answer

    @staticmethod
    async def get_all_answers(question_id: str):
        answers = await Answer.find_all(question_id=question_id).to_list()
        return answers

    @staticmethod
    async def find_one(query):
        return await Answer.find_one(query)

    @staticmethod
    async def update_answer(answer_id: str, data: AnswerUpdate):
        answer = await Answer.get(answer_id)
        if not answer:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(answer, k, v)

        await answer.save()
        return answer

    @staticmethod
    async def delete_answer(answer_id: str):
        answer = await Answer.get(answer_id)
        if not answer:
            return False

        await answer.delete()
        return True
    
