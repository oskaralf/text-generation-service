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

    users = await prisma.user.find_many()

    await prisma.disconnect()
    return users


@router.post("/test/create_user")
async def create_user():
    await prisma.connect()

    user = await prisma.user.create(data={"name": "Felix"})

    await prisma.disconnect()
    return user
