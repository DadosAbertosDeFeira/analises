import nltk
import spacy
from nltk.tokenize import word_tokenize

try:
    # se não tiver na máquina faz o download
    import pt_core_news_sm  # noqa
except:  # noqa
    from spacy.cli.download import download as spacy_download

    spacy_download("pt_core_news_sm")
nltk.download("punkt")
sp = spacy.load("pt_core_news_sm")


def remove_portuguese_stopwords(text, custom_stopwords=None):
    text = text.lower()
    all_stopwords = sp.Defaults.stop_words
    abc = [char for char in "abcdefghijklmnopqrstuvxyzw"]
    if not custom_stopwords:
        custom_stopwords = []
    aditional_stopwords = list(all_stopwords) + abc + custom_stopwords

    text_tokens = word_tokenize(text)
    return " ".join([word for word in text_tokens if word not in aditional_stopwords])
