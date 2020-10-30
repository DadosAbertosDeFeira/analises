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
# - [Como criar nuvem de palavras]
# (https://medium.com/turing-talks/introdu%C3%A7%C3%A3o-ao-processamento-de-linguagem-natural-com-baco-exu-do-blues-17cbb7404258)
# - [Explore 175 Years of Words in Scientific American]
# (https://www.scientificamerican.com/article/explore-175-years-of-words-in-scientific-american/)
# e [How to Turn 175 Years of Words in Scientific American into an Image]
# (https://www.scientificamerican.com/article/how-to-turn-175-years-of-words-in-scientific-american-into-an-image/)
# - [Tutorial de visualização de informações textuais]
# (https://infovis.fh-potsdam.de/tutorials/infovis5text.html)
# - [Tutorial de análise exploratória de texto]
# (https://towardsdatascience.com/a-complete-exploratory-data-analysis-and-visualization-for-text-data-29fb1b96fb6a)
# - [Análise dos tweets do congresso americano]
# (https://congress.pudding.cool/)

# ## Pré-requisitos
#
# Para rodar este notebook,
# você precisa de um corpus de texto.
#
# Atualmente usamos o corpus das Leis Municipais.
# Este corpus está presente no arquivo leis.json,
# disponível [no Kaggle]
# (https://www.kaggle.com/anapaulagomes/leis-do-municpio-de-feira-de-santana/).

# In[ ]:


import re
import unicodedata

import matplotlib.pyplot as plt
import nltk
import pandas as pd
from nltk import FreqDist
from nltk.corpus import stopwords

# In[ ]:


city_laws = pd.read_json("leis.json")
city_laws.drop(["documento"], inplace=True, axis=1)
city_laws.describe()


# In[ ]:


city_laws


# ### Abaixo um exemplo de uma lei do munícipio

# In[ ]:


print(city_laws.iloc[len(city_laws) - 1, 3])


# ## Quais as palavras mais comuns?
#
# A seguir, geramos uma visualização
# das palavras mais comuns no texto das Leis.
# Algo que pode ser desenvolvido em uma núvem de palavras.
#
# A ideia é descobrir palavras chave recorrente nas Leis.
# Sobre o que falam nossas Leis Municiapis?

# In[ ]:


nltk.download("stopwords")


# In[ ]:


def clean_text(text, remove_accents=False):
    if isinstance(text, float):
        return ""

    # Remove ponctuation, digits and whitespaces  # TODO documentação em pt-br
    text = " ".join(re.findall(r"[A-Za-zÀ-ú]+[-A-Za-zÀ-ú]*", text.lower()))

    # Remove accents
    if remove_accents:
        nfkd_form = unicodedata.normalize("NFKD", text)
        text = "".join([char for char in nfkd_form if not unicodedata.combining(char)])

    # Remove stopwords
    nltk_stopwords = stopwords.words("portuguese")
    custom_stopwords = [
        "feira",
        "santana",
        "art",
        "municipal",
        "lei",
        "r",
        "prefeito",
        "câmara",
        "municipio",
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
        "decretou",
        "execução",
        "sobre",
        "das",
        "decorrentes",
        "decreta",
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
        "correrão",
    ]
    all_stopwords = nltk_stopwords + custom_stopwords

    return [word for word in text.split() if word not in all_stopwords]


# In[ ]:


text = " ".join(city_laws["texto"].tolist())
text = clean_text(text)

unique_words_count = len(set(text))
print(f"Numero de palavras unicas no text: {unique_words_count}")


# In[ ]:


plt.figure(figsize=(20, 10))
fd = FreqDist(text)
fd.plot(30, title="Palavras x Frequência", cumulative=False)
