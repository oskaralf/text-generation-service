from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    name: str
    language: Optional[str] = None
    level: Optional[float] = None
    interests: Optional[str] = None
