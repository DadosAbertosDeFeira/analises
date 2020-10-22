import re

import xlrd


def currency_to_float(value):
    """Converte de R$ 69.848,70 (str) para 69848.70 (float)."""
    try:
        cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
        return float(cleaned_value)
    except ValueError:
        return


def extract_nature(nature_str):
    """Extrai natureza da despesa a partir de um texto."""
    formatted = r"\d{1}\.\d{1}.\d{2}.\d{2}.\d{2}"
    not_formatted = r"\d+"

    result = re.findall(formatted, nature_str)
    if result:
        return result[0].replace(".", "")

    result = re.findall(not_formatted, nature_str)
    if result:
        return result[0][:8]
    return


def all_expenses_nature_from_tcmba(year=None):
    """Extrai e formata natureza das despesas do TCM-BA.

    Os arquivos podem ser encontrados na página de contabilidade municipal
    do TCM-BA: https://www.tcm.ba.gov.br/contabilidade-municipal/.
    Para evitar indisponibilidade dos dados e ter carregamento mais rápido
    das informações, os arquivos foram commitados na pasta ``data`` desse
    repositório.
    """
    files = {
        2018: "data/tabespecificacaodespesa2018.xls",
        2019: "data/tabespecificacaodespesa2019.xls",
        2020: "data/tabespecificacaodespesa2020.xls",
        2021: "data/tabespecificacaodespesa2021.xls",
    }
    if not year:
        year = max(files.keys())
    workbook = xlrd.open_workbook(files.get(year))
    worksheet = workbook.sheet_by_index(0)
    natures = {}
    for row in worksheet.get_rows():
        code = None
        superior_group_code = None
        valid_row = True
        if isinstance(row[0].value, str):
            valid_row = row[0].value.lower() not in ["codigo", "código"]
            if valid_row:
                # é string mas não é o cabeçalho
                code = row[0].value
                if row[2].value not in [0, "0"] and row[0].value != row[2].value:
                    superior_group_code = row[2].value
        else:
            # ao invés de string, foi usado o formato float no arquivo.
            # a conversão é necessária porque a biblioteca lê o valor da mesma
            # forma como ele é salvo no Office (float ao invés de string)
            code = str(int(row[0].value))
            if row[2].value != 0 and row[0].value != row[2].value:
                superior_group_code = str(int(row[2].value))

        if valid_row:
            natures[code] = {
                "code": code,
                "description": row[1].value,
                "superior_group_code": superior_group_code,
            }
    return natures


def identify_code_and_description(row):
    """Identifica classificação da despesa e sua descrição.

    O Tribunal de Contas dos Municípios da Bahia disponibiliza
    um arquivo com as naturezas da despesa.
    Esse método extrai informações desse arquivo.

    Exemplo de entradas esperadas:

    CO	GD	MA	ED	SED	Código	     Código sem máscara   Descrição
    3	0	00	00	00	3.0.00.00.00 30000000 Despesas Correntes
    3 	1	00	00	00	3.1.00.00.00 31000000 Pessoal e Encargos Sociais
    3	1	71	00	00	3.1.71.00.00 31710000 Transferências a Consórcios...
    3	1	71	70	00	3.1.71.70.00 31717000 Rateio pela Participação...
    3	1	90	01	01	3.1.90.01.01 31900101 Aposentadorias Custeadas...
    """
    from_pandas = False
    try:
        import pandas as pd

        if isinstance(row, pd.Series) or isinstance(row, pd.DataFrame):
            from_pandas = True
    except ModuleNotFoundError:
        pass
    # FIXME add tests
    if from_pandas:
        if row.empty or len(row) < 8:
            return
    elif not row or len(row) < 8:
        return

    code_and_description = {
        "code_with_mask": row[5],
        "code": row[5].replace(".", ""),
        "description": row[7],
    }

    is_gd_empty = row[1] == "0"
    is_ma_empty = row[2] == "00"
    is_ed_empty = row[3] == "00"
    is_sed_empty = row[4] == "00"

    is_co = all([is_gd_empty, is_ma_empty, is_ed_empty, is_sed_empty])
    if is_co:
        code_and_description["value"] = row[0]
        code_and_description["group"] = "CO"
        return code_and_description
    is_gd = all([is_ma_empty, is_ed_empty, is_sed_empty])
    if is_gd:
        code_and_description["value"] = row[1]
        code_and_description["group"] = "GD"
        return code_and_description
    is_ma = all([is_ed_empty, is_sed_empty])
    if is_ma:
        code_and_description["value"] = row[2]
        code_and_description["group"] = "MA"
        return code_and_description
    is_ed = is_sed_empty
    if is_ed:
        code_and_description["value"] = row[3]
        code_and_description["group"] = "ED"
        return code_and_description
    is_sed = not all([is_gd_empty, is_ma_empty, is_ed_empty, is_sed_empty])
    if is_sed:
        code_and_description["value"] = row[4]
        code_and_description["group"] = "SED"
        return code_and_description
