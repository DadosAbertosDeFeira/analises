import re
from pathlib import Path

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
    dir = Path(__file__).parent.parent / "data"
    files = {
        2018: f"{dir}/tabespecificacaodespesa2018.xls",
        2019: f"{dir}/tabespecificacaodespesa2019.xls",
        2020: f"{dir}/tabespecificacaodespesa2020.xls",
        2021: f"{dir}/tabespecificacaodespesa2021.xls",
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


def is_company(text):
    """Identifica se um valor é um CNPJ ou não.

    Retorna True para um CNPJ, False para um CPF
    e None para não identificável.
    """
    # checa valores sem máscara
    text = str(text)
    if len(text) == 14 and text.isdigit():
        return True
    if len(text) == 11 and text.isdigit():
        return False

    # checa valores com máscara
    if len(text) == 18:
        cnpj_pattern = r"\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}"
        result = re.search(cnpj_pattern, text)
        if result:
            return True
    elif len(text) == 14:
        cpf_pattern = r"\d{3}\.\d{3}\.\d{3}\-\d{2}"
        result = re.search(cpf_pattern, text)
        if result:
            return False
    return
