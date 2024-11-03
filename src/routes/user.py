from fastapi import APIRouter, HTTPException
from prisma import Prisma

from src.models.user import User
from src.services.user_service import put_user_to_db, post_user_to_db

router = APIRouter()
prisma = Prisma()


@router.post("/register-user")
async def register_user(user: User):
    success = await post_user_to_db(user)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to save user")
    return {"message": "User saved successfully"}


@router.post("/update-user-score")
async def update_user_score(user: User):
    success = await put_user_to_db(user)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to update user")
    return {"message": "User saved successfully"}


@router.post("/login-user")
async def login_user(user: User):
    await prisma.connect()
    user = await prisma.user.find_first(where={"name": user.name})
    await prisma.disconnect()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.name
