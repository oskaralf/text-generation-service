from abc import ABC, abstractmethod
from enum import Enum
import spacy


class Language:
    def __init__(self, name: str):
        self.name = LanguageName(name)
        self.nlp_code = getattr(NLPCode, self.name.value.upper())
        self.nlp = self.get_nlp()

    def get_nlp(self):
        return spacy.load(self.nlp_code.value)

    def __str__(self):
        return self.name.value


class NLPCode(Enum):
    ITALIAN = 'it_core_news_sm'
    ENGLISH = 'en_core_web_sm'


class LanguageName(Enum):
    ITALIAN = 'italian'
    ENGLISH = 'english'
