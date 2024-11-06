from typing import List
from pydantic import BaseModel


class SentenceEntry(BaseModel):
    sentence: str
    rating: int


class SentenceHistoryRequest(BaseModel):
    sentenceHistory: List[SentenceEntry]