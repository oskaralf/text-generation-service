from fastapi import APIRouter, HTTPException
from prisma import Prisma

from src.models.word import Word
from src.services.post_word_to_db import post_word_to_db

router = APIRouter()
prisma = Prisma()


@router.post("/save-word")
async def save_word(word: Word):
    success = await post_word_to_db(word)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save word")
    return success
