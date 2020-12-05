import pytest
from scripts.nlp import remove_portuguese_stopwords


@pytest.mark.parametrize(
    "text,expected_text",
    [
        ("GILBERTO REIS FILHO DE JÚ", "gilberto reis filho jú"),
        ("A casa dela é bela", "casa dela bela"),
        ("A de da e", ""),
    ],
)
def test_remove_stop_words(text, expected_text):
    assert remove_portuguese_stopwords(text) == expected_text


def test_remove_stop_words_with_custom_stop_words():
    text = "GILBERTO REIS FILHO DE JÚ"
    expected_text = "gilberto reis jú"
    custom_stopwords = ["filho"]
    assert remove_portuguese_stopwords(text, custom_stopwords) == expected_text
