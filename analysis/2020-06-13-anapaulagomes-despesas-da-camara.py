#!/usr/bin/env python
# coding: utf-8

# # Dá para cortar?
#
# Antes mesmo da epidemia chegar ao município de Feira de Santana,
# a Câmara de Vereadores já era conhecida por seus gastos extravagantes.
# A casa já chegou a gastar, de uma só vez, [17.767,60 em iogurtes][1]
# e disponibilizar 60 linhas de telefone celular para uso dos vereadores ,
# apesar dos gastos [R$ 40 mil anuais com a Telemar][1].
#
# [1]: https://www.blogdovelame.com/camara-de-feira-ja-chegou-a-comprar-616-unidades-de-iogurte-de-uma-so-vez/
# [2]: https://www.blogdovelame.com/camara-de-feira-disponibiliza-60-linhas-de-telefone-celular-para-uso-dos-vereadores/
#
#
# Muitas Câmaras tem se mobilizado para cortar gastos e repassar a verba
# para que a prefeitura utilize nos esforços para conter a pandemia.
#
# Nesse texto vamos conhecer um pouco melhor as despesas da Câmara e
# o que pode ser cortado para ajudar o município na crise do COVID-19.
#
# ## As despesas da Câmara Municipal
#
# Antes, vamos entender um pouco sobre as despesas, segundo a própria Câmara:
#
# > São todos os gastos feitos pela Câmara. As Despesas são divididas em:
#
# > - Despesas correntes. Aquelas necessárias à manutenção dos serviços públicos, como as despesas com material de consumo, telefone, pessoal, serviços de terceiros, etc.
# > - Despesas de capital. São os investimentos, ou seja, gastos com novos equipamentos e obras, como construção e reforma de escolas, hospitais, postos de saúde, pavimentação, etc.
# Os registros de classificação da despesa são efetuados por meio de rotinas específicas e de forma geral podem ser assim tratadas:
#
# > - Valor Orçado (Dotação Orçamentária) - Dependem de autorização legislativa e correspondem ao valor a ser utilizado para a manutenção da Administração Pública;
# > - Valor Empenhado - Consiste na reserva da dotação orçamentária para um fim específico, devendo registrar o nome/razão social do credor, valor e descrição do que será pago;
# > - Valor Liquidado - Registra efetivamente a despesa executada. No entanto, por ocasião do encerramento do exercício, conforme as normas da Lei Federal n° 4.320/1964, as despesas empenhadas e ainda não liquidadas são inscritas em restos a pagar não processados;
# > - Valor Pago - Consiste na entrega do numerário ao credor e só pode ser efetuado após regular liquidação da despesa.
#
# Fonte: https://www.transparencia.feiradesantana.ba.leg.br/index.php?view=despesasinfo
#
# No [portal da transparência](https://www.transparencia.feiradesantana.ba.leg.br/index.php?view=despesasinfo)
# podemos verificar os gastos nas três fases: empenho, liquidação e pagamento. Cada despesa
# apresenta também as seguintes informações:
#
# ![](images/despesa.png)
#
# * Data
# * Fase
# * Credor (Empresa ou pessoa física)
# * Valor
# * Número
# * Documento (o CPF ou CNPJ da empresa ou pessoa)
# * Número do processo
# * Bem / Serviço prestado
# * Natureza
# * Função
# * Subfunção
# * Processo licitatório
# * Fonte de recurso
#
# Mas como saber qual valor pode ser gasto pelo município durante o ano?
#
# ## Lei Orçamentária
#
# O valor que o município pode gastar, bem como a receita esperada, é estabelecido
# pela Lei Orçamentária Anual (LOA). Todos os anos o município deve estabelecer um orçamento
# para o ano seguinte. Saiba mais sobre isso [aqui](https://www.politize.com.br/ppa-ldo-loa-3-siglas-que-definem-orcamento-governo/).
#
# Embora esteja publicada no diário oficial, a LOA de Feira de Santana não foi encontrada
# facilmente nos portais da transparência da prefeitura e da câmara. Você pode acessá-la
# [aqui](http://www.diariooficial.feiradesantana.ba.gov.br/atos/executivo/1JE1WJ2162019.pdf).
#

# In[34]:


import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Baixe os dados das despesas da Câmara aqui:
#
# https://www.kaggle.com/anapaulagomes/despesas-da-cmara-municipal
#
# Descompacte o arquivo e coloque na pasta `analysis`.

# In[35]:


despesas = pd.read_csv("expenses-11.04.2020.csv")
despesas.head()


# In[36]:


columns = [
    "crawled_at",
    "crawled_from",
    "function",
    "published_at",
    "resource",
    "subfunction",
]
despesas.drop(columns, inplace=True, axis=1)

despesas["date"] = pd.to_datetime(despesas["date"])
despesas = despesas[despesas["date"].isin(pd.date_range("2019-01-01", "2019-12-31"))]
despesas["month"] = despesas["date"].apply(lambda x: x.month)

despesas = despesas.sort_values("date", ascending=False)
despesas.head()


# In[37]:


despesas.shape


# In[38]:


despesas["value"].plot(kind="hist")


# ## Análises por classificação das despesas
#
# > O plano de contas da despesa orçamentária da Câmara está correto, pois segue ao estabelecido pelo TCM-BA, conforme Ato nº 456/2019. O código 33903005 se refere à Material de processamento de dados. Importante lembrar que a STN determina os elementos de despesa, de acordo com a Portaria Interministerial nº 163/2001, mas os desdobramentos da despesa (subelementos) são determinados pelo TCM BA. Segue em anexo o ato normativo com os códigos de despesa.
#
# ESPECIFICAÇÃO DE DESPESA 2020
#
# https://www.tcm.ba.gov.br/contabilidade-municipal/
#
# Faça o download do arquivo `.csv` do natureza das despesas [aqui](https://gist.githubusercontent.com/anapaulagomes/379525586f941a1183aa448dad282f90/raw/378f01c23f0ead542a88fde6274b12ba82b84f8e/especificacao-despesas-tcm-bahia.csv) e coloque na pasta `analysis`.
#
#
# ### Categoria econômica
#
#
# CATEGORIA ECONÔMICA: a despesa orçamentária, assim como a receita orçamentária, é classificada em duas categorias econômicas:
#
# 3-DESPESAS CORRENTES: classificam-se nesta categoria todas as despesas que não contribuem, diretamente, para a formação ou aquisição de um bem de capital.
#
# 4 -DESPESAS  DE  CAPITAL: classificam-se  nesta  categoria  aquelas  despesas  que contribuem, diretamente, para a formação ou aquisição de um bem de capital

# In[39]:


despesas["legal_status"].unique()


# In[40]:


classificacao = pd.read_csv(
    "especificacao-despesas-tcm-bahia.csv",
    dtype={"Codigo": str, "Descricao": str, "Codigo Superior": str},
)
classificacao


# In[41]:


despesas["classificacao"] = despesas["legal_status"].str.extract("(\d{8})")

despesas_com_classificacao = despesas.merge(
    classificacao, left_on=["classificacao"], right_on=["Codigo"], how="left"
)
despesas_com_classificacao


# In[42]:


despesas.shape, despesas_com_classificacao.shape


# 3 Despesas Correntes
# 4 Despesas de Capital

# ### Com o que a Câmara anda gastando?
#
# Agora que já sabemos as informações que temos e onde encontrá-las,
# vamos dar uma olhadinha nos gastos da casa no último ano.

# O que são esses picos?
#
# * Dia 01 de Janeiro é um feriado nacional mas, em 2020, a Câmara registrou um único pagamento a Feira Cópias
# * Janeiro registrou atividade nos pagamentos durante apenas 4 dias
#

# In[43]:


sns.set_style("whitegrid")


# In[44]:


despesas_com_classificacao.groupby(
    ["subgroup", "Descricao", "Codigo"]
).size().reset_index().rename(columns={0: "count"}).sort_values(
    "count", ascending=False
)


# In[45]:


despesas_com_classificacao.groupby(["subgroup", "Descricao", "Codigo"], as_index=False)[
    "value"
].sum().sort_values(by="value", ascending=False)


# In[46]:


plt.figure(figsize=(16, 8))
plot = sns.barplot(
    data=despesas_com_classificacao,
    x="Descricao",
    y="value",
    estimator=sum,
    palette=sns.color_palette("BuGn_r", n_colors=len(despesas_com_classificacao) + 4),
)
plot.set_xticklabels(plot.get_xticklabels(), rotation=75, horizontalalignment="right")
plt.show()


# In[47]:


vencimentos = [
    "Vencimentos e Vantagens Fixas - Pessoal Civil",
    "Vencimento e vantagens fixas Pessoal Civil (Vencimento Básico)",
]
despesas_sem_vencimentos = despesas_com_classificacao[
    ~despesas_com_classificacao["Descricao"].isin(vencimentos)
]

plt.figure(figsize=(16, 8))
plot = sns.barplot(
    data=despesas_sem_vencimentos,
    x="Descricao",
    y="value",
    estimator=sum,
    palette=sns.color_palette("muted", n_colors=len(despesas_sem_vencimentos) + 4),
)
plot.set_xticklabels(plot.get_xticklabels(), rotation=75, horizontalalignment="right")
plt.show()


# In[48]:


sns.catplot(
    x="value",
    y="Descricao",
    col="month",
    data=despesas_com_classificacao,
    kind="bar",
    height=4,
    aspect=0.7,
)


# In[49]:


despesas_com_classificacao[
    ["legal_status", "subgroup", "Descricao", "summary", "Codigo"]
].head(100)


# In[50]:


# Auxílio-Alimentação
# Vale refeição/vale alimentação

# Encargos pela Honra de Avais, Garantias, Seguros e Similares


# In[51]:


# Locacao de Software / Locaçao de Software
# Materiais de Consumo - gás e outros / Materiais de Consumo - gás e outros materiais ...


# In[52]:


despesas = despesas[despesas["phase"] == "pagamento"]
despesas.describe()["value"]


# In[53]:


pd.options.display.float_format = "{:20,.2f}".format
despesas["value"].describe()


# In[54]:


despesas.nlargest(20, "value")[["date", "value", "summary", "subgroup", "phase"]]


# In[55]:


despesas.nsmallest(20, "value")[["date", "value", "summary", "subgroup", "phase"]]


# ## Quem foram os fornecedores?

# In[56]:


pd.pivot_table(
    despesas,
    values="value",
    index=["company_or_person"],
    columns="month",
    aggfunc=np.sum,
).sort_values(by="company_or_person", ascending=False)


# In[57]:


def to_csv(despesas, arquivo="todas-as-despesas-desde-2016.csv"):
    despesas.to_csv(
        arquivo,
        index=False,
        columns=[
            "published_at",
            "phase",
            "company_or_person",
            "value",
            "number",
            "document",
            "date",
            "process_number",
            "summary",
            "group",
            "function",
            "subfunction",
            "type_of_process",
            "resource",
        ],
        header=[
            "publicado_em",
            "fase",
            "empresa_ou_pessoa",
            "valor",
            "numero",
            "documento",
            "data",
            "numero_do_processo",
            "sumario",
            "grupo",
            "funcao",
            "subfuncao",
            "type_of_process",
            "fonte",
        ],
    )


# In[58]:


despesas.groupby("type_of_process")["value"].sum().plot(kind="bar")
plt.show()

despesas.groupby("group")["value"].sum().plot(kind="bar")
plt.show()

despesas.groupby("group")["value"].sum().plot(kind="bar")
plt.show()


# In[59]:


despesas.group.value_counts()


# In[60]:


despesas.company_or_person.value_counts()


# In[61]:


despesas.groupby(["company_or_person"]).sum().groupby(level=[0])[
    "value"
].cumsum().sort_values(ascending=False)


# ## O que a Câmara consome mais em cada categoria?

# In[62]:


despesas_com_classificacao["summary"].describe()


# In[63]:


despesas_com_classificacao[["Descricao", "Codigo", "summary", "value"]].tail(20)


# In[64]:


despesas.groupby(["company_or_person", "document"]).size().reset_index().rename(
    columns={0: "count"}
).sort_values("count", ascending=False)


# In[65]:


padrao = {
    re.compile("\d{2}.?\d{3}.?\d{3}/?\d{4}-?\d{2}"): "jurídica",
    re.compile("\d{3}\.\d{3}\.\d{3}\-\d{2}"): "física",
}


despesas["tipo_de_pessoa"] = despesas["document"].replace(padrao, regex=True)
print(despesas.groupby(["tipo_de_pessoa"]).size())

despesas["tipo_de_pessoa"].value_counts().plot.pie(
    y="tipo_de_pessoa",
    title="Pessoa física ou jurídica?",
    autopct="%1.1f%%",
    startangle=0,
)
