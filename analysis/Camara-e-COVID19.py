#!/usr/bin/env python
# coding: utf-8

# # A Câmara de Vereadores e o COVID-19
# 
# Você também fica curioso(a) para saber o que a Câmara de Vereadores
# de Feira de Santana fez em relação ao COVID-19? O que discutiram?
# O quão levaram a sério o vírus? Vamos responder essas perguntas e
# também te mostrar como fazer essa análise. Vem com a gente!
# 
# Desde o início do ano o mundo tem falado a respeito do COVID-19.
# Por isso, vamos basear nossa análise no período de 1 de Janeiro
# a 27 de Março de 2020. Para entender o que se passou na Câmara
# vamos utilizar duas fontes de dados:
# 
# * [Diário Oficial](diariooficial.feiradesantana.ba.gov.br/)
# * [Atas das sessões](https://www.feiradesantana.ba.leg.br/atas)
# 
# Nas atas temos acesso ao que foi falado nos discursos e no Diário
# Oficial temos acesso ao que realmente virou (ou não) lei. Você
# pode fazer _download_ dos dados [aqui]()
# e [aqui](https://www.kaggle.com/anapaulagomes/dirios-oficiais-de-feira-de-santana).
# Procuramos mas não foi encontrada nenhuma menção ao vírus na
# [Agenda da Câmara Municipal](https://www.feiradesantana.ba.leg.br/agenda).
# 
# Lembrando que as atas foram disponibilizadas no site da casa apenas
# depois de uma reunião nossa com o presidente em exercício José Carneiro.
# Uma grande vitória dos dados abertos e da transparência na cidade.
# 
# Os dados são coletados por nós e todo código está [aberto e disponível
# no Github](https://github.com/DadosAbertosDeFeira/maria-quiteria/).
# 
# ## Vamos começar por as atas
# 
# As atas trazem uma descrição do que foi falado durante as sessões.
# Se você quer acompanhar o posicionamento do seu vereador(a), é uma
# boa maneira. Vamos ver se encontramos alguém falando sobre *coronavírus*
# ou *vírus*.
# 
# Se você não é uma pessoa técnica, não se preocupe. Vamos continuar o texto
# junto com o código.

# In[47]:


import pandas as pd


# esse arquivo pode ser baixado aqui: https://www.kaggle.com/anapaulagomes/atas-da-cmara-de-vereadores
atas = pd.read_csv('atas-28.03.2020.csv')
atas.describe()


# Explicando um pouco sobre os dados (colunas):
# 
# * `crawled_at`: data da coleta
# * `crawled_from`: fonte da coleta (site de onde a informação foi retirada)
# * `date`: data da sessão
# * `event_type`: tipo do evento: sessão ordinária, ordem do dia, solene, etc
# * `file_content`: conteúdo do arquivo da ata
# * `file_urls`: url(s) do arquivo da ata
# * `title`: título da ata
# 
# ### Filtrando por data
# 
# Bom, vamos então filtrar os dados e pegar apenas as atas entre 1 de Janeiro
# e 28 de Março:

# In[48]:


atas["date"] = pd.to_datetime(atas["date"])
atas["date"]
atas = atas[atas["date"].isin(pd.date_range("2020-01-01", "2020-03-28"))]
atas = atas.sort_values('date', ascending=True)  # aqui ordenados por data em ordem crescente
atas.head()


# Bom, quantas atas temos entre Janeiro e Março?

# In[49]:


len(atas)


# Apenas 21 atas, afinal os trabalhos na casa começaram no início de Fevereiro
# e pausaram por uma semana por conta do coronavírus.
# 
# Fonte:
# https://www.feiradesantana.ba.leg.br/agenda
# https://www.feiradesantana.ba.leg.br/noticia/2029/c-mara-municipal-suspende-sess-es-ordin-rias-da-pr-xima-semana
# 
# ### Filtrando conteúdo relacionado ao COVID-19
# 
# Agora que temos nossos dados filtrados por data, vamos ao conteúdo.
# Na coluna `file_content` podemos ver o conteúdo das atas. Nelas vamos
# buscar por as palavras:
# 
# - COVID, COVID-19
# - coronavírus, corona vírus

# In[50]:


termos_covid = "COVID-19|coronavírus"
atas = atas[atas['file_content'].str.contains(termos_covid, case=False)]
atas


# In[51]:


len(atas)


# Doze atas mencionando termos que representam o COVID-19 foram encontradas.
# Vamos ver o que elas dizem?
# 
# Atenção: o conteúdo das atas é grande para ser mostrado aqui. Por isso vamos
# destacar as partes que contém os termos encontrados.

# In[52]:


import re

padrao = r'[A-Z][^\\.;]*(coronavírus|covid)[^\\.;]*'


def trecho_encontrado(conteudo_do_arquivo):
    frases_encontradas = []
    for encontrado in re.finditer(padrao, conteudo_do_arquivo, re.IGNORECASE):
        frases_encontradas.append(encontrado.group().strip().replace('\n', ''))
    return '\n'.join(frases_encontradas)

atas['trecho'] = atas['file_content'].apply(trecho_encontrado)
pd.set_option('display.max_colwidth', 100)

atas[['date', 'event_type', 'title', 'file_urls', 'trecho']]


# Já que não temos tantos dados assim (apenas 12 atas) podemos fazer parte dessa análise manual,
# para ter certeza que nenhum vereador foi deixado de fora. Vamos usar o próximo comando
# para exportar os dados para um novo CSV. Nesse CSV vai ter os dados filtrados por data
# e também o trecho, além do conteúdo da ata completo.

# In[53]:


def converte_para_arquivo(df, nome_do_arquivo):
    conteudo_do_csv = df.to_csv(index=False)  # convertemos o conteudo para CSV
    arquivo = open(nome_do_arquivo, 'w')  # criamos um arquivo
    arquivo.write(conteudo_do_csv)
    arquivo.close()

converte_para_arquivo(atas, 'analise-covid19-atas-camara.csv')


# ### Quem levantou a bola do COVID-19 na Câmara?
# 
# Uma planilha com a análise do quem-disse-o-que pode ser encontrada [aqui](https://docs.google.com/spreadsheets/d/1h7ioFnHH8sGSxglThTpQX8W_rK9cgI_QRB3u5aAcNMI/edit?usp=sharing).

# ## E o que dizem os diários oficiais?
# 
# No diário oficial do município você encontra informações sobre o que virou
# realidade: as decretas, medidas, nomeações, vetos.
# 
# Em Feira de Santana os diários dos poderes executivo e legislativo estão juntos.
# Vamos filtrar os diários do legislativo, separar por data, como fizemos com as
# atas, e ver o que foi feito.

# In[54]:


# esse arquivo pode ser baixado aqui: https://www.kaggle.com/anapaulagomes/dirios-oficiais-de-feira-de-santana
diarios = pd.read_csv('gazettes-28.03.2020.csv')
diarios = diarios[diarios['power'] == 'legislativo']

diarios["date"] = pd.to_datetime(diarios["date"])
diarios = diarios[diarios["date"].isin(pd.date_range("2020-01-01", "2020-03-28"))]
diarios = diarios.sort_values('date', ascending=True)  # aqui ordenados por data em ordem crescente

diarios.head()


# O que é importante saber sobre as colunas dessa base de dados:
# 
# * `date`: quando o diário foi publicado
# * `power`: poder executivo ou legislativo (sim, os diários são unificados)
# * `year_and_edition`: ano e edição do diário
# * `events`:
# * `crawled_at`: quando foi feita essa coleta
# * `crawled_from`: qual a fonte dos dados
# * `file_urls`: url dos arquivos
# * `file_content`: o conteúdo do arquivo do diário
# 
# Vamos filtrar o conteúdo dos arquivos que contém os termos relacionados ao COVID-19
# (os mesmos que utilizamos com as atas).

# In[55]:


diarios = diarios[diarios['file_content'].str.contains(termos_covid, case=False)]
diarios['trecho'] = diarios['file_content'].apply(trecho_encontrado)

diarios[['date', 'power', 'year_and_edition', 'file_urls', 'trecho']]


# Apenas 4 diários com menção ao termo, entre 1 de Janeiro e 28 de Março de 2020
# foram encontrados. O que será que eles dizem? Vamos exportar os resultados para
# um novo CSV e continuar no Google Sheets.

# In[56]:


converte_para_arquivo(diarios, 'analise-covid19-diarios-camara.csv')


# ### O que encontramos nos diários
# 
# Os 4 diários tratam de suspender licitações por conta da situação na cidade.
# Apenas um dos diários, o diário do dia 17 de Março de 2020, [Ano VI - Edição Nº 733](http://www.diariooficial.feiradesantana.ba.gov.br/atos/legislativo/2CI2L71632020.pdf),
# traz instruções a respeito do que será feito na casa. Aqui citamos o trecho que fala
# a respeito das medidas:
# 
# > Art.  1º **Qualquer  servidor,  estagiário,  terceirizado,  vereador  que  apresentar  febre  ou  sintomas  respiratórios  (tosse  seca,  dor  de garganta,  mialgia,  cefaleia  e  prostração,  dificuldade  para  respirar  e  batimento  das  asas  nasais)  passa  a  ser  considerado  um  caso suspeito e deverá notificar imediatamente em até 24 horas à Vigilância Sanitária Epidemiológica/Secretaria Municipal de Saúde**.
# § 1ºQualquer servidor, estagiário, terceirizado, a partir dos 60 (sessenta)anos; portador de doença crônica e gestante estarão liberados das atividades laborais na Câmara Municipal de Feira de Santana sem prejuízo a sua remuneração.
# § 2º A(o) vereador(a) a partir dos 60 (sessenta)anos; portador de doença crônica e gestante será facultado as atividades laborais na Câmara Municipal de Feira de Santana sem prejuízo a sua remuneração
# § 3º Será  considerado  falta  justificada  ao  serviço  público  ou  à  atividade  laboral  privada  o  período  de  ausência  decorrente de afastamento por orientação médica.
# 
# > Art. 2º **Fica interditado o elevador no prédio anexo por tempo indeterminado**, até que sejam efetivamente contida a propagação do Coronavírus no Município e estabilizada a situação. _Parágrafo único_ O uso do elevador nesse período só será autorizado para transporte de portadores de necessidades especiais, como cadeirantes e pessoas com mobilidade reduzida.
# 
# > Art. 3º Será liberada a catraca para acesso ao prédio anexo. 
# 
# > Art. 4º O portãolateral (acesso a rua do prédio anexo) será fechado com entrada apenas pela portaria principal.
# 
# > Art. 5º Será disponibilizado nas áreas comuns dispensadores para álcool em gel.
# 
# > Art.6º Será  intensificada  a  limpeza  nos  banheiros,  elevadores,  corrimãos,  maçanetase  áreas  comuns  com  grande  circulação de pessoas.
# 
# > Art.7º Na cozinha e copa só será permitido simultaneamente à permanência de uma pessoa. 
# 
# > Art. 8º **Ficam suspensas as Sessões Solenes, Especiais e Audiências Públicas por tempo indeterminado**, até que sejam efetivamente contida a propagação do Coronavírus no Município e estabilizada a situação. 
# 
# > Art. 9º Nesse período de contenção é recomendado que o público/visitante assista a Sessão Ordinária on-line via TV Câmara. Parágrafo - Na  Portaria  do  Prédio  Sede  **haverá  um  servidor  orientando  as  pessoas  a  assistirem  os  trabalhos  legislativos  pela  TV Câmara** disponível  em https://www.feiradesantana.ba.leg.br/  distribuindo  panfletos  informativos  sobre  sintomas  e  métodos  de prevenção.
# 
# > Art. 10º No âmbito dos gabinetes dos respectivos Vereadores, **fica a critério de cada qual adotar restrições ao atendimento presencial do público externo ou visitação à sua respectiva área**.
# 
# > Art.11º A Gerência Administrativa fica autorizada a adotar outras providências administrativas necessárias para evitar a propagação interna do vírus COVID-19, devendo as medidas serem submetidas ao conhecimento da Presidência.
# 
# > Art.12º A validade desta Portaria será enquanto valer oestado de emergência de saúde pública realizado pela Secretaria Municipal de Saúde e pelo Comitê de Ações de Enfrentamento ao Coronavírus no Município de Feira de Santana.
# 
# > Art.13º Esta Portaria entra em vigor na data de sua publicação, revogadas disposições em contrário.
# 

# ## Conclusão
# 
# Caso os edis da casa tenham feito mais nós não teríamos como saber sem ser por as atas,
# pelo diário oficial ou por notícias do site. O ideal seria ter uma página com projetos
# e iniciativas de cada vereador. Dessa forma, seria mais fácil se manter atualizado a
# respeito do trabalho de cada um na cidade.
# 
# As análises manuais e o que encontramos pode ser visto [aqui](https://docs.google.com/spreadsheets/d/1h7ioFnHH8sGSxglThTpQX8W_rK9cgI_QRB3u5aAcNMI/edit?usp=sharing).
# Um texto sobre a análise e as descobertas podem ser encontradas no blog do [Dados Abertos de Feira](https://medium.com/@dadosabertosdefeira).
# 
# Gostou do que viu? Achou interessante? Compartilhe com outras pessoas e não esqueça de mencionar
# o projeto.

# In[ ]:




