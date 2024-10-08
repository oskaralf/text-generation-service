import openai
from dotenv import load_dotenv
import os

from src.models.languages import Language

load_dotenv()
api_key = os.getenv("OPENAI_API")


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