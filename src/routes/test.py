from fastapi import APIRouter
from prisma import Prisma
from prisma.models import User

router = APIRouter()
prisma = Prisma()


@router.get("/ping")
async def test():
    return {"msg": "pong"}


@router.get("/test/get_users")
async def test_prisma():
    await prisma.connect()
    user = await prisma.user.find_unique(where={"name": "anders"}, include={"savedWords": True, "history": True})
    print([word.word for word in user.savedWords])

    await prisma.disconnect()
    return user


@router.post("/test/create_user")
async def create_user():
    await prisma.connect()

    user = await prisma.user.create(data={"name": "dessan",
                                   "level": 0.3,
                                   "language": "english",
                                   "interests": "baking, hiking, knitting, travelling"})

    await prisma.disconnect()
    return user


@router.delete("/test/delete_user")
async def delete_user():
    await prisma.connect()

    user = await prisma.user.delete(where={"name": "oskar"})

    await prisma.disconnect()
    return user
