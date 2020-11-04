#!/usr/bin/env python
# coding: utf-8

# # Conhecendo os Dados

# In[103]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from unidecode import unidecode

pesquisa = pd.read_csv("resultados-pesquisa-anonimizado.csv")
pesquisa.info()


# In[104]:


pesquisa.describe()[:2]


# Inicialmente, podemos ver que todos os campos do resultado da pesquisa consistem de objetos, provavelmente representando informações textuais. Isso também é resultado da forma como os dados foram armazenados na planilha no Google Sheets.
#
# Analisando as colunas, podemos considerar que a informação de data/hora da resposta da pesquisa pode ser descartada, já que não traz um dado que possa ser analisado em conjunto com os demais, representando apenas o momento em que aquela resposta foi preenchida.
#
# A maioria das demais colunas possuem quase que todos os registros com valores únicos. Supondo que isso seja resultado da inserção da informação por um campo de texto, podemos tentar analisar respostas que sejam semelhantes e agrupá-las, criando categorias que possam ser mais úteis para a análise.
#
# A coluna que menos apresenta valores únicos para os seus registros é a pergunta <i>"Com qual frequência você busca por informações fornecidas pela prefeitura de Feira de Santana?"</i>. Supondo que a pergunta tenha disponibilizado opções para resposta, isso faz sentido. Ainda assim, a pergunta supõe uma ordenação entre as respostas, que buscaremos evidenciar.

# In[105]:


pesquisa.drop(["Carimbo de data/hora"], axis=1, inplace=True)


# # Limpeza e Exibição dos Dados

# ## Ocupação

# In[106]:


pesquisa["Qual sua atual ocupação (profissão ou estudante)? "].unique()


# Vendo os resultados únicos e o texto da coluna para a pergunta sobre ocupação, podemos fazer uma breve limpeza nos dados e classificação, criando uma nova coluna.

# In[107]:


pesquisa["OCUPACAO"] = (
    pesquisa["Qual sua atual ocupação (profissão ou estudante)? "]
    .fillna("Não informado")
    .apply(str.strip)
    .apply(str.title)
)


# In[108]:


pesquisa["OCUPACAO"].sort_values().unique()


# Analisando novamente as profissões, podemos considerar algumas categorias.
#
# "Bombeiro Militar", "Policial Militar" e "Polícial Militar" podem ser agrupados em uma categoria "Militar".
#
# "Professor" e "Professora" podem ser agrupados em "Professor/Professora".
#
# "Promotor De Vendas" e "Representante" podem ser agrupados em "Vendas".
#
# "Publicitária" e "Publicitário E Locutor" podem ser agrupados em "Publicitário/Publicitária".
#
# As demais ocupações não parecem se agrupar naturalmente.

# In[109]:


def categorize_profession(profession):
    if "militar" in profession.lower():
        return "Militar"
    if "professor" in profession.lower():
        return "Professor/Professora"
    if profession in ("Promotor De Vendas", "Representante"):
        return "Vendedor/Representante"
    if "publicit" in profession.lower():
        return "Publicitário/Publicitária"
    if "community manager" in profession.lower():
        return "Organizador de Comunidade"
    else:
        return profession


pesquisa["OCUPACAO_CATEGORY"] = pesquisa["OCUPACAO"].apply(categorize_profession)


# In[110]:


pesquisa.groupby("OCUPACAO_CATEGORY").size().sort_values().plot(
    kind="barh", title="Ocupação Profissional"
)


# ## Frequência de Busca de Informações

# In[111]:


# Reescrevendo a resposta em uma escrita mais concisa
pesquisa.loc[
    pesquisa[
        "Com qual frequência você busca por informações fornecidas pela prefeitura de Feira de Santana?"
    ]
    == "Depende da semana, mas geralmente mais de uma vez por semana. ",
    "Com qual frequência você busca por informações fornecidas pela prefeitura de Feira de Santana?",
] = "Mais de 1 vez por semana"


# In[112]:


pesquisa[
    "Com qual frequência você busca por informações fornecidas pela prefeitura de Feira de Santana?"
].value_counts()


# As informações já estão bem descritas, e podemos exibir os dados de forma ordenada.

# In[113]:


order = [
    "Todos os dias",
    "Mais de 1 vez por semana",
    "1 vez por semana",
    "1 vez por mês",
    "Quase nunca",
    "Nunca busquei",
]
pesquisa[
    "Com qual frequência você busca por informações fornecidas pela prefeitura de Feira de Santana?"
].value_counts().reindex(order).plot(
    kind="barh", title="Frequência de busca de informações"
)


# ## Expectativa das Informações

# In[114]:


pesquisa[
    "Que tipo de informação você ESPERA encontrar no Dados abertos de Feira? (Coisas que você acredita que é certeza ter)"
].value_counts()


# Podemos notar que todas as respostas são distintas entre si, provavelmente resultado da coleta através de uma caixa de texto.
#
# Assim como fizemos em outras perguntas, podemos estabelecer categorias através de palavras-chave. Como a quantidade de respostas não é muito extensa, é possível fazer uma análise em cada uma das respostas.
#
# Em uma observação das respostas, podemos estabelecer as seguintes categorias:
#
# 1. Investimentos (infraestrutura, despesas gerais, salário);
# 2. Saúde;
# 3. Educação;
# 4. Segurança;
# 5. Orçamento (verba);
# 6. Transparência;
# 7. Outros;
#
# Uma resposta pode estar representada em mais de uma categoria. Assim, a soma das categorias pode ser maior que a quantidade de respostas obtidas.

# In[115]:


def categorize_expectation_public_investments(answer):
    if any(
        x in unidecode(answer.lower())
        for x in [
            "servidor",
            "investimento",
            "obra",
            "urbanizacao",
            "salario",
            "compra",
            "dinheiro",
            "bairro",
            "recurso",
            "gasto",
            "licitacao",
            "licitacoes",
        ]
    ):
        return 1
    return 0


def categorize_expectation_public_health(answer):
    if any(x in unidecode(answer.lower()) for x in ["saude"]):
        return 1
    return 0


def categorize_expectation_public_education(answer):
    if any(x in unidecode(answer.lower()) for x in ["educacao", "escola", "colegio"]):
        return 1
    return 0


def categorize_expectation_public_safety(answer):
    if any(x in unidecode(answer.lower()) for x in ["seguranca"]):
        return 1
    return 0


def categorize_expectation_public_budget(answer):
    if any(x in unidecode(answer.lower()) for x in ["verba", "dinheiro", "receita"]):
        return 1
    return 0


def categorize_expectation_public_transparency(answer):
    if any(
        x in unidecode(answer.lower())
        for x in [
            "informacoes",
            "informacao",
            "transparencia",
            "gasto",
            "dados",
            "verdade",
            "clareza",
        ]
    ):
        return 1
    return 0


def categorize_expectation_others(answer):
    if any(
        x in unidecode(answer.lower())
        for x in ["geral", "relato", "proposta", "grafico"]
    ):
        return 1
    return 0


def categorize_information(answer):
    if any(
        x in unidecode(answer.lower())
        for x in [
            "retorno",
            "gastos",
            "questionamento",
            "atende",
            "conteudo",
            "informacao",
            "informacoes",
            "dados",
            "confiabilidade",
            "resumo",
            "divulgacao",
        ]
    ):
        return 1
    return 0


def categorize_frequency(answer):
    if any(
        x in unidecode(answer.lower())
        for x in [
            "frequente",
            "atualizacao",
            "tempo real",
            "atualizados",
            "atualizadas",
        ]
    ):
        return 1
    return 0


def categorize_usability(answer):
    if any(
        x in unidecode(answer.lower())
        for x in ["facilidade", "intuitiva", "intuitivo",]
    ):
        return 1
    return 0


pesquisa["ANSWER_INVESTMENT"] = pesquisa[
    "Que tipo de informação você ESPERA encontrar no Dados abertos de Feira? (Coisas que você acredita que é certeza ter)"
].apply(categorize_expectation_public_investments)

pesquisa["ANSWER_HEALTH"] = pesquisa[
    "Que tipo de informação você ESPERA encontrar no Dados abertos de Feira? (Coisas que você acredita que é certeza ter)"
].apply(categorize_expectation_public_health)

pesquisa["ANSWER_EDUCATION"] = pesquisa[
    "Que tipo de informação você ESPERA encontrar no Dados abertos de Feira? (Coisas que você acredita que é certeza ter)"
].apply(categorize_expectation_public_education)

pesquisa["ANSWER_SAFETY"] = pesquisa[
    "Que tipo de informação você ESPERA encontrar no Dados abertos de Feira? (Coisas que você acredita que é certeza ter)"
].apply(categorize_expectation_public_safety)

pesquisa["ANSWER_BUDGET"] = pesquisa[
    "Que tipo de informação você ESPERA encontrar no Dados abertos de Feira? (Coisas que você acredita que é certeza ter)"
].apply(categorize_expectation_public_budget)

pesquisa["ANSWER_TRANSPARENCY"] = pesquisa[
    "Que tipo de informação você ESPERA encontrar no Dados abertos de Feira? (Coisas que você acredita que é certeza ter)"
].apply(categorize_expectation_public_transparency)

pesquisa["ANSWER_OTHERS"] = pesquisa[
    "Que tipo de informação você ESPERA encontrar no Dados abertos de Feira? (Coisas que você acredita que é certeza ter)"
].apply(categorize_expectation_others)


# In[116]:


labels = {
    "ANSWER_INVESTMENT": "INVESTIMENTO",
    "ANSWER_HEALTH": "SAÚDE",
    "ANSWER_EDUCATION": "EDUCAÇÃO",
    "ANSWER_SAFETY": "SEGURANÇA",
    "ANSWER_BUDGET": "ORÇAMENTO",
    "ANSWER_TRANSPARENCY": "TRANSPARÊNCIA",
    "ANSWER_OTHERS": "OUTROS",
}
pesquisa[
    [
        "ANSWER_INVESTMENT",
        "ANSWER_HEALTH",
        "ANSWER_EDUCATION",
        "ANSWER_SAFETY",
        "ANSWER_BUDGET",
        "ANSWER_TRANSPARENCY",
        "ANSWER_OTHERS",
    ]
].apply(np.sum).rename(index=labels).sort_values().plot(
    kind="barh", title="Expectativa do tipo de informação"
)


# ## Informações Adicionais

# In[117]:


pesquisa[
    "Que tipo de informação você GOSTARIA que tivesse em um portal de transparência de dados da cidade? (Coisas que vão além do obrigado a ter)"
].value_counts()


# Em relação à pergunta de quais informações seria interessante existirem no portal (indo além do obrigatório), novamente temos respostas únicas para cada respondente. Isso é esperado, decorrente da forma discursiva da coleta dos dados. Faremos a categorização de forma semelhante à pergunta anterior.

# In[118]:


pesquisa[
    "Que tipo de informação você GOSTARIA que tivesse em um portal de transparência de dados da cidade? (Coisas que vão além do obrigado a ter)"
] = pesquisa[
    "Que tipo de informação você GOSTARIA que tivesse em um portal de transparência de dados da cidade? (Coisas que vão além do obrigado a ter)"
].fillna(
    ""
)


# In[119]:


pesquisa["SECOND_ANSWER_INVESTMENT"] = pesquisa[
    "Que tipo de informação você GOSTARIA que tivesse em um portal de transparência de dados da cidade? (Coisas que vão além do obrigado a ter)"
].apply(categorize_expectation_public_investments)

pesquisa["SECOND_ANSWER_HEALTH"] = pesquisa[
    "Que tipo de informação você GOSTARIA que tivesse em um portal de transparência de dados da cidade? (Coisas que vão além do obrigado a ter)"
].apply(categorize_expectation_public_health)

pesquisa["SECOND_ANSWER_EDUCATION"] = pesquisa[
    "Que tipo de informação você GOSTARIA que tivesse em um portal de transparência de dados da cidade? (Coisas que vão além do obrigado a ter)"
].apply(categorize_expectation_public_education)

pesquisa["SECOND_ANSWER_SAFETY"] = pesquisa[
    "Que tipo de informação você GOSTARIA que tivesse em um portal de transparência de dados da cidade? (Coisas que vão além do obrigado a ter)"
].apply(categorize_expectation_public_safety)

pesquisa["SECOND_ANSWER_BUDGET"] = pesquisa[
    "Que tipo de informação você GOSTARIA que tivesse em um portal de transparência de dados da cidade? (Coisas que vão além do obrigado a ter)"
].apply(categorize_expectation_public_budget)

pesquisa["SECOND_ANSWER_TRANSPARENCY"] = pesquisa[
    "Que tipo de informação você GOSTARIA que tivesse em um portal de transparência de dados da cidade? (Coisas que vão além do obrigado a ter)"
].apply(categorize_expectation_public_transparency)

pesquisa["SECOND_ANSWER_OTHERS"] = pesquisa[
    "Que tipo de informação você GOSTARIA que tivesse em um portal de transparência de dados da cidade? (Coisas que vão além do obrigado a ter)"
].apply(categorize_expectation_others)


# In[120]:


labels = {
    "SECOND_ANSWER_INVESTMENT": "INVESTIMENTO",
    "SECOND_ANSWER_HEALTH": "SAÚDE",
    "SECOND_ANSWER_EDUCATION": "EDUCAÇÃO",
    "SECOND_ANSWER_SAFETY": "SEGURANÇA",
    "SECOND_ANSWER_BUDGET": "ORÇAMENTO",
    "SECOND_ANSWER_TRANSPARENCY": "TRANSPARÊNCIA",
    "SECOND_ANSWER_OTHERS": "OUTROS",
}
pesquisa[
    [
        "SECOND_ANSWER_INVESTMENT",
        "SECOND_ANSWER_HEALTH",
        "SECOND_ANSWER_EDUCATION",
        "SECOND_ANSWER_SAFETY",
        "SECOND_ANSWER_BUDGET",
        "SECOND_ANSWER_TRANSPARENCY",
        "SECOND_ANSWER_OTHERS",
    ]
].apply(np.sum).rename(index=labels).sort_values().plot(
    kind="barh", title="Informações além do obrigatório"
)


# ## Incentivo a Retorno

# In[121]:


pesquisa[
    "O que lhe faria voltar a consultar o portal Dados abertos de Feira com frequência?"
].value_counts()


# Para a questão "O que lhe faria voltar a consultar o portal Dados abertos de Feira com frequência?", temos novamente respostas diferentes entre os respondentes. Faremos uma categorização assim como nas perguntas anteriores.

# In[122]:


pesquisa["THIRD_ANSWER_INFO"] = pesquisa[
    "O que lhe faria voltar a consultar o portal Dados abertos de Feira com frequência?"
].apply(categorize_information)

pesquisa["THIRD_ANSWER_FREQ"] = pesquisa[
    "O que lhe faria voltar a consultar o portal Dados abertos de Feira com frequência?"
].apply(categorize_frequency)

pesquisa["THIRD_ANSWER_USABILITY"] = pesquisa[
    "O que lhe faria voltar a consultar o portal Dados abertos de Feira com frequência?"
].apply(categorize_usability)


# In[123]:


labels = {
    "THIRD_ANSWER_INFO": "QUALIDADE DA INFORMAÇÃO",
    "THIRD_ANSWER_FREQ": "FREQUÊNCIA DA INFORMAÇÃO",
    "THIRD_ANSWER_USABILITY": "SISTEMA INTUITIVO",
}
pesquisa[["THIRD_ANSWER_INFO", "THIRD_ANSWER_FREQ", "THIRD_ANSWER_USABILITY"]].apply(
    np.sum
).rename(index=labels).sort_values().plot(
    kind="barh",
    title="O que me faria voltar a utilizar o portal?",
    xticks=np.arange(2, 22, 2),
)


# ## Outras Fontes de Informação

# In[124]:


pesquisa["Quais sites você usa ou já usou para pesquisar esses dados?"] = pesquisa[
    "Quais sites você usa ou já usou para pesquisar esses dados?"
].fillna("Nenhum")
pesquisa["Quais sites você usa ou já usou para pesquisar esses dados?"].value_counts()


# Podemos ver que existem algumas respostas semelhantes, embora a maior parte dos respondentes não tenha informado outra fonte de informação dos dados municipais. De qualquer forma, precisamos categorizar algumas das informações. Apesar do Acorda Cidade ser um website, pela quantidade expressiva de respostas, vamos separá-lo em uma categoria própria.

# In[125]:


def categorize_acorda_cidade(answer):
    if any(x in unidecode(answer.lower()).strip() for x in ["acorda cidade"]):
        return 1
    return 0


def categorize_prefeitura(answer):
    if any(x in unidecode(answer.lower()).strip() for x in ["prefeitura"]):
        return 1
    return 0


def categorize_diario_oficial(answer):
    if any(x in unidecode(answer) for x in ["DO", "oficial"]):
        return 1
    return 0


def categorize_sites(answer):
    if any(
        x in unidecode(answer.lower()).strip() for x in ["sites", "jornal", "jornais"]
    ):
        return 1
    return 0


def categorize_none(answer):
    if any(x in unidecode(answer.lower()).strip() for x in ["nenhum"]):
        return 1
    return 0


# In[126]:


pesquisa["FOURTH_ANSWER_ACORDA_CIDADE"] = pesquisa[
    "Quais sites você usa ou já usou para pesquisar esses dados?"
].apply(categorize_acorda_cidade)

pesquisa["FOURTH_ANSWER_CITY_HALL"] = pesquisa[
    "Quais sites você usa ou já usou para pesquisar esses dados?"
].apply(categorize_prefeitura)

pesquisa["FOURTH_ANSWER_OFFICIAL"] = pesquisa[
    "Quais sites você usa ou já usou para pesquisar esses dados?"
].apply(categorize_diario_oficial)

pesquisa["FOURTH_ANSWER_WEBSITES"] = pesquisa[
    "Quais sites você usa ou já usou para pesquisar esses dados?"
].apply(categorize_sites)

pesquisa["FOURTH_ANSWER_NONE"] = pesquisa[
    "Quais sites você usa ou já usou para pesquisar esses dados?"
].apply(categorize_none)


# In[127]:


labels = {
    "FOURTH_ANSWER_ACORDA_CIDADE": "ACORDA CIDADE",
    "FOURTH_ANSWER_CITY_HALL": "PREFEITURA",
    "FOURTH_ANSWER_OFFICIAL": "DIÁRIO OFICIAL",
    "FOURTH_ANSWER_WEBSITES": "OUTROS SITES",
    "FOURTH_ANSWER_NONE": "NENHUM",
}
pesquisa[
    [
        "FOURTH_ANSWER_ACORDA_CIDADE",
        "FOURTH_ANSWER_CITY_HALL",
        "FOURTH_ANSWER_OFFICIAL",
        "FOURTH_ANSWER_WEBSITES",
        "FOURTH_ANSWER_NONE",
    ]
].apply(np.sum).rename(index=labels).sort_values().plot(
    kind="barh", title="Outros sites utilizados"
)


# In[128]:


labels = {
    "FOURTH_ANSWER_ACORDA_CIDADE": "ACORDA CIDADE",
    "FOURTH_ANSWER_CITY_HALL": "PREFEITURA",
    "FOURTH_ANSWER_OFFICIAL": "DIÁRIO OFICIAL",
    "FOURTH_ANSWER_WEBSITES": "OUTROS SITES",
}
pesquisa[
    [
        "FOURTH_ANSWER_ACORDA_CIDADE",
        "FOURTH_ANSWER_CITY_HALL",
        "FOURTH_ANSWER_OFFICIAL",
        "FOURTH_ANSWER_WEBSITES",
    ]
].apply(np.sum).rename(index=labels).sort_values().plot(
    kind="barh", title="Outros sites utilizados (para aqueles que usam)"
)
