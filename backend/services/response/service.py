from models import Response
from services.response.schema import ResponseCreate

class ResponseService:

    @staticmethod
    async def create_response(data: ResponseCreate):
        response = Response(**data)
        await response.insert()
        return response

    @staticmethod
    async def get_all_responses(page: int = 1, page_size: int = 10):
        response = await Response.find_all().to_list()
        return {
            "responses": response,
        }

    @staticmethod
    async def delete_response(response_id: str):
        response = await Response.get(response_id)
        if not response:
            return False

        await response.delete()
        return True
    
