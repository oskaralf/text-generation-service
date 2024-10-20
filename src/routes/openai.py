from fastapi import APIRouter
from prisma import Prisma

from src.models.languages import Language
from src.services.generate_text import generate_text

router = APIRouter()
prisma = Prisma()


@router.get("/generate_text")
async def generate_text(user: str, context: str):
    text = await generate_text(user, context)
    return text


def generate_text():
    prompt = build_prompt()


def build_prompt(dcrf_score: float, target_language: Language, familiar_words: list[str], new_words: list[str], cefr: str, theme: str):
    prompt = (
        f"Write a story based on the CEFR level {cefr} and in langugae {target_language} using the following words: "
        + ", ".join(familiar_words)
        + ". Additionally, include these new or more difficult words: "
        + ", ".join(new_words)
        + ". The text should be understandable for a language learner who knows basic words but is learning more complex ones. "
        + f"The theme of the story should be {theme}."
    )
    return prompt