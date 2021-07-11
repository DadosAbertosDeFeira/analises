#!/usr/bin/env python
# coding: utf-8

# # As denúncias ao TCM-BA
#
#
# Quanto tempo em média uma denúncia demora para ser julgada pelo Tribunal
# de Contas dos Municípios?
#
# Essa é a pergunta que queremos responder com esse notebook.
#
# ---
#
# A coleta de dados foi feita utilizando scripts do repositório
# [tcm-ba](https://github.com/DadosAbertosDeFeira/tcm-ba) em 17 de Julho de 2021.

# In[17]:


import pandas as pd
import seaborn as sns

df = pd.read_csv("processos-tcm-ba.csv")


# In[19]:


df.sample(3)


# In[21]:


df.shape


# In[6]:


df["nature"].unique()


# In[7]:


df["entry_at"] = pd.to_datetime(df["entry_at"], format="%d/%m/%Y")
df["last_update_at"] = pd.to_datetime(df["last_update_at"], format="%d/%m/%Y")


# In[8]:


df["interval_in_days"] = df["last_update_at"] - df["entry_at"]


# In[9]:


df[
    [
        "process_number",
        "description",
        "entry_at",
        "last_update_at",
        "interval_in_days",
        "nature",
        "city",
    ]
]


# In[10]:


df.groupby("nature")["interval_in_days"].describe()


# In[11]:


df["nature"].fillna("", inplace=True)
denuncias = df[df["nature"].str.contains("Denuncia")]
denuncias


# In[12]:


df["interval_in_days"] = df["interval_in_days"].apply(lambda x: x.days)


# In[13]:


ax = sns.barplot(y="nature", x="interval_in_days", data=df, orient="h")


# In[14]:


ax = sns.countplot(x="nature", data=df)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)


# In[15]:


ax = sns.countplot(x="city", data=denuncias)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)


# In[16]:


ax = sns.countplot(x="place_of_origin", data=denuncias)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
