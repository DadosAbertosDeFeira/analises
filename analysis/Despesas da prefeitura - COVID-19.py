#!/usr/bin/env python
# coding: utf-8

# # A prefeitura e os seus gastos declarados no combate a COVID-19
# 
# http://www.transparencia.feiradesantana.ba.gov.br/index.php?view=covid19
# 

# In[88]:


import pandas as pd
import matplotlib.pyplot as plt


despesas = pd.read_csv('gastos-covid19-prefeitura.csv')
despesas.head()


# In[89]:


colunas = ['crawled_at', 'crawled_from']
despesas.drop(colunas, inplace=True, axis=1)


def currency_to_float(value):
    """Converte de R$ 69.848,70 (str) para 69848.70 (float)."""
    try:
        cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
        return float(cleaned_value)
    except ValueError:
        pass
    return

despesas['value'] = despesas['value'].apply(currency_to_float)

despesas = despesas.sort_values('date', ascending=False)
despesas.head()


# In[90]:


# disponível em: https://gist.github.com/anapaulagomes/379525586f941a1183aa448dad282f90#file-especificacao-despesas-tcm-bahia-csv

classificacao = pd.read_csv(
    'especificacao-despesas-tcm-bahia.csv',
    dtype={'Codigo': str, 'Descricao': str, 'Codigo Superior': str}
)
classificacao


# In[91]:


despesas['classificacao'] = despesas['group'].str.extract('(\d{8})')

despesas_com_classificacao = despesas.merge(classificacao, left_on=['classificacao'], right_on=['Codigo'], how='left')
despesas_com_classificacao


# In[92]:


despesas.shape, despesas_com_classificacao.shape


# In[93]:


despesas.groupby('process_number').count()

despesas.groupby(['process_number', 'phase'])['value'].sum().to_frame()


# In[94]:


import seaborn as sns
sns.set_style("whitegrid")


# In[95]:


pagamentos = despesas_com_classificacao[despesas_com_classificacao['phase'] == 'PAGAMENTO']

plt.figure(figsize=(16,8))
plot = sns.barplot(
    x=pagamentos['Descricao'],
    y=pagamentos.value,
    estimator=sum,
    log=False,
    ci=None,
)
plot.set_xticklabels(plot.get_xticklabels(), rotation=75, horizontalalignment='right')
plt.ticklabel_format(style='plain', axis='y')
plt.show()


# In[96]:


pagamentos.groupby(
    ['company_or_person']
)['value'].sum().to_frame()


# In[97]:


pagamentos.groupby(
    ['Descricao']
)['value'].sum().to_frame()


# In[98]:


print(pagamentos.describe())

# 64 pagamentos. Menor: 375 Maior: 365380.00
# Total: 2.244.342,32

print(pagamentos['value'].sum())


# In[99]:


# despesas_com_classificacao.to_csv('despesas-covid19-prefeitura.csv')
# https://drive.google.com/file/d/1SAkAuGuOnuBTC5KT133lJhsYCm40Hfxc/view?usp=sharing

