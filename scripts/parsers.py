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


def clean_text(text, remove_accents=False, return_string=True) -> str or list:
    if isinstance(type(text), float):
        return ""

    # Remove ponctuation, digits and whitespaces
    text = re.sub(r"[0-9]+", " NUM ", text.lower())
    text = " ".join(re.findall(r"\b[A-Za-zÀ-ú]+[-A-Za-zÀ-ú]*", text))

    # Remove accents
    if remove_accents:
        nfkd_form = unicodedata.normalize("NFKD", text)
        text = "".join([char for char in nfkd_form if not unicodedata.combining(char)])

    # Remove stopwords
    nltk_stopwords = stopwords.words("portuguese")
    all_stopwords = nltk_stopwords + CUSTOM_STOPWORDS

    text = [word for word in text.split() if word not in all_stopwords]

    if return_string:
        return " ".join(text)
    else:
        return text
