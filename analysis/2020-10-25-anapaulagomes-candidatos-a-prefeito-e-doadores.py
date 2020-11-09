#!/usr/bin/env python
# coding: utf-8

# # Candidatos a prefeito, doações e doadores
#
# A partir dos dados da prestação de contas das eleições feitas ao Tribunal Superior
# Eleitoral (TSE) analisamos os dados das doações recebidas por candidatos a prefeitura
# de Feira de Santana. Apesar de saber que esse ano as doações vindas de empresas
# não são permitidas, [sabemos que não é o fim delas](https://twitter.com/fecampa/status/1325791183554154498?s=20).
#
# Vale salientar que os dados são atualizados pelo TSE diariamente. Atenção a data
# que essa análise foi publicada e a data de _download_ do arquivo.
#
# ### Instruções download dos dados
#
# A análise foi feita com arquivos do [repositório de dados eleitorais do TSE](https://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais-1/repositorio-de-dados-eleitorais).
#
# Faça o download do arquivo: http://agencia.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_2020.zip (download feito em 31/10/2020)
#
# Siga o seguinte caminho dentro da pasta:
# ```
# Prestação de contas eleitorais > 2020 > Candidatos (formato zip) > receitas_candidatos_2020_BA.csv
# ```
#
# Copie o arquivo do estado desejado (`receitas_candidatos_2020_<estado>.csv`)
# para a pasta `analysis` nesse repositório.
#
# Dicionário de dados: `leiame_receitas-candidatos.pdf`
#
# Observações sobre os dados:
#
# * `#NULO` é o mesmo que `None`
# * `#NE` significa que naquele ano a informação não era registrada
# * Campo `UF`: `BR` para nível nacional, `VT` voto em trânsito e `ZZ` para Exterior
# * Campo `NM_UE`, no caso de eleições municipais, é o nome do município

# In[2]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scripts.parsers import currency_to_float, is_company

df = pd.read_csv("receitas_candidatos_2020_BA.csv", encoding="latin", delimiter=";")


# In[3]:


# In[4]:


df_feira = df[df["NM_UE"] == "FEIRA DE SANTANA"].copy()


# In[5]:


df_feira["VR_RECEITA"] = df_feira["VR_RECEITA"].apply(currency_to_float)


# Abaixo uma amostra aleatória de 5 doações recebidas:

# In[36]:


fields = [
    "NM_CANDIDATO",
    "SG_PARTIDO",
    "DS_FONTE_RECEITA",
    "DS_ORIGEM_RECEITA",
    "NR_CPF_CNPJ_DOADOR",
    "NM_DOADOR",
    "NM_DOADOR_RFB",
    "DS_CARGO",
    "NM_MUNICIPIO_DOADOR",
    "NM_PARTIDO_DOADOR",
    "DT_RECEITA",
    "DS_RECEITA",
    "VR_RECEITA",
]

df_filtered = df_feira[fields]


# ## Doações recebidas por candidatos a prefeito
#
# Vamos filtrar as doações feitas para prefeitos.
# Ao final dessa página você poderá ver a lista com todos as doações
# recebidas pelos candidatos a prefeito na cidade de Feira de Santana.

# In[7]:


mayor_df = df_filtered[df_filtered["DS_CARGO"] == "Prefeito"]
mayor_df.sample(5)  # amostra das doações a prefeitos de Feira de Santana


# ### Total, mediana e número de doações recebidas por candidato

# In[8]:


mayor_df.groupby(["NM_CANDIDATO"])["VR_RECEITA"].agg(
    ["sum", "median", "count"]
).sort_values(ascending=False, by=["sum", "NM_CANDIDATO"])


# In[13]:


sns.set_theme(style="whitegrid")
f, ax = plt.subplots(figsize=(6, 15))
plt.ticklabel_format(style="plain", axis="y", useOffset=False)

sns.set_color_codes("pastel")

sns.barplot(
    x="VR_RECEITA",
    y="NM_CANDIDATO",
    data=mayor_df,
    label="Total",
    color="b",
    ci=None,
    estimator=sum,
)

ax.set(xlabel="Total de doações em R$ por candidatos", ylabel="")
sns.despine(left=True, bottom=True)


# ## Quem são os doadores?

# In[35]:


mayor_df.groupby(
    [
        "NM_CANDIDATO",
        "NM_DOADOR_RFB",
        "NR_CPF_CNPJ_DOADOR",
        "NM_PARTIDO_DOADOR",
        "NM_MUNICIPIO_DOADOR",
    ]
)["VR_RECEITA"].agg(["sum"])


# ### Qual a origem dos recursos?

# In[37]:


ax = sns.stripplot(
    x="NM_CANDIDATO",
    y="VR_RECEITA",
    hue="DS_ORIGEM_RECEITA",
    data=mayor_df,  # , xlabel="Candidato", ylabel="R$"
)
ax.set_xlabel("Candidato")
# ax.set_yscale("log")
ax.set_ylabel("R$")
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)


# Entre os candidatos podemos ver diferenças na distribuição da origem das receitas.
# O candidato CARLOS MEDEIROS MIRANDA (Novo) recebeu doações diversificadas de pessoas
# físicas. Enquanto DAYANE JAMILLE CARNEIRO DOS SANTOS PIMENTEL recebeu massivamente doações
# vindas do seu partido (PSL), graças ao fundão eleitoral.
# A candidata que se destacou no recebimento de recursos de financiamento coletivo, que
# ainda não é muito popular dentre os outros candidatos, foi a MARCELA PREST (PSOL).
# O candidato JOSE CERQUEIRA DE SANTANA NETO foi quem mais investiu em sua campanha
# a partir de recursos próprios.
#
# ### Veja os valores por candidato e origem

# In[15]:


mayor_df.groupby(["NM_CANDIDATO", "DS_ORIGEM_RECEITA"])["VR_RECEITA"].agg(["sum"])


# ## Ranking de Doadores

# In[17]:


mayor_df.groupby(["NM_DOADOR_RFB", "NM_DOADOR"])["VR_RECEITA"].agg(["sum"]).sort_values(
    ascending=False, by=["sum", "NM_DOADOR_RFB"]
)


# ## As pessoas que doaram estão ligadas a empresas diretamente?

# In[32]:


def mask_cpf(cpf):
    """Útil para busca dos sócios em empresas no Brasil.io."""
    cpf = str(cpf)
    return f"***{cpf[3:9]}**"


mayor_df_copy = mayor_df.copy()
mayor_df_copy["DONATED_BY_CNPJ"] = mayor_df_copy["NR_CPF_CNPJ_DOADOR"].apply(is_company)

donated_by_people = mayor_df_copy[mayor_df_copy["DONATED_BY_CNPJ"] == False]
donated_by_people = donated_by_people[
    donated_by_people["NM_CANDIDATO"] != donated_by_people["NM_DOADOR_RFB"]
]
donated_by_people["CPF_MASCARADO"] = mayor_df_copy["NR_CPF_CNPJ_DOADOR"].apply(mask_cpf)
donated_by_people[
    ["NM_CANDIDATO", "NM_DOADOR_RFB", "NR_CPF_CNPJ_DOADOR", "CPF_MASCARADO"]
]


# Para verificar se os doadores são sócios em empresas, basta acessar
# https://brasil.io/dataset/socios-brasil/socios/ e buscar pelo nome completo.
#
# Verifique se o CPF mascarado bate com o CPF da página para confirmar.

# ## Qual partido é mais generoso?
#
# As doações feitas por partidas podem ser identificadas pela coluna `NM_PARTIDO_DOADOR`.
# O valor `#NULO#` representa as doações feitas por todas as outras entidades que não são
# partidos (como pessoas e aplicativos de doação).

# In[11]:


donations_by_party = (
    mayor_df.groupby(["NM_PARTIDO_DOADOR"], as_index=False)["VR_RECEITA"]
    .agg(["sum"])
    .sort_values(ascending=False, by=["sum", "NM_PARTIDO_DOADOR"])
)
donations_by_party


# In[12]:


donations_by_party.plot.bar(
    xlabel="Partidos", stacked=True, title="Doações feitas por partidos"
)


# ## Veja todas as doações

# In[18]:


pd.set_option("display.max_rows", None)
mayor_df
