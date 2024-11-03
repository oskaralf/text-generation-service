from prisma import Prisma

from src.models.word import Word

prisma = Prisma()


async def post_word_to_db(word: Word):
    try:
        await prisma.connect()
        new_word = await prisma.words.create(
            data={
                'word': word.word,
                'translation': word.translation,
                'language': word.language,
                'userName': word.user
            }
        )
        print(new_word)
        success = True
        await prisma.disconnect()
    except Exception:
        success = False
    return success

