from nltk.corpus import stopwords
from scripts.stopwords import CUSTOM_STOPWORDS
import re
import unicodedata


def currency_to_float(value):
    """Converte de R$ 69.848,70 (str) para 69848.70 (float)."""
    try:
        cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
        return float(cleaned_value)
    except ValueError:
        return


def limpa_texto(text, remove_acentos=False, return_string=True) -> str or list:
    if type(text) == float:
        return ""

    # Remove pontuacao, digitos e espacos
    text = re.sub(r"[0-9]+", " NUM ", text.lower())
    text = " ".join(re.findall(r"\b[A-Za-zÀ-ú]+[-A-Za-zÀ-ú]*", text))

    # Remove acentos, cedilhas etc
    if remove_acentos:
        nfkd_form = unicodedata.normalize('NFKD', text)
        text = ''.join([char for char in nfkd_form if not unicodedata.combining(char)])

    # Remove stopwords
    nltk_stopwords = stopwords.words("portuguese")
    all_stopwords = nltk_stopwords + CUSTOM_STOPWORDS

    text = [word for word in text.split() if word not in all_stopwords]

    if return_string:
        return " ".join(text)
    else:
        return text
