from pydantic import BaseModel


class Word(BaseModel):
    word: str
    translation: str
    language: str
    user: str
