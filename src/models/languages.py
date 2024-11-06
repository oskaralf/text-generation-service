from abc import ABC, abstractmethod
from enum import Enum
import spacy
import pandas as pd


language_to_nlp = {
    'italian': 'it_core_news_sm',
    'english': 'en_core_web_sm',
    'spanish': 'es_core_news_sm'
}

language_to_file = {
    'italian': 'it_m3.xls',
    'english': 'en_m3.xls',
}


class Language:
    def __init__(self, name: str):
        self.name = name
        self.nlp_code = language_to_nlp.get(name)
        self.nlp = self.get_nlp()

    def get_nlp(self):
        return spacy.load(self.nlp_code)

    def get_vocab(self):
        df = pd.read_excel(f'vocab/{language_to_file.get(self.name)}', engine='xlrd')
        filtered_df = df[df['CEFR'].isin(['A1'])]
        vocab = filtered_df['Word'].tolist()
        return vocab

    def __str__(self):
        return self.name
