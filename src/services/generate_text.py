from dotenv import load_dotenv
import os
import openai
from prisma import Prisma
import pandas as pd

from src.services.dcrf import generate_dcrf_score

prisma = Prisma()

assistant_text = ("You are a helpful assistant for people learning a new language."
                  "You will help them practice their reading skills by generating texts "
                  "based on their interests, language level, and the specific context and type of the text output."
                  "Please adapt the length of the text according to the level of the user,"
                  "i.e. shorter texts for beginners and longer texts for more advanced learners."
                  "The level is a float between 0.0 and 10.0, where 0.0 means the user speaks absolutely and 10.0 is fluent.")


def generate_prompt(user, context: str, text_type: str) -> str:
    language = user.language
    interests = user.interests.split(",")
    level = user.level

    prompt = (f"Language: {language}\n"
              f"Level: 1.0"
              f"Interests: {interests}\n"
              f"Context: {context}\n"
              f"Text type: {text_type}\n")

    return prompt


def retrieve_text(prompt: str) -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": assistant_text},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )
    text = response.choices[0].message.content
    print("GENERATED TEXT:")
    print(text)
    return text


async def generate_text(user: str, context: str, text_type: str) -> str:
    await prisma.connect()
    user = await prisma.user.find_unique(where={"name": user})
    await prisma.disconnect()

    prompt = generate_prompt(user, context, text_type)
    text = retrieve_text(prompt)

    df = pd.read_excel('/Users/felixdahl/dev/text-generation-service/vocab/en_m3.xls', engine='xlrd')
    filtered_df = df[df['CEFR'].isin(['"A1"', '"A2"'])]
    lemma_list = filtered_df['Word'].tolist()
    dcrf_score = generate_dcrf_score(text, lemma_list)
    print('DCRF score:', dcrf_score)
    return text
