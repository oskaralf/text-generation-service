from fastapi import APIRouter, HTTPException
from prisma import Prisma

from src.models.sentences import SentenceHistoryRequest
from src.models.user import User
from src.models.languages import Language
from src.services.user_service import put_user_to_db, post_user_to_db
from src.services.user_service import get_sentence_from_openai
from src.services.calculate_text_score import generate_overall_score

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

    return {'language': user.language}


@router.post("/get-registration-sentence")
async def get_registration_sentence(request: SentenceHistoryRequest):
    sentence = await get_sentence_from_openai(request)

    return {"sentence": sentence}


from pydantic import BaseModel
class ScoreRequest(BaseModel):
    rating: int
    sentence: str
    user: str


@router.post("/set-initial-level")
async def initialise_score(request: ScoreRequest):
    await prisma.connect()
    user = await prisma.user.find_first(where={"name": request.user})

    sentence_score = generate_overall_score(request.sentence, Language(user.language))['overall_difficulty_score']
    user_level = (request.rating / 5) * sentence_score

    user = await prisma.user.update(where={"name": request.user}, data={'level': user_level})
    await prisma.disconnect()

    print('setting initial user level to:', user_level)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user_level