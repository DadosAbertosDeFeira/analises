import nltk
from nltk.corpus import stopwords
import re

# import unicodedata


def currency_to_float(value):
    """Converte de R$ 69.848,70 (str) para 69848.70 (float)."""
    try:
        cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
        return float(cleaned_value)
    except ValueError:
        return


def limpa_texto(text, return_string=True) -> str or list:
    if type(text) == float:
        return ""

    # Remove pontuacao, digitos e espacos
    text = re.sub(r"[0-9]+", " NUM ", text.lower())
    text = " ".join(re.findall(r"\b[A-Za-zÀ-ú]+[-A-Za-zÀ-ú]*", text))

    # Remove acentos, cedilhas etc
    # nfkd_form = unicodedata.normalize('NFKD', text)
    # text = ''.join([char for char in nfkd_form if not unicodedata.combining(char)])

    # Remove stopwords
    my_stopwords = stopwords.words("portuguese")
    with open("stopwords.txt") as f:
        my_words = f.read().split()
    my_stopwords = my_stopwords + my_words

    text = [word for word in text.split() if word not in my_stopwords]

    if return_string:
        return " ".join(text)
    else:
        return text
