import pandas as pd
import re
import spacy

from src.models.languages import Language


def generate_dcrf_score(text: str, vocab: list[str], language: Language) -> float:
    sentences = get_sentences_from_text(text)
    words = get_words_from_text(text)

    difficult_word_count = count_difficult_words(words, vocab, language)
    total_words = len(words)
    total_sentences = len(sentences)

    dcrf_score = 0.1579 * (difficult_word_count / total_words * 100) + 0.0496 * (total_words / total_sentences)
    return dcrf_score


def get_sentences_from_text(text: str) -> list[str]:
    sentences = re.split(r'[.!?]+', text)
    return sentences


def get_words_from_text(text: str) -> list[str]:
    words = re.findall(r'\b\w+\b', text)
    return words


def count_difficult_words(words: list[str], vocab, language: Language) -> int:
    count = 0

    for word in words:
        clean_word = word.strip(",.!?\"'").lower()
        lem_word = get_lemma_from_word(clean_word, language.nlp)
        if lem_word not in vocab:
            count += 1
    return count


def get_lemma_from_word(word: str, nlp: spacy.Language) -> str:
    doc = nlp(word)
    return [token.lemma_ for token in doc][0]


text = """Ciao! Mi chiamo Marco e ho trent'anni. Vivo a Milano, una grande città in Italia. Lavoro in un ristorante come chef. Mi piace cucinare e creare nuovi piatti. Ogni giorno, preparo il pranzo e la cena per i clienti. La mattina, vado al mercato per comprare ingredienti freschi. Adoro i pomodori, le zucchine e il pesce. Dopo il lavoro, a volte incontro gli amici per una birra o una pizza. Nel fine settimana, mi piace andare a visitare musei o fare una passeggiata nei parchi della città. A Milano ci sono molti eventi culturali e mostre d’arte. Che cosa ti piace fare nei weekend?"""
df = pd.read_excel('/Users/felixdahl/dev/text-generation-service/vocab/it_m3.xls', engine='xlrd')
filtered_df = df[df['Points'] == 'A1']
lemma_list = filtered_df['Lemma'].tolist()

dcrf = generate_dcrf_score(text, lemma_list)
print(dcrf)
