from prisma import Prisma
from src.models.user import User
from src.services.get_text_for_user import get_text_from_openai
from src.models.sentences import SentenceHistoryRequest


prisma = Prisma()


async def put_user_to_db(user: User):
    try:
        updated_user = await prisma.user.update(where={"name": user.name}, data={'level': user.level})
        success = True
    except Exception:
        success = False
    return success


async def post_user_to_db(user: User):
    await prisma.connect()
    try:
        new_user = await prisma.user.create(data={
            'name': user.name,
            'language': user.language,
            'interests': user.interests
        })
        success = True
    except Exception:
        success = False

    await prisma.disconnect()
    return success

assistant_text = ('You are an expert at generating texts for users in a language which they are trying to learn. '
                  'You are going to generate texts in order to assess a users overall level. The texts should be two sentences. '
                  'I am going to provide a text, and the difficulty rating from a user on that sentence, '
                  'on a 1-5 scale, 1 being "i dont understand anything" and 5 being "i understand everything". '
                  'In turn, you are going to provide a new text which is aimed at suiting the level of the user by increasing or decreasing the text. '
                  'Hence a 1 means that you need to decrease the difficulty by a lot, and a 5 means you need to increase difficulty by a lot. '
                  'Only respond with the new text. The text should not be a variation of the previous text, come up with something new each time.')


async def get_sentence_from_openai(request: SentenceHistoryRequest):
    sentences = request.sentenceHistory
    messages = [
        {"role": "system", "content": assistant_text}
    ]

    for i in range(len(sentences)-1):
        messages.append({"role": "user", "content": f"Sentence: {sentences[i].sentence}\nRating: {sentences[i].rating}"})
        messages.append({"role": "assistant", "content": f"{request.sentenceHistory[i+1].sentence}"})

    messages.append({"role": "user", "content": f"Sentence: {sentences[-1].sentence}\nRating: {sentences[-1].rating}"})

    generated_sentence = get_text_from_openai(messages)
    return generated_sentence


