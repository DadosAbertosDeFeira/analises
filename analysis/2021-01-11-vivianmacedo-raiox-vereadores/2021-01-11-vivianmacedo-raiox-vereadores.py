# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd


# %%
data = pd.read_csv('vereadores_feira.csv')


# %%
data.sample(2).T


# %%
(data['resultado'].unique())


# %%
status_eleito = ['eleito por media', 'eleito por qp']

eleitos = data[data['resultado'].isin(status_eleito)]
eleitos.sample(2)


# %%
reeleitos = pd.pivot_table(eleitos, values='votos', index=['cpf'], columns=['ano'], aggfunc='count', margins=True)
reeleitos


# %%
reeleitos.sort_values(by=('All'), ascending = False)
# Foram 8 vereadores reeleitos em Feira de Santana


# %%
instrucao_group = eleitos.groupby(['instrucao', 'ano'])
instrucao_group.size().unstack()
# Foram mais vereadores com ensino superio completo eleitos em 2020


# %%
superior_completo = ['ensino superior completo']
ultima_eleicao = [2020]
candidatos_superior = eleitos[eleitos['instrucao'].isin(superior_completo)]
candidatos_superior_2020 = candidatos_superior[candidatos_superior['ano'].isin(ultima_eleicao)]

candidatos_superior_2020[['nome_urna_candidato', 'instrucao', 'ocupacao']] 
# Aqui podemos ver as ocupacoes dos vereadores eleitos em 2020 com ensino superior completo


# %%
eleitos_2020 = eleitos[eleitos['ano'].isin(ultima_eleicao)]
eleitos_2020['ocupacao'].value_counts()
#A ocupacao mais frequente entre os eleitos é ser vereador


# %%
genero_group = eleitos.groupby(['genero', 'ano'])
genero_group.size().unstack()


# %%
raca_group = eleitos.groupby(['raca', 'ano'])
raca_group.size().unstack()


# %%
raca_genero_group = eleitos.groupby(['raca', 'genero', 'ano'])
raca_genero_group.size().unstack()


# %%
idade_2020 = eleitos_2020['idade']
idade_2020.describe()
# A média de idade dos eleitos é 49 anos. O mais novo possui 34 anos, o mais velho 65 anos


# %%
eleicao_anterior = [2016]
eleitos_2016 = eleitos[eleitos['ano'].isin(eleicao_anterior)]


idade_2016 = eleitos_2016['idade']
idade_2016.describe()

# A média na eleição de 2016 foi 49 anos. O mais novo foi eleitos com 31 anos e o meis velho com 63 anos.


# %%



