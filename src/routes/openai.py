from fastapi import APIRouter
from prisma import Prisma

from src.models.languages import Language
from src.services.generate_text import generate_text

router = APIRouter()
prisma = Prisma()


@router.get("/generate")
async def generate(user: str, context: str, text_type: str):
    text = await generate_text(user, context, text_type)
    return text
