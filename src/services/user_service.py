from prisma import Prisma
from src.models.user import User

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
        await prisma.disconnect()
    except Exception:
        success = False
    return success
