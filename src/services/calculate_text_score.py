import pandas as pd
import re
import spacy

from src.models.languages import Language
import nltk
from collections import Counter
from nltk.corpus import stopwords
import textstat  # For readability formulas
import syllapy

# Download necessary data for NLTK
nltk.download('punkt_tab')
nltk.download('stopwords')


# Function to calculate lexical complexity
def lexical_complexity(text: str, language: Language):
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words(language.name))

    # Remove stopwords and punctuation
    words = [word for word in words if word.isalnum() and word.lower() not in stop_words]

    tot_syll = sum(syllapy.count(word) for word in words)
    pol_syll_count = sum(syllapy.count(word) for word in words if syllapy.count(word) >= 3)

    total_words = len(words)
    avg_syllable = tot_syll / total_words

    unique_words = len(set(words))
    avg_word_length = sum(len(word) for word in words) / total_words

    word_length_over_six = sum(len(word) for word in words if len(word) > 6) / total_words
    one_syll_percentage = sum(syllapy.count(word) for word in words if syllapy.count(word) == 1)

    lexical_diversity = unique_words / total_words

    return {
        'word_count': total_words,
        'over_six_word': word_length_over_six,
        'one_syll': one_syll_percentage,
        'avg_syll': avg_syllable,
        'pol_syll': pol_syll_count,
        'tot_syllables': tot_syll,
        'unique_words': unique_words,
        'lexical_diversity': lexical_diversity,
        'avg_word_length': avg_word_length
    }


# Function to calculate syntactic complexity
def syntactic_complexity(text, language):
    doc = language.nlp(text)
    sentence_lengths = [len(sent) for sent in doc.sents]

    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)

    # Count subordinating conjunctions for measuring complex sentences
    subordination_count = sum(1 for token in doc if token.dep_ == 'mark')  # "mark" is the label for subordination
    sentence_count = len(list(doc.sents))

    return {
        'sentence_count': sentence_count,
        'avg_sentence_length': avg_sentence_length,
        'subordination_count': subordination_count
    }


# Function to calculate readability (cohesion and coherence)
def readability_metrics(text):
    # Using textstat for various readability formulas
    flesch_reading_ease = textstat.flesch_reading_ease(text)
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
    gunning_fog = textstat.gunning_fog(text)
    smog_index = textstat.smog_index(text)

    return {
        'flesch_reading_ease': flesch_reading_ease,
        'flesch_kincaid_grade': flesch_kincaid_grade,
        'gunning_fog': gunning_fog,
        'smog_index': smog_index}


def generate_overall_score(text: str, language: Language):
    text = text.replace("\n", " ")
    lex = lexical_complexity(text, language)
    syn = syntactic_complexity(text, language)
    read = readability_metrics(text)

    if language.name == 'english':

        # Weighted difficulty score (customizable)
        difficulty_score = (
                (lex['lexical_diversity']) * 0.15 +  # High diversity = lower difficulty
                (syn['avg_sentence_length'] / 25) * 0.05 +  # Normalize sentence length by a typical average (25)
                (syn['subordination_count'] / syn['sentence_count']) * 0.25 +
                (read['flesch_kincaid_grade'] / 12) * 0.55  # Normalize Flesch-Kincaid to a 12-grade scale
        )
    elif language.name == 'spanish':
        fer_huerta = 206.84 - (0.60 * lex['tot_syllables']) - 1.02 * lex['word_count']
        new_fer_huerta = (fer_huerta * -1 + 200) / 500
        difficulty_score = new_fer_huerta
    else: #for german
        wiener = 0.1935 * lex['pol_syll'] + 0.1672 * syn['avg_sentence_length'] + 0.1297 * lex[
            'over_six_word'] - 0.0327 * lex['one_syll'] - 0.875
        normalised_wiener = wiener / 40  # Normalize
        difficulty_score = (
                (lex['lexical_diversity']) * 0.15 +  # High diversity = lower difficulty
                (syn['avg_sentence_length'] / 25) * 0.05 +  # Normalize sentence length by a typical average (25)
                (syn['subordination_count'] / syn['sentence_count']) * 0.25 +
                normalised_wiener * 0.55
        )

    # Return individual metrics and an overall score
    return {
        'overall_difficulty_score': round(difficulty_score, 3)
    }


def get_sentences_from_text(text: str) -> list[str]:
    sentences = re.split(r'[.!?]+', text)
    return sentences


def get_words_from_text(text: str) -> list[str]:
    words = re.findall(r'\b\w+\b', text)
    return words


def count_difficult_words(words: list[str], language: Language) -> int:
    count = 0
    vocab = language.get_vocab()
    nlp = language.nlp
    for word in words:
        clean_word = word.strip(",.!?:\"").lower()
        lem_word = get_lemma_from_word(clean_word, nlp)

        if lem_word not in vocab:
            count += 1
    return count


def get_lemma_from_word(word: str, nlp: spacy.Language) -> str:
    doc = nlp(word)
    return [token.lemma_ for token in doc][0]


text = """Ciao! Mi chiamo Marco e ho trent'anni. Vivo a Milano, una grande città in Italia. Lavoro in un ristorante come chef. Mi piace cucinare e creare nuovi piatti. Ogni giorno, preparo il pranzo e la cena per i clienti. La mattina, vado al mercato per comprare ingredienti freschi. Adoro i pomodori, le zucchine e il pesce. Dopo il lavoro, a volte incontro gli amici per una birra o una pizza. Nel fine settimana, mi piace andare a visitare musei o fare una passeggiata nei parchi della città. A Milano ci sono molti eventi culturali e mostre d’arte. Che cosa ti piace fare nei weekend?"""
"""df = pd.read_excel('/Users/felixdahl/dev/text-generation-service/vocab/it_m3.xls', engine='xlrd')
filtered_df = df[df['Points'] == 'A1']
lemma_list = filtered_df['Lemma'].tolist()

dcrf = generate_dcrf_score(text, lemma_list)
print(dcrf)"""
