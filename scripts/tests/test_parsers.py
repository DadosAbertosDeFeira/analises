import pytest
from scripts.parsers import clean_bidding_process, currency_to_float


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
    "bidding_process,expected_bidding_process",
    [
        ("isento", "isento"),
        ("ENTO", "isento"),
        ("SENTO", "isento"),
        ("pregao", "pregao"),
        ("REGAO", "pregao"),
        ("EGAO", "pregao"),
        ("dispensa", "dispensa"),
        ("SPENSA", "dispensa"),
        ("ISPENSA", "dispensa"),
        ("PENSA", "dispensa"),
        ("CONCORENCIA", "concorrencia"),
        ("ONCORRENCIA", "concorrencia"),
        ("NCORRENCIA", "concorrencia"),
        ("INEXIGIBILIDADE", "inexigibilidade"),
        ("NEXIGIBILIDADE", "inexigibilidade"),
        ("Inexibilidade", "inexigibilidade"),
        ("XIGIBILIDADE", "inexigibilidade"),
        ("EXIGIBILIDADE", "inexigibilidade"),
        ("TOMADA DE PRECO", "tomada de preco"),
        ("OMADA DE PRECO", "tomada de preco"),
        ("omada de preco", "tomada de preco"),
    ],
)
def test_clean_bidding_process(bidding_process, expected_bidding_process):
    assert clean_bidding_process(bidding_process) == expected_bidding_process
