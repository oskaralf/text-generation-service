from dotenv import load_dotenv
import os
import openai
from prisma import Prisma
import pandas as pd

from src.services.dcrf import generate_dcrf_score
from src.models.languages import Language

prisma = Prisma()

assistant_text = ("You are a helpful assistant for people learning a new language."
                  "You will help them practice their reading skills by generating texts "
                  "based on their interests, language level, and the specific context and type of the text output."
                  "Please adapt the length of the text according to the level of the user,"
                  "i.e. shorter texts for beginners and longer texts for more advanced learners."
                  "The level is measured as the DCRF score, which is based on the percentage of difficult words and the average sentence length.")


def generate_prompt(user, context: str, text_type: str) -> str:
    language = user.language
    interests = user.interests.split(",")
    level = user.level

    prompt = (f"Language: {language}\n"
              f"Level: {level}\n"
              f"Interests: {interests}\n"
              f"Context: {context}\n"
              f"Text type: {text_type}\n")

    return prompt


def get_text_from_openai(messages: list) -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200
    )
    text = response.choices[0].message.content
    print("GENERATED TEXT:")
    print(text)
    return text


async def get_text_for_user(user: str, context: str, text_type: str) -> str:
    await prisma.connect()
    user = await prisma.user.find_unique(where={"name": user})
    await prisma.disconnect()
    language = Language(user.language)

    prompt = generate_prompt(user, context, text_type)
    messages = [
        {"role": "system", "content": assistant_text},
        {"role": "user", "content": prompt}
    ]
    text = get_text_from_openai(messages)
    messages.append({"role": "assistant", "content": text})
    dcrf_score = generate_dcrf_score(text, language)
    """
    while abs(dcrf_score - user.level) > 1:
        if dcrf_score - user.level > 1:
            messages.append({"role": "user", "content": f"The text is too difficult for the user, it scored a DCRF score of {dcrf_score} while the user needs {user.level}. Can you make the text a bit easier?"})
        elif dcrf_score - user.level < -1:
            messages.append({"role": "user", "content": f"The text is too easy for for the user, it scored a DCRF score of {dcrf_score} while the users needs {user.level}. Can you make the text a bit more challenging?"})
        text = get_text_from_openai(messages)
        dcrf_score = generate_dcrf_score(text, language)
    """

    return text
