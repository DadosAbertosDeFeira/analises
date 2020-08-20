from scripts.parsers import currency_to_float, limpa_texto
import pytest


@pytest.mark.parametrize(
    "original_value,expected_value",
    [
        ("R$ 69.848,70", 69848.70),
        ("69.848,70", 69848.70),
        ("R$ -69.848,70", -69848.70),
        ("1,70", 1.70),
        ("00,00", 0),
        ("Random", None),
    ],
)
def test_currency_to_float(original_value, expected_value):
    assert currency_to_float(original_value) == expected_value


@pytest.mark.parametrize(
    "texto,texto_limpo",
    [
        ("Guarda-chuva", "guarda-chuva"),
        ("123abraço", "NUM abraço"),
        ("123oliveira4", "NUM oliveira NUM"),
        ("Onde.Vai", "onde vai"),
        ("AteNÇÃo", "atenção"),
        ("Qualquer uma destas xx casas", "casas"),
        ("Pé-De-Moleque", "pé-de-moleque"),
        ("________", ""),
        ("anexo______", "anexo"),
    ],
)
def test_limpa_texto(texto, texto_limpo):
    assert limpa_texto(texto) == texto_limpo
