from models import User
from schemas.user import UserCreate

class UserService:

    @staticmethod
    async def create_user(data):
        user = User(**data)
        await user.insert()
        return user

    @staticmethod
    async def find_one(query):
        return await User.find_one(query)

    @staticmethod
    async def get_all_users():
        return await User.find_all().to_list()

    @staticmethod
    async def get_user(user_id: str):
        return await User.get(user_id)

    @staticmethod
    async def update_user(user_id: str, data):
        user = await User.get(user_id)
        if not user:
            return None

        update_data = data.dict(exclude_unset=True)
        for k, v in update_data.items():
            setattr(user, k, v)

        await user.save()
        return user

    @staticmethod
    async def delete_user(user_id: str):
        user = await User.get(user_id)
        if not user:
            return False

        await user.delete()
        return True
    
