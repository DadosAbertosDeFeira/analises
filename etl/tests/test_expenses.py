from etl.expenses import identify_code_and_description, extract_classification
import pytest


@pytest.mark.parametrize('row,expected_description',[
    (
        ['3', '0', '00', '00', '00', '3.0.00.00.00', '3.0.00.00.00', 'Despesas Correntes'],
        {
            'value': '3',
            'group': 'CO',
            'code': '3.0.00.00.00',
            'description': 'Despesas Correntes'
        }
    ),
    (
        ['3', '1', '00', '00', '00', '3.1.00.00.00', '3.0.00.00.00', 'Pessoal e Encargos Sociais'],
        {
            'value': '1',
            'group': 'GD',
            'code': '3.1.00.00.00',
            'description': 'Pessoal e Encargos Sociais'
        }
    ),
    (
        ['3', '1', '71', '00', '00', '3.1.71.00.00', '3.0.00.00.00', 'Transferências a Consórcios Públicos Mediante Contrato de Rateio'],
        {
            'value': '71',
            'group': 'MA',
            'code': '3.1.71.00.00',
            'description': 'Transferências a Consórcios Públicos Mediante Contrato de Rateio'
        }
    ),
    (
        ['3', '1', '71', '70', '00', '3.1.71.70.00', '3.0.00.00.00', 'Rateio pela Participação em Consórcio Público'],
        {
            'value': '70',
            'group': 'ED',
            'code': '3.1.71.70.00',
            'description': 'Rateio pela Participação em Consórcio Público'
        }
    ),
    (
        ['3', '1', '90', '01', '01', '3.1.90.01.01', '3.0.00.00.00', 'Aposentadorias Custeadas com Recursos do RPPS'],
        {
            'value': '01',
            'group': 'SED',
            'code': '3.1.90.01.01',
            'description': 'Aposentadorias Custeadas com Recursos do RPPS'
        }
    ),
    ([], None),
    (None, None),
    (['3', '1', '90'], None)
])
def test_identify_code_and_description(row, expected_description):
    assert identify_code_and_description(row) == expected_description


def test_extract_classification_from_text():
    text = "339030040000000000 - Medicamentos"

    assert extract_classification(text) == "33903004"


def test_return_none_if_extract_classification_is_not_found():
    text = "Medicamentos31938 1830183"

    assert extract_classification(text) is None
