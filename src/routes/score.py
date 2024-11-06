from fastapi import APIRouter
from prisma import Prisma

from src.services.score_service import update_user_level
from src.models.user import User

router = APIRouter()


@router.post("/update-score")
async def update_score(user: User):
    print(user.name)
    old_level, new_average_level = await update_user_level(user.name)
    print({"old_level": old_level, "new_average_level": new_average_level})
    return {"old_level": old_level, "new_average_level": new_average_level}
