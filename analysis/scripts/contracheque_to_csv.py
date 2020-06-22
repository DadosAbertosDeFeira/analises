import pandas as pd
from glob import glob
from unidecode import unidecode

"""
Os arquivos precisam ser salvos no formato `ano_mes_entidade.xls`.
Exemplo: `2020_04_prefeitura.xls`

O script funciona em arquivos `.xls` onde as duas primeiras linhas e as últimas 3 linhas são ignoradas.
"""
# O script funciona em xls que possuem o formato:
# - duas primeiras linhas com informações para descartar
# - últimas 3 linhas com informações para descartar

folder = input("Pasta onde estão os xls:")

filepaths = glob(folder + "/*.xls")

# Transformar xls para um único dataframe incluindo colunas extras e tirando cabeçalho e rodapé
df_list = []

for path in filepaths:
    df = pd.read_excel(path, skiprows=(0, 1))
    df.drop(df.tail(3).index, inplace=True)
    filename = path.split("/")[-1]
    name, extension = filename.split(".")
    ano, mes, entidade = name.split("_")
    df["ano"] = ano
    df["mes"] = mes
    df["entidade"] = entidade
    df_list.append(df)

df_full = pd.concat(df_list)

# Editar o nome das colunas para lower e sem acentuação
columns = df_full.columns

column_list = []

for column in columns:
    column = column.lower()
    column = column.replace(" ", "_")
    column = unidecode(column)
    column_list.append(column)


# Modificar colunas no dataframe
df_full.columns = column_list


# Modificar R$ em float
def currency_to_float(value):
    """Converte de R$ 69.848,70 (str) para 69848.70 (float)."""
    try:
        cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
        return float(cleaned_value)
    except ValueError:
        return


df_full["salario_base"] = df_full["salario_base"].apply(currency_to_float)

df_full["salario_vantagens"] = df_full["salario_vantagens"].apply(currency_to_float)

df_full["salario_gratificacao"] = df_full["salario_gratificacao"].apply(
    currency_to_float
)

# Criar csv a partir do dataframe
df_full.to_csv(folder + "/contracheques.csv", index=False)
