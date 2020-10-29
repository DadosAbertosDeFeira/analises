#!/usr/bin/env python
# coding: utf-8

# # Buscador
#
# Esse notebook implementa um buscador simples.
# A representação pra cada texto é criada a partir da TF-IDF.
# A representação da query (consulta, ou termos buscados)
# é construída a partir do vocabulário dos textos.
# O ranqueamento dos resultados é feito de acordo com
# a semelhança cosseno da query pros textos.
#
# Há várias oportunidades de melhoria.
# Algumas delas são discutidas ao longo do notebook.
#
# Os resultados, mesmo deste buscador ingênuo,
# são bastante satisfatórios.
# O buscador é capaz de retornar leis (neste caso)
# relacionadas à localidades ou personalidades.
# No entanto, o mesmo mecanismo pode ser utilizado
# pra quaisquer outros textos, por exemplo o Diário Oficial.
# Alguns exemplos de buscas são:
#
# "winterianus" - retorna a Lei Municipal sobre citronelas;
#
# "Elydio Azevedo" - retorna Lei Municipal que concede título de cidadão feirense;
#
# "Rua Espassonavel" - retorna Lei Municipal que cita a rua.

# In[6]:


import numpy as np
import pandas as pd
from scripts.parsers import clean_text
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

# In[7]:


laws = pd.read_json("leis.json")
laws.drop(["documento"], inplace=True, axis=1)
print(laws.info())
print(laws.nunique())


# In[8]:


laws


# In[9]:


print(laws.loc[len(laws) - 1, "texto"])


# # Buscas por texto
#
# No notebook _similar_laws_ vimos que TF-IDF encontra Leis bastante similares entre si.
# Será que conseguimos também encontrar leis similares a uma query?
#
# Primeiro, devemos construir a representação das leis com TF-IDF.
# Após termos as representações,
# limpamos o texto da consulta utilizando o mesmo método de limpeza das leis.
# Depois, criar uma representação da consulta utilizando o IDF do modelo treinado.
# Finalmente, calcular a similaridade desta consulta
# para todas as leis na base e retornar as mais próximas.

# In[5]:


laws["texto_limpo"] = laws["texto"].apply(clean_text)


# In[6]:


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(laws["texto_limpo"])
X


# In[7]:


transformer = TfidfTransformer()
X_tfidf = transformer.fit_transform(X)

X_tfidf


# In[21]:


query = ["rua espassonavel"]
query[0] = clean_text(query[0])
query = vectorizer.transform(query)
query = transformer.transform(query)


# In[18]:


best_matches = cosine_similarity(query, X_tfidf)
best_matches_idx = np.argsort(best_matches)
for i in range(1, 5):
    idx = best_matches_idx[0, -i]
    print(laws.loc[idx, "texto"])
    print("\n---Next Result:---\n")


# Tcharam! Feito um buscador simples!
#
# Existem limitações.
# A sequência e composição das palavras é uma delas, por exemplo.
# Não adianta buscar pelo nome - sobrenome de uma pessoa.
# Ele vai retornar resultados onde
# algum destes termos sejam mais frequentes.
# Não existe as aspas do Google pra dizer
# "busque por este termo todo junto".
#
# Por exemplo, se eu buscar Elydio,
# o primeiro resultado é a Lei conferindo
# cidadania à Elydio Azevedo Lopes.
# Perfeito.
# Mas se eu buscar Azevedo Lopes,
# o primeiro resultado sequer tem Azevedo,
# mas o nome Lopes aparece mais de uma vez.
#
# Uma das formas de contornar essa dificuldade é
# usar bigramas ou n-gramas maiores.
#

# ## Outras opções
# ### Indexar
# Há outras formas de indexar os documentos
# e de recuperar, também simples.
# Uma outra forma de indexar, por exemplo,
# é fazer um vetor pra cada palavra
# contando as palavras vizinhas.
# E depois, o vetor do documento seria
# a soma dos vetores das palavras.
# É uma forma interessante porque
# pode gerar visualizações interessantes
# entre a similaridade das palavras.
# Por exemplo, no corpus das Leis Municipais,
# a quais palavras EDUCAÇÃO mais se assemelha?
# Ou SAÚDE? Etc.
#
# Outra forma é contar n-gramas - por exemplo,
# bi-gramas: duas palavras juntas formando um token.
# Dessa forma, você possui uma matriz maior
# e de certa forma uma relação entre a sequencialidade das palavras,
# que pode ser útil pra nomes de pessoas e bairros,
# como citado acima.
#
# ### Recuperar
# Outra forma de recuperar é por
# _local sensitive hashing_.
# Divide em vários planos múltiplas vezes
# e retorna os resultados que estão na mesma região da query.
# No entanto,
# o corpus não é grande o suficiente pra precisar essa estratégia,
# que é mais pra grandes corpora.
# O método acima
# (calcular a simlaridade cosseno e retornar os maiores valores)
# é rápido o suficiente pra parecer instantâneo.
# Talvez com uma demanda mais alta pelo servidor
# venha a necessidade de aumentar a velocidade da busca,
# porém por enquanto não é o caso.
#
# Há ainda um [novo método]
# (https://ai.googleblog.com/2020/07/announcing-scann-efficient-vector.html)
# e uma lib pra isso,
# lançada pelo Google recentemente,
# no dia 28 de Julho de 2020.
#
# ### Avaliação
# Com múltiplas formas de indexar e recuperar vem o dilema:
# como avaliar se uma é melhor que a outra?
# Repetir o processo acima pra todas as opções?
# Isto é, mostrar N melhores resultados e comparar manualmente?
# Ou colocar labels em algumas leis?
# Ex: essa lei trata disso, com tais entidades.
# Checar formas de avaliação.
# Se tivesse em produção,
# poderiamos avaliar por _click through rate_ (CTR) por ex,
# mas não é o caso
