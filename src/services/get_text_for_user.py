from dotenv import load_dotenv
import os
import openai
from prisma import Prisma
import pandas as pd
from datetime import datetime

from src.services.calculate_text_score import generate_overall_score
from src.models.languages import Language

prisma = Prisma()

"""
assistant_text = ("You are a helpful assistant for people learning a new language."
                  "You will help them practice their reading skills by generating texts "
                  "based on their interests, language level, and the specific context and type of the text output."
                  "Please adapt the length of the text according to the level of the user,"
                  "i.e. shorter texts for beginners and longer texts for more advanced learners."
                  "The level is measured as the DCRF score, which is based on the percentage of difficult words and the average sentence length.")
"""
assistant_text = ("You are a expert linguistic coach for people learning a new language."
                  "You will help them practice their reading skills by generating texts in a specified language "
                  "based on their interests, language level, and the specific context and type of the text output."
                  "Please adapt the length of the text according to the level of the user,"
                  "i.e. shorter texts for beginners and longer texts for more advanced learners."
                  "The level is a value between 0 and 1. Assume that 0 is absolute beginner and 1 is a native speaker.")

english_assistant_text = ("The level is measured based on lexical diversity (unique words/ total words), "
                          "normalized flesch kincaid grade, subordinate count/sentence count and finally normalized "
                          "average sentence length. The formula is as follows: "
                          "difficulty score = flesch_kincaid_grade/ 12) * 0.4 + (1 - lexical diversity) * 0.3 + subordination count/sentence count * 0.25 + average sentence length/ 25 * 0.05. ")

spanish_assistant_text = ("The level is measured based on sentence length and syllable count per word in the text."
                          "The formula is as follows: 206.84 - (0.6 * syllable count) - 1.02 * word count. ")

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
        max_tokens=300
    )
    text = response.choices[0].message.content
    print("GENERATED TEXT:")
    print(text)
    return text


async def get_text_for_user(user: str, context: str, text_type: str) -> str:
    await prisma.connect()
    user = await prisma.user.find_unique(where={"name": user}, include={"savedWords": True})
    await prisma.disconnect()
    language = Language(user.language)

    user_words = [word.word for word in user.savedWords]
    additional_words_query = (f"These are words that the user has saved in the past for repetition,"
                              f"please include a small selection of these words if possible without"
                              f" without ruining the context of the text {', '.join(user_words)}")

    prompt = generate_prompt(user, context, text_type)
    print(assistant_text + additional_words_query)

    if user.language == "english":
        formula = english_assistant_text
    else:
        formula = spanish_assistant_text


    messages = [
        {"role": "system", "content": assistant_text + formula + additional_words_query},
        {"role": "user", "content": prompt}
    ]
    text = get_text_from_openai(messages)

    messages.append({"role": "assistant", "content": text})
    overall_score = generate_overall_score(text, language)["overall_difficulty_score"]
    best_text = []
    best_text.append(overall_score)
    best_text.append(text)

    count = 0
    print("start to find text")

    # FIXA us_level till user-level!!
    us_level = user.level
    degree = ["slightly", "a bit", "much"]
    while abs(overall_score - us_level) > 0.025 and count < 5:
        count += 1
        if overall_score - us_level > 0.025:
            messages.append({"role": "user",
                             "content": f"The text is too difficult for the user, it scored an overall score of {overall_score} while the user needs {us_level}. Can you make the text easier?"})
        elif overall_score - us_level < -0.025:
            messages.append({"role": "user",
                             "content": f"The text is too easy for the user, it scored an overall score of {overall_score} while the users needs {us_level}. Can you make the text more difficult?"})
        text = get_text_from_openai(messages)
        overall_score = generate_overall_score(text, language)["overall_difficulty_score"]

        if abs(overall_score - us_level) < abs(best_text[0] - us_level):
            best_text.clear()
            best_text.append(overall_score)
            best_text.append(text)
        print(overall_score)
    print("found text", best_text[1])
    score_of_text = best_text[0]
    print("with score:", score_of_text)

    length_of_text = len(best_text[1].split())

    await prisma.connect()
    user = await prisma.text.create(data={
        "language": user.language,
        "content": best_text[1],
        "totalWords": length_of_text,
        "level": score_of_text,
        "userName": user.name,
    })
    await prisma.disconnect()

    return best_text[1]
