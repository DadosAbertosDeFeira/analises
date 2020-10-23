import re
import unicodedata

from nltk.corpus import stopwords
from scripts.stopwords import CUSTOM_STOPWORDS


def currency_to_float(value):
    """Converte de R$ 69.848,70 (str) para 69848.70 (float)."""
    try:
        cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
        return float(cleaned_value)
    except ValueError:
        return


def remove_ponctuation(text):
    """
    Remove pontuação, dígitos e espaços em branco
    """

    if not isinstance(text, str):
        return ""

    text = re.sub(r"[0-9]+", " NUM ", text.lower())
    return " ".join(re.findall(r"\b[A-Za-zÀ-ú]+[-A-Za-zÀ-ú]*", text))


def remove_accents(text):
    """
    # Remove accents
    # TODO: Apparently this doesn't remove accents like "á", é" and so on.
    # Maybe it would be a good idea to remove those as well
    """

    if not isinstance(text, str):
        return ""

    nfkd_form = unicodedata.normalize("NFKD", text)
    return "".join([char for char in nfkd_form if not unicodedata.combining(char)])


def remove_stopwords(text):
    if not isinstance(text, str):
        return ""

    nltk_stopwords = stopwords.words("portuguese")
    all_stopwords = nltk_stopwords + CUSTOM_STOPWORDS

    text = [word for word in text.split() if word not in all_stopwords]
    return " ".join(text)


def clean_text(text, remove_accents=False) -> str:
    if not isinstance(text, str):
        return ""

    text = remove_ponctuation(text)
    if remove_accents:
        text = remove_accents(text)
    return remove_stopwords(text)
