import pytest
from scripts.parsers import (
    all_expenses_nature_from_tcmba,
    currency_to_float,
    extract_nature,
    identify_code_and_description,
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
    "row,expected_description",
    [
        (
            [
                "3",
                "0",
                "00",
                "00",
                "00",
                "3.0.00.00.00",
                "3.0.00.00.00",
                "Despesas Correntes",
            ],
            {
                "value": "3",
                "group": "CO",
                "code": "3.0.00.00.00",
                "description": "Despesas Correntes",
            },
        ),
        (
            [
                "3",
                "1",
                "00",
                "00",
                "00",
                "3.1.00.00.00",
                "3.0.00.00.00",
                "Pessoal e Encargos Sociais",
            ],
            {
                "value": "1",
                "group": "GD",
                "code": "3.1.00.00.00",
                "description": "Pessoal e Encargos Sociais",
            },
        ),
        (
            [
                "3",
                "1",
                "71",
                "00",
                "00",
                "3.1.71.00.00",
                "3.0.00.00.00",
                "Transferências a Consórcios Públicos Mediante Contrato de Rateio",
            ],
            {
                "value": "71",
                "group": "MA",
                "code": "3.1.71.00.00",
                "description": "Transferências a Consórcios Públicos "
                "Mediante Contrato de Rateio",
            },
        ),
        (
            [
                "3",
                "1",
                "71",
                "70",
                "00",
                "3.1.71.70.00",
                "3.0.00.00.00",
                "Rateio pela Participação em Consórcio Público",
            ],
            {
                "value": "70",
                "group": "ED",
                "code": "3.1.71.70.00",
                "description": "Rateio pela Participação em Consórcio Público",
            },
        ),
        (
            [
                "3",
                "1",
                "90",
                "01",
                "01",
                "3.1.90.01.01",
                "3.0.00.00.00",
                "Aposentadorias Custeadas com Recursos do RPPS",
            ],
            {
                "value": "01",
                "group": "SED",
                "code": "3.1.90.01.01",
                "description": "Aposentadorias Custeadas com Recursos do RPPS",
            },
        ),
        ([], None),
        (None, None),
        (["3", "1", "90"], None),
    ],
)
def test_identify_code_and_description(row, expected_description):
    assert identify_code_and_description(row) == expected_description


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
