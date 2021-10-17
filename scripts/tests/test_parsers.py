import pytest
from scripts.parsers import (
    all_expenses_nature_from_tcmba,
    currency_to_float,
    extract_nature,
    is_company,
)


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
    "nature_str,expected_nature",
    [
        ("339030040000000000 - Medicamentos", "33903004"),
        ("339030120000000000 - Genero Alimenticios - Outros", "33903012"),
        ("339039140000 - Aquisiçao de Vale-Transporte", "33903914"),
        ("3.0.00.00.00", "30000000"),
        ("3.1.90.01.01", "31900101"),
    ],
)
def test_extract_nature(nature_str, expected_nature):
    assert extract_nature(nature_str) == expected_nature


@pytest.mark.parametrize(
    "year,nature,expected_size,expected_data",
    [
        (
            None,
            "30000000",
            2484,
            {
                "code": "30000000",
                "description": "Despesas Correntes",
                "superior_group_code": None,
            },
        ),
        (
            2020,
            "99999999",
            2484,
            {
                "code": "99999999",
                "description": "Reserva de Contingência",
                "superior_group_code": "99999900",
            },
        ),
        (
            2019,
            "99999999",
            2484,
            {
                "code": "99999999",
                "description": "Reserva de Contingência",
                "superior_group_code": "99999900",
            },
        ),
        (
            2018,
            "99999999",
            2175,
            {
                "code": "99999999",
                "description": "Reserva de Contingência",
                "superior_group_code": "99999900",
            },
        ),
    ],
)
def test_all_expenses_nature_from_tcmba(year, nature, expected_size, expected_data):
    expenses_nature = all_expenses_nature_from_tcmba(year)

    assert len(expenses_nature) == expected_size
    assert expenses_nature.get(nature) == expected_data


@pytest.mark.parametrize(
    "original_value,expected_value",
    [
        ("88888888888", False),
        ("99999999999999", True),
        ("888.888.888-88", False),
        ("99.999.999/9999-99", True),
        ("000", None),
        (99999999999999, True),
        (88888888888, False),
        (123456, None),
    ],
)
def test_is_company(original_value, expected_value):
    assert is_company(original_value) == expected_value
