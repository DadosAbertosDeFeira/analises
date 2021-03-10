#!/usr/bin/env python
# coding: utf-8

# # Equipe : FlaRe análise
# # integrantes: Flávio Monteiro e Rejanio Moraes
# # email: rejaniomoraes@gmail.com
# ##### relatório explicativo da análise: https://docs.google.com/document/d/1aRzknUnMZdc_e3nqljTfou46NI-mL7rgYOyh1Bw2MAo/edit

# ### Análise: O crescimento educacional da população está relacionado com o crescimento do trabalho formal?
# 
# #### A análise começa investigando o nível educacional da mão de obra jovens com idade para trabalhar e a expectativa de anos de estudo. Depois foi analisada os índices de empregos formais, informais e o grau de formalização dos ocupados. Também o nível educacional da mão de obra que está trabalhando, o rendimento médio, redimento de até 1 salário mínimo.
# ###### Ps: Importante salientar que os dados disponíveis do munípicio foi do censo apenas do ano 1991, 2000 e 2010. E em alguns casos só tinha os dados do censo de 2010.
# ###### Os dados foram coletados do site: https://atlasbrasil.org.br/consulta/planilha

# In[6]:


import pandas as pd
import numpy as np


# In[8]:


# Dados da educação de Feira de Santana. Os anos usado nas análises foi do censo do ano 1991, 2000 e 2010 
# Infelizmente Feira de Santana não tem dados do PNAD - IBGE, pois não é capital e nem considerada 
# região metropolitana ainda.
dados_edu = pd.read_csv('../data/dados_edu.csv', sep=',')
dados_edu.set_index('Territorialidades',inplace = True)
dados_edu.drop(index = 'Brasil', inplace = True)


# In[9]:


dados_edu.head()


# In[5]:


#trocando , para . para ser transformado em float para análises 
for row , col in dados_edu.iterrows():
    aux = col.str.replace(',','.',regex=True)
    dados_edu.loc[row] = pd.to_numeric(aux)
dados_edu = dados_edu.astype(float)


# In[6]:


# Analisando dados da porcentagem de 18 anos ou mais de idade com ensino médio completo nos anos de 1991,2000 e 2010
aux = dados_edu[['% de 18 anos ou mais de idade com ensino médio completo 1991','% de 18 anos ou mais de idade com ensino médio completo 2000','% de 18 anos ou mais de idade com ensino médio completo 2010']]
aux


# In[7]:


grafico = aux.groupby(['Feira de Santana (BA)']).sum()


# In[24]:



ax = grafico.plot.bar()
ax.set_title("Porcentagem de 18 anos ou mais de idade com ensino médio completo nos anos de 1991, 2000 e 2010")
ax.legend(bbox_to_anchor=(1.2, 0.5))


# In[13]:


# Analisando dados da porcentagem de 25 anos ou mais de idade com ensino superior completo nos anos de 1991,2000 e 2010
aux = dados_edu[['% de 25 anos ou mais de idade com ensino superior completo 1991','% de 25 anos ou mais de idade com ensino superior completo 2000','% de 25 anos ou mais de idade com ensino superior completo 2010']]
aux


# In[ ]:


grafico = aux.groupby(['Feira de Santana (BA)']).sum()


# In[14]:


ax = grafico.plot.bar()
ax.set_title("Porcentagem de 25 anos ou mais de idade com ensino superior completo nos anos de 1991, 2000 e 2010")
ax.legend(bbox_to_anchor=(1.2, 0.5))


# In[10]:


# Dados do trabalho de feira de Santana. Os anos usado nas análises foi do censo do ano 2000 e 2010 
# Infelizmente Feira de Santana não tem dados do PNAD - IBGE, pois não é capital e nem considerada 
# região metropolitana ainda.
dados_trabalho = pd. read_csv('../data/dados_trabalho.csv', sep=',')

dados_trabalho.set_index('Territorialidades',inplace = True)
dados_trabalho.drop(index = 'Brasil', inplace = True)
dados_trabalho.head()


# In[11]:


#trocando , para . para ser transformado em float para análises 
for row , col in dados_trabalho.iterrows():
    aux = col.str.replace(',','.',regex=True)
    dados_trabalho.loc[row] = pd.to_numeric(aux)
dados_trabalho


# In[12]:


# convertendo todos os campos em float
dados_trabalho = dados_trabalho.replace(np.nan,0,regex=True)
dados_trabalho = dados_trabalho.astype(float)


# In[13]:


# Analisando dados da porcentagem de jovens a partir de 18 anos ocupados COM carteira assinada.
dados_aux = dados_trabalho[['% de ocupados de 18 anos ou mais de idade que são empregados com carteira 2000','% de ocupados de 18 anos ou mais de idade que são empregados com carteira 2010']]

dados_aux


# In[14]:


# gerando o gráfico para comparação

grafico = dados_aux.groupby(['Feira de Santana (BA)']).sum()

ax = grafico.plot.bar()

ax.set_title("Porcentagem de ocupados com mais de 18 naos COM carteira assinada")
ax.legend( bbox_to_anchor = (1.05, 1), loc = 0 , borderaxespad = 0.)


# In[7]:


# Analisando dados da porcentagem de jovens a partir de 18 anos ocupados SEM carteira assinada.
dados_aux = dados_trabalho[['% de ocupados de 18 anos ou mais de idade que são empregados sem carteira 2000','% de ocupados de 18 anos ou mais de idade que são empregados sem carteira 2010']]

dados_aux


# In[8]:


# gerando o gráfico para comparação
grafico = dados_aux.groupby(['Feira de Santana (BA)']).sum()

ax = grafico.plot.bar()

ax.set_title("Porcentagem de ocupados com mais de 18 naos SEM carteira assinada")
ax.legend( bbox_to_anchor = (1.05, 1), loc = 0 , borderaxespad = 0.)


# In[9]:


# Analisando dados do grau de formalização dos ocupados - 18 anos ou mais no ano 2000 e 2010
dados_aux = dados_trabalho[['Grau de formalização dos ocupados - 18 anos ou mais 2000','Grau de formalização dos ocupados - 18 anos ou mais 2010']]
dados_aux


# In[10]:


# gerando o gráfico para comparação
grafico = dados_aux.groupby(['Feira de Santana (BA)']).sum()

ax = grafico.plot.bar()

ax.set_title("Grau de formalização dos ocupados - 18 anos ou mais")
ax.legend( bbox_to_anchor = (1.05, 1), loc = 0 , borderaxespad = 0.)


# In[11]:


# Analisando dados da porcentagem  dos ocupados com ensino médio completo no ano 2000 e 2010
dados_aux = dados_trabalho[['% dos ocupados com ensino médio completo 2000','% dos ocupados com ensino médio completo 2010']]
dados_aux


# In[12]:


# gerando o gráfico para comparação
grafico = dados_aux.groupby(['Feira de Santana (BA)']).sum()

ax = grafico.plot.bar()

ax.set_title(" Porcentagem dos ocupados com ensino médio completo")
ax.legend( bbox_to_anchor = (1.05, 1), loc = 0 , borderaxespad = 0.)


# In[13]:


# Analisando dados da porcentagem  dos ocupados com ensino superior completo do 2000  e 2010
dados_aux = dados_trabalho[['% dos ocupados com ensino superior completo 2000','% dos ocupados com ensino superior completo 2010']]
dados_aux


# In[14]:


# gerando o gráfico para comparação
grafico = dados_aux.groupby(['Feira de Santana (BA)']).sum()

ax = grafico.plot.bar()

ax.set_title("Porcentagem dos ocupados com ensino superior completo")
ax.legend( bbox_to_anchor = (1.05, 1), loc = 0 , borderaxespad = 0.)


# In[20]:


# Analisando dados  de rendimento médio dos ocupados do ano 2010, pois o ano 2000 não teve dado.
# No ano de 2010 o salário mínimo era de R$ 510,00
dados_aux = dados_trabalho[['Rendimento médio dos ocupados 2010']]
dados_aux


# In[22]:


# gerando o gráfico para comparação
grafico = dados_aux.groupby(['Feira de Santana (BA)']).sum()

ax = grafico.plot.bar()

ax.set_title("Rendimento médio dos ocupados")
ax.legend( bbox_to_anchor = (1.05, 1), loc = 0 , borderaxespad = 0.)


# In[23]:


# Analisando dados de porcentagem dos ocupados com rendimento de até 1 salário mínimo do ano 2000 e 2010 
dados_aux = dados_trabalho[['% dos ocupados com rendimento de até 1 salário mínimo 2000','% dos ocupados com rendimento de até 1 salário mínimo 2010']]
dados_aux


# In[24]:


# gerando o gráfico para comparação
grafico = dados_aux.groupby(['Feira de Santana (BA)']).sum()

ax = grafico.plot.bar()

ax.set_title("Porcentagem dos ocupados com rendimento de até 1 salário mínimo")
ax.legend( bbox_to_anchor = (1.05, 1), loc = 0 , borderaxespad = 0.)


# In[25]:


# Analisando dados de porcentagem  dos ocupados com rendimento de até 2 salários mínimo do ano 2000 e 2010
dados_aux = dados_trabalho[['% dos ocupados com rendimento de até 2 salários mínimo 2000','% dos ocupados com rendimento de até 2 salários mínimo 2010']]
dados_aux


# In[26]:


# gerando o gráfico para comparação
grafico = dados_aux.groupby(['Feira de Santana (BA)']).sum()

ax = grafico.plot.bar()

ax.set_title("Porcentagem dos ocupados com rendimento de até 2 salário mínimo")
ax.legend( bbox_to_anchor = (1.05, 1), loc = 0 , borderaxespad = 0.)

