from fastapi import APIRouter, HTTPException, Depends
from services.user.service import UserService

from utils import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.delete("/delete")
async def delete_user(user_id: str = Depends(get_current_user)):
    success = await UserService.delete_user(user_id)
    if not success:
        raise HTTPException(404, "User not found")
    return {"message": "Deleted"}