from fastapi import APIRouter
from prisma import Prisma

from src.models.languages import Language
from src.services.get_text_for_user import get_text_for_user
from src.services.get_contexts_for_user import get_contexts_for_user
from src.services.get_text_types_for_user import get_text_types_from_context
from src.services.get_calibration_text import get_calibration_text


router = APIRouter()
prisma = Prisma()


@router.get("/generate_text")
async def generate_text(user: str, context: str, text_type: str):
    text = await get_text_for_user(user, context, text_type)
    return text


@router.get("/generate_contexts")
async def generate_contexts(user: str):
    contexts = await get_contexts_for_user(user)
    return contexts


@router.get("/generate_text_types")
async def generate_text_types(context: str):
    text_types = await get_text_types_from_context(context)
    return text_types


@router.get("/generate-calibration-text")
async def generate_calibration_text():
    text = await get_calibration_text()
    return text