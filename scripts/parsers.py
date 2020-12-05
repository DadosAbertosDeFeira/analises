import re
import unicodedata
from pathlib import Path

import nltk
import xlrd
from nltk.corpus import stopwords
from scripts.stopwords import CUSTOM_STOPWORDS

nltk.download("stopwords")


def currency_to_float(value):
    """Converte de R$ 69.848,70 (str) para 69848.70 (float)."""
    try:
        cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
        return float(cleaned_value)
    except ValueError:
        return


def remove_ponctuation(text):
    """
    Remove pontuação, dígitos e espaços em branco
    """

    if not isinstance(text, str):
        return ""

    return " ".join(re.findall(r"[A-Za-zÀ-ú]+[-A-Za-zÀ-ú]*", text))


def remove_accents(text):
    """
    # Remove accents
    # TODO: Apparently this doesn't remove accents like "á", é" and so on.
    # Maybe it would be a good idea to remove those as well
    """

    if not isinstance(text, str):
        return ""

    nfkd_form = unicodedata.normalize("NFKD", text)
    return "".join([char for char in nfkd_form if not unicodedata.combining(char)])


def remove_stopwords(text):
    if not isinstance(text, str):
        return ""

    nltk_stopwords = stopwords.words("portuguese")
    all_stopwords = nltk_stopwords + CUSTOM_STOPWORDS

    text = [word for word in text.split() if word not in all_stopwords]
    return " ".join(text)


def clean_text(text, remove_accents=False):
    if not isinstance(text, str):
        return ""

    text = remove_ponctuation(text.lower())
    if remove_accents:
        text = remove_accents(text)
    return remove_stopwords(text)


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
