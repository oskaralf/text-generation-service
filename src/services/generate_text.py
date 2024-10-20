from prisma import Prisma

prisma = Prisma()


async def generate_text(user: str, context: str):
    await prisma.connect()
    interests = await prisma.interest.find_many(where={"user": user})
    language = await



