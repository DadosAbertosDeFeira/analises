import pytest
from scripts.parsers import currency_to_float, limpa_proc_licitatorio


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
    "proc_licitatorio_sujo,proc_licitatorio_limpo",
    [
        ("ISENTO", "isento"),
        ("ENTO", "isento"),
        ("Isento", "isento"),
        ("SENTO", "isento"),
        ("sento", "isento"),
        ("PREGAO", "pregao"),
        ("REGAO", "pregao"),
        ("Pregao", "pregao"),
        ("EGAO", "pregao"),
        ("egao", "pregao"),
        ("DISPENSA", "dispensa"),
        ("SPENSA", "dispensa"),
        ("ISPENSA", "dispensa"),
        ("Dispensa", "dispensa"),
        ("PENSA", "dispensa"),
        ("pensa", "dispensa"),
        ("CONCORENCIA", "concorrencia"),
        ("ONCORRENCIA", "concorrencia"),
        ("NCORRENCIA", "concorrencia"),
        ("INEXIGIBILIDADE", "inexigibilidade"),
        ("NEXIGIBILIDADE", "inexigibilidade"),
        ("Inexibilidade", "inexigibilidade"),
        ("XIGIBILIDADE", "inexigibilidade"),
        ("xigibilidade", "inexigibilidade"),
        ("EXIGIBILIDADE", "inexigibilidade"),
        ("exigibilidade", "inexigibilidade"),
        ("TOMADA DE PRECO", "tomada de preco"),
        ("OMADA DE PRECO", "tomada de preco"),
        ("omada de preco", "tomada de preco"),
    ],
)
def test_limpa_proc_licitatorio(proc_licitatorio_sujo, proc_licitatorio_limpo):
    assert limpa_proc_licitatorio(proc_licitatorio_sujo) == proc_licitatorio_limpo
