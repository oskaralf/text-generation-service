from prisma import Prisma

from src.models.word import Word

prisma = Prisma()


async def post_word_to_db(word: Word):
    try:
        await prisma.connect()

        latest_text = await prisma.text.find_first(
            where={"userName": word.user},
            order={"date": "desc"},
        )

        new_word = await prisma.words.create(
            data={
                'word': word.word,
                'translation': word.translation,
                'language': word.language,
                'userName': word.user,
                'textId': latest_text.id,
            }
        )
        print(new_word)
        success = True
        await prisma.disconnect()
    except Exception as e:
        success = False
        print(e)
    return success

