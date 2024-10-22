from fastapi import APIRouter, HTTPException
from prisma import Prisma
from pydantic import BaseModel

router = APIRouter()
prisma = Prisma()

class WordEntry(BaseModel):
    word: str
    translation: str
    language: str
    userName: str

@router.post("/save-word")
async def save_word(entry: WordEntry):
    try:
        await prisma.connect()
        new_word = await prisma.words.create(
            data={
                'word': entry.word,
                'translation': entry.translation,
                'language': entry.language,
                'userName': entry.userName
            }
        )
        await prisma.disconnect()
        return {"success": True, "id": new_word.id}
    except Exception as e:
        await prisma.disconnect()
        raise HTTPException(status_code=500, detail="Failed to save word")
