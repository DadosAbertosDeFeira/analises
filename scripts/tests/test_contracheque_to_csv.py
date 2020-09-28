import pandas as pd

from scripts.contracheque_to_csv import (
    concat_xls,
    get_filepath_attributes,
    transform_df,
    xls_from_folderpath,
)


def test_get_filepath_attributes():
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


def test_xls_from_folderpath():
    expected_filepaths = {
        "2020_01_superintendencia_municipal_de_transito.xls",
        "2020_01_fundacao_cultural_egberto_tavares_costa.xls",
    }

    filepaths = {
        filepath.name for filepath in xls_from_folderpath("scripts/tests/files/")
    }

    assert filepaths == expected_filepaths


def test_return_nothing_if_folder_has_no_xls():
    assert list(xls_from_folderpath("scripts/tests/files/empty_folder")) == []


def test_concat_xls_from_filepaths():
    filepaths = list(xls_from_folderpath("scripts/tests/files/"))
    df = concat_xls(filepaths)

    assert df.shape == (209, 10)
    assert "year" in df.columns
    assert "month" in df.columns
    assert "area" in df.columns
    assert df.iloc[0]["year"] == "2020"
    assert df.iloc[0]["month"] == "01"
    assert df.iloc[0]["area"] in [
        "superintendencia_municipal_de_transito",
        "fundacao_cultural_egberto_tavares_costa",
    ]
