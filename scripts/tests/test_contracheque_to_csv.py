import pandas as pd

from scripts.contracheque_to_csv import (
    get_filepath_attributes,
    transform_df,
)


def test_correct_atts_filepath():
    expected = ("2019", "05", "prefeitura")
    path = "User/name/test/2019_05_prefeitura.xls"
    assert expected == get_filepath_attributes(path)


def test_change_columns_case():
    df = pd.DataFrame(
        {
            "Salário Base": ["R$ 2,00"],
            "Salário Vantagens": ["R$ 2,00"],
            "Salário Gratificação": ["R$ 2,00"],
        }
    )
    new_df = transform_df(df)
    assert "salario_base" in new_df.columns
    assert "salario_vantagens" in new_df.columns
    assert "salario_gratificacao" in new_df.columns


def test_change_salario_columns_format():
    df = pd.DataFrame(
        {
            "Salário Base": ["R$ 2,00"],
            "Salário Vantagens": ["R$ 298,99"],
            "Salário Gratificação": ["R$ 0,00"],
        }
    )
    new_df = transform_df(df)
    assert new_df["salario_base"][0] == 2.0
    assert new_df["salario_vantagens"][0] == 298.99
    assert new_df["salario_gratificacao"][0] == 0.0
