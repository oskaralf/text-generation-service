import json
from prisma import Prisma

from src.services.get_text_for_user import get_text_from_openai

prisma = Prisma()

assistant_text = ("You are a helpful assistant for people learning a new language."
                  "You will help come up with creative contexts/topics for texts "
                  "that are tailored to specific interests and language levels. Some should be more tailored to the interests"
                  "and some should be more tailored to the language level, i.e. a beginner might need to learn asking for directions"
                  "or describing objects. "
                  "I will provide you a list of interests and a language level from 0-10, "
                  "where 0 is an absolut beginner and 10 is a native speaker. "
                  "I want you to generate a list of contexts/topics for texts that i can later use to generate texts "
                  "based on the users interests. "
                  "Please only answer with a list of contexts/topics separated with commas and absolutely nothing else: "
                  "No more than 8 contexts are allowed. Keep the contexts short."
                  "Example: Ordering food at restaurant, Asking for directions, At a baseball game, math concepts, music ...")


async def get_contexts_for_user(user: str):
    await prisma.connect()
    user = await prisma.user.find_unique(where={"name": user})
    await prisma.disconnect()
    interests = user.interests.split(",")

    messages = [
        {"role": "system", "content": assistant_text},
        {"role": "user", "content": f"Interests: {interests}\nLevel: 2.0"}
    ]

    generated_contexts = get_text_from_openai(messages)
    generated_contexts = generated_contexts.split(',')
    print(generated_contexts)
    return generated_contexts
