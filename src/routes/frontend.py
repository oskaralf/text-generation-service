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

class UserProfileEntry(BaseModel):
    userName: str
    language: str
    level: float
    interests: str

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

@router.post("/save-user")
async def save_user_profile(entry: UserProfileEntry):
    try:
        await prisma.connect()
        existing_user = await prisma.user.find_unique(where={"name": entry.userName})
        
        if existing_user:
            updated_user = await prisma.user.update(
                where={"name": entry.userName},
                data={
                    'language': entry.language,
                    'level': entry.level,
                    'interests': entry.interests
                }
            )
            return {"success": True, "id": updated_user.id}
        else:
            new_user = await prisma.user.create(
                data={
                    'name': entry.userName,
                    'language': entry.language,
                    'level': entry.level,
                    'interests': entry.interests 
                }
            )
            return {"success": True, "id": new_user.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save user profile")
    finally:
        await prisma.disconnect()
