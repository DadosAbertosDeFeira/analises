#!/usr/bin/env python
# coding: utf-8

# # Análise exploratória de textos
#
# Sobre o que falam os documentos oficiais?
# Quais as palavras mais frequentes?
# Este é um notebook para
# exploração inicial do texto dos documentos municipais.
# Atualmente só mostra as palavras mais frequentes,
# mas há outras análises interessantes.
#
# O exemplo é com as Leis Municipais,
# porém qualquer documento oficial pode ser carregado
# para realizar a mesma análise.
#
# ### Algumas ideias para melhorar esse notebook:
#
# - Separar os documentos por tópicos,
# usando Latent Semantic Analysis (LSA) ou LDA, por exemplo,
# e calcular a frequência de palavras pra cada tópico
# - Separar entidades (nome de pessoas, ruas) das outras palavras
# - Rodar o Part of Speech Tagging (POS Tagging) do Spacy
# e calcular frequências para cada categoria
# (substantivo, adjetivo, etc)
#
# ### Algumas referências para ideias e melhorias:
#
# - [Como criar nuvem de palavras](https://medium.com/turing-talks/introdu%C3%A7%C3%A3o-ao-processamento-de-linguagem-natural-com-baco-exu-do-blues-17cbb7404258)  # noqa
# - [Explore 175 Years of Words in Scientific American](https://www.scientificamerican.com/article/explore-175-years-of-words-in-scientific-american/)  # noqa
# e
# [How to Turn 175 Years of Words in Scientific American into an Image](https://www.scientificamerican.com/article/how-to-turn-175-years-of-words-in-scientific-american-into-an-image/)   # noqa
# - [Tutorial de visualização de informações textuais](https://infovis.fh-potsdam.de/tutorials/infovis5text.html)  # noqa
# - [Tutorial de análise exploratória de texto](https://towardsdatascience.com/a-complete-exploratory-data-analysis-and-visualization-for-text-data-29fb1b96fb6a)   # noqa
# - [Análise dos tweets do congresso americano](https://congress.pudding.cool/)   # noqa

# ## Pré-requisitos
#
# Para rodar este notebook,
# você precisa de um conjunto de textos (corpus).
#
# Atualmente usamos o corpus das Leis Municipais,
# presente no arquivo `leis.json`,
# disponível [no Kaggle](https://www.kaggle.com/anapaulagomes/leis-do-municpio-de-feira-de-santana/).   # noqa

# In[1]:


import re
from collections import Counter

import matplotlib.pyplot as plt
import nltk
import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords

# In[2]:


city_laws = pd.read_json("leis.json")
city_laws.drop(["documento"], inplace=True, axis=1)
city_laws.describe()


# In[3]:


city_laws


# ### Abaixo um exemplo de uma lei do munícipio

# In[4]:


print(city_laws.iloc[len(city_laws) - 1, 3])


# ## Quais as palavras mais comuns?
#
# A seguir, geramos uma visualização
# das palavras mais comuns no texto das Leis.
# Algo que pode ser desenvolvido em uma núvem de palavras.
#
# A ideia é descobrir palavras chave recorrente nas Leis.
# Sobre o que falam nossas Leis Municiapis?

# In[5]:


nltk.download("stopwords")


# In[6]:


def clean_text(text):
    if not isinstance(text, str):
        raise ValueError(f"Esperava string, recebido {type(text)}")

    # Remove pontuação, dígitos e espaços em branco
    text = re.findall(r"[A-Za-zÀ-ú]+[-A-Za-zÀ-ú]*", text.lower())

    # Remove stopwords
    return [word for word in text if word not in stopwords.words("portuguese")]


# In[7]:


text = " ".join(city_laws["texto"].tolist())
text = clean_text(text)

unique_words_count = len(set(text))
print(f"Número de palavras únicas no texto: {unique_words_count}")


# ## Removendo stopwords
#
# Stopwords são palavras a serem removidas na etapa de
# pré-processamento do texto. Em geral são palavras muito
# comuns, utilizadas em quase todos os textos,
# ou não possuem valor descritivo do que diz o texto.
#
# Em ambos os casos, não possuem informação sobre o que trata
# o texto, que é o que a gente quer visualizar com a
# frequencia das palavras do texto.
#
# O método `clean_text` já remove algumas stopwords
# padrões do português, como preposições, artigos, etc:
# ("de", "a", "este").
#
# Utilizamos o módulo Counter do Python para visualizar
# as palavras mais comuns nos textos das Leis
# e decidir se elas possuem valor semântico ou não.
# Isto é, se descrevem o conteúdo do texto ou não.
# As palavras que não possuirem,
# incluímos na lista de stopwords, palavras a serem
# removidas.

# In[8]:


counter_ = Counter(text)
counter_.most_common(100)


# ### Selecionando as stopwords
#
# Palavras como:
# 'art' (artigo),
# 'municipal',
# 'lei',
# 'rua',
# 'feira',
# 'santana',
# 'prefeito',
# 'câmara',
# 'município',
# 'publicação',
# 'seguinte',
# 'disposições',
# 'estado',
# 'bahia',
# 'vigor',
# aparecem em quase todas as Leis, portanto
# elas não identificam bem o texto das Leis.
#
# Letras do alfabeto e números romanos, como:
# 'i', 'ii', 'iii',
# 'd', 'n', 'r'
# também aparecem bastante no texto das Leis
# e não possuem valor semântico. Também vamos
# remove-las.
#

# In[9]:


def remove_stopwords(text):
    custom_stopwords = [
        "feira",
        "santana",
        "art",
        "municipal",
        "lei",
        "r",
        "prefeito",
        "câmara",
        "município",
        "data",
        "seguinte",
        "disposições",
        "estado",
        "bahia",
        "vigor",
        "secretário",
        "decreto",
        "projeto",
        "iii",
        "i",
        "ii",
        "contrário",
        "presidente",
        "artigo",
        "rua",
        "faço",
        "parágrafo",
        "executivo",
        "gabinete",
        "único",
        "sanciono",
        "desta",
        "v",
        "iv",
        "autoria",
        "através",
        "deste",
        "vice",
        "autor",
        "qualquer",
        "b",
        "sobre",
        "das",
        "decorrentes",
        "fica",
        "dias",
        "resolução",
        "geral",
        "uso",
        "ato",
        "diretiva",
        "exercício",
        "seguintes",
        "meio",
        "m",
        "c",
        "d",
        "n",
        "correrão",
        "publicação",
    ]

    return [word for word in text if word not in custom_stopwords]


text = remove_stopwords(text)


# In[10]:


plt.figure(figsize=(20, 10))
fd = FreqDist(text)
fd.plot(30, title="Palavras x Frequência", cumulative=False)


# ## Analisando o resultado
#
# O que esperava era obter palavras comuns no
# texto das Leis que também descrevessem o conteúdo.
#
# Existem algumas palavras descritivas do conteúdo,
# por exemplo "revogadas", "secretaria", "serviços",
# "despesas", "social", "saúde",
# de certa forma descrevem o conteúdo das Leis.
#
# Aparecem alguns nomes próprios, como "José",
# "Silva", "Santos", "Carvalho". Nomes frequentes
# na base de dados. Os nomes do prefeito em exercício,
# do edil, presidente da câmara e outros cargos,
# frequentemente aparecem no texto das Leis.
# O que por exemplo explica os nomes José e Carvalho,
# que aparecem no nome do prefeito José Ronaldo de Carvalho,
# ganhador de 4 pleitos no município.
#
# No entanto apenas estas palavras não dão uma boa
# indicação sobre o conteúdo destas Leis. Por isso,
# sugerimos no começo deste notebook algumas técnicas
# para extração tópicos dos textos, bem como as
# palavras mais frequentes nestes tópicos.
# Possivelmente este procedimento retornará um
# resultado mais interpretável.
#
