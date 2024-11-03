from fastapi import APIRouter, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from src.models.word import Word
from src.models.user import User

router = APIRouter()
prisma = Prisma()


