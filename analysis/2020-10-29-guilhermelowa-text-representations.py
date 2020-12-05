#!/usr/bin/env python
# coding: utf-8

# # Semelhança de documentos
#
# A função desse notebook é criar representações para o texto dos documentos,
# exibir textos semelhantes e com isso avaliar as representações.
# Os textos semelhantes são um teste para a representação do texto:
# se os textos mostrados não são semelhantes, então a representação não é boa;
# se são semelhantes, então a representação pode ser boa.
#
# ## Dados
#
# Este notebook é um template genérico para comparação de textos.
# Utilizamos o dataset das leis municipais, disponível
# [aqui](https://www.kaggle.com/anapaulagomes/leis-do-municpio-de-feira-de-santana/).
#

# In[ ]:


import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from scripts.parsers import clean_text
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

# In[ ]:


laws_file = "leis.json"

# Descomente pra usar no Google Colab
# from google.colab import files
# import os.path


# if (not os.path.isfile(laws_file)):
#     uploaded = files.upload()


# In[ ]:


laws = pd.read_json(laws_file)
laws.drop(["documento"], inplace=True, axis=1)
laws.describe().T


# In[ ]:


laws.sample(10)


# In[ ]:


def print_law(law_idx):
    print(f"LEI {law_idx}:\n\n")
    print(laws.loc[law_idx, "texto"])


# In[ ]:


# Exemplo de texto de lei
print_law(len(laws) - 1)


# ## Comparando documentos: representação e calculo de similaridade
#
# Para comparar quão parecido são dois documentos,
# primeiro temos que transformar estes documentos
# para uma representação que o computador consiga calcular alguma coisa a respeito.
# Existem alguns métodos para isto.
# Neste notebook temos 3: TF, TF-IDF e vetores de palavras.
# Para calcular a similaridade, também existem alguns métodos diferentes.
# Utilizamos similaridade do cosseno.
#
# ### Term Frequency (TF)
#
# A primeira representação construída é bastante ingênua:
# apenas conta a quantidade de vezes que cada palavra apareceu em cada texto
# e atribui um vetor pra esse texto.
# Cada posição do vetor é uma palavra
# e cada valor representa quantas vezes essa palavra apareceu no dado texto.
# Todos os textos, portanto, são representados por uma matriz
# de dimensões _m_ x _n_, onde _m_ é o número de textos
# e _n_ é o número de palavras únicas (tamanho do vocabulário).

# In[ ]:


laws["texto_limpo"] = laws["texto"].apply(clean_text)


# In[ ]:


# Gera matriz de documentos
vectorizer = CountVectorizer()
tf_representation = vectorizer.fit_transform(laws["texto_limpo"])
tf_representation


# Com a matriz de documentos ~~literalmente~~ em mãos,
# vamos calcular a similaridade entre dois textos.
# A similaridade é calculada pela similaridade do cosseno (ver algebra linear).
# Existem outras medidas pra calcular similaridade / distância.
# Uma discussão sobre isso [aqui](https://cmry.github.io/notes/euclidean-v-cosine).

# In[ ]:


cos_sim_matrix = cosine_similarity(tf_representation, dense_output=True)

# ordenando de forma crescente, por linha,
# os índices dos documentos de acordo com
# a medida de distância (similaridade cosseno)
cos_sim_argsort = np.argsort(cos_sim_matrix)


# In[ ]:


# -1 é o mais similar (o mesmo texto)
most_similar_indexes_tf = cos_sim_argsort[:, -2]
tf_similarities = [
    cos_sim_matrix[i, ind] for i, ind in enumerate(most_similar_indexes_tf)
]


# In[ ]:


max_sim_overall = np.max(tf_similarities)
print(f"Maior similaridade entre duas Leis: {max_sim_overall}")

original_law_index = np.argmax(tf_similarities)
most_similar_law_index = most_similar_indexes_tf[original_law_index]

print(f"Leis mais similares:\n")
print_law(original_law_index)
print_law(most_similar_law_index)


# As leis 5949 e 6026 são idênticas.
# Opa! Lei 13 e Lei 118 são a mesma lei, com 3 dias de diferença. Por que existe isso?
# Uma boa investigação pra fazer.

# ### TF-IDF
#
# Outra representação possível para os textos é TF-IDF.
# Ainda contamos a frequência de cada termo (TF),
# porém ponderamos esta frequência pela raridade da palavra,
# medida pela frequência inversa que ela aparece nos documentos
# (Inverse Document Frequency).
# Ou seja, quanto mais rara é a palavra no corpus,
# mais ela caracteriza o texto em que ela aparece, maior será o peso dela.

# In[ ]:


transformer = TfidfTransformer()
tfidf_representation = transformer.fit_transform(tf_representation)

cos_sim_tfidf = cosine_similarity(tfidf_representation, dense_output=True)
cos_sim_tfidf_sorted_idxs = np.argsort(cos_sim_tfidf)

tfidf_representation


# In[ ]:


most_similar_law_idx = cos_sim_tfidf_sorted_idxs[original_law_index, -2]
tfidf_similarity = cos_sim_tfidf[original_law_index, most_similar_law_idx]

print(
    f"Dada a primeira lei anterior, similaridade com TF-IDF é: {round(tfidf_similarity, 2)}  e lei mais similar é:\n"
)
print_law(original_law_index)
print_law(most_similar_law_idx)


# Mostram a mesma lei. O que faz sentido, já que as leis são idênticas.

# In[ ]:


most_similar_indexes_tfidf = cos_sim_tfidf_sorted_idxs[:, -2]

dif_tf_tfidf = most_similar_indexes_tf != most_similar_indexes_tfidf
print(
    f"TF e TF-IDF discordam em {round(sum(dif_tf_tfidf) / len(dif_tf_tfidf) * 100, 2)}% dos resultados"
)


# A lei mais semelhante de acordo com TF e TF-IDF é diferente 56,97% das vezes.
#
# Vamos dar uma olhada em algumas leis onde os resultados diferem,
# para ter uma intuição sobre qual representação é melhor para as leis.
#
# Vamo sortear indices aleatorios desse vetor e
# ler as leis que eles representam e as similaridades

# In[ ]:


def get_disagreement_idxs(dif_array, num_laws=10):
    dif_results_idxs = [i for i, dif_result in enumerate(dif_array) if dif_result]
    random_idxs = np.random.randint(len(dif_results_idxs) - 1, size=num_laws)
    drafted_laws_idxs = [dif_results_idxs[i] for i in random_idxs]
    return drafted_laws_idxs


def compare_methods(
    laws_idxs,
    sim_array_a,
    sim_array_b,
    method_a_name="Metodo A",
    method_b_name="Metodo B",
):
    for i in laws_idxs:
        print(f"\n- - Lei comparada - -\n")
        print_law(i)
        print(f"\nMais similar de acordo com {method_a_name}:\n")
        print_law(sim_array_a[i])
        print(f"\nMais similar de acordo com {method_b_name}:\n")
        print_law(sim_array_b[i])


# In[ ]:


drafted_laws_idxs = get_disagreement_idxs(dif_tf_tfidf)
print(drafted_laws_idxs)


# In[ ]:


compare_methods(
    drafted_laws_idxs,
    most_similar_indexes_tf,
    most_similar_indexes_tfidf,
    method_a_name="TF",
    method_b_name="TF-IDF",
)


# Como é um sorteio,
# cada vez que você rodar esse notebook vai ter resultados diferentes.
# Fique a vontade pra fazer um PR com a comparação de leis diferentes.
# Abaixo estão comparações da primeira vez que rodei
#
# ### Lei 1018
# Lei 1018 é sobre proibição de homenagens a condenados por corrupção.
#
# TF trouxe uma lei sobre tornar uma associação pública.
#
# TF-IDF trouxe uma lei sobre evento de comemoração de adoção animal.
#
# Todas duas erraram.
#
# ### Lei 5776
# Lei 5776 sobre pagamento servidor público.
#
# TF trouxe: leitura da bíblia na abertura da câmara
# (que bizarro, diga-se de passagem).
#
# TF-IDF: aposentadoria diretor valor vencimento etc.
#
# Ambas as leis parecem ter sido trazidas como semelhantes
# por causa dos nomes próprios contidos nas leis.
#
# ### Lei 2789
# Lei 2789 (mil anos da revolução francesa) sobre obrigatoriedade
# de um servidor formado em primeiros socorros em escolas.
#
# TF: faço saber inkaba instituto de karate.
#
# TF-IDF: faço saber associação estrela jaco.
#
# Novamente as semelhanças são os nomes próprios nas leis.
#
# ### Lei 1772
# Lei 1772: faço saber sindicato trabalhadores rurais.
#
# TF: faço saber associação profissionais sexo.
#
# TF-IDF: faço saber associação pequenos agricultures apaeb -
# a rua da sede é a mesma da lei comparada.
#
# TF-IDF se saiu melhor nessa.
# Os nomes das pessoas em TF eram os mesmos da Lei,
# mas em TF-IDF não.
# O fator decisivo aqui foi o nome da rua, que era o mesmo.
# Ponto pra TF-IDF.
#
# ### Lei 530
# Lei 530: faço saber igreja ministerio pentecostal fogo gloria.
# rua volta redonda bairro campo limpo.
#
# TF: faço saber instituto nobre sede rodovia br km cis.
# nomes das pessoas iguais.
#
# TF-IDF: faço saber igreja evangelica pentecostal monte carmelo
# rua espassonavel bairro george americo.
# prefeitos diferentes.
#
# ### Lei 4810
# Lei: comenda.
# nomes: godofredo rebell figueiredo filho,
# raymundo luiz oliveira lopes.
#
# TF: comenda.
# nomes: godofredo rebello figueiredo filho,
# nilton bellas vieira.
#
# TF-IDF: comenda.
# nomes: godofredo rebello figueiredo filho,
# raimundo antonio carneiro pinto.
#
# As duas acertaram
#
# ### Lei 5238
# Lei 5238: promulgação de novas vias públicas.
# A via por TF-IDF passa por mais ruas iguais.
#
# ### Lei 5383
# Lei promulga academia de ginástica.
# TF: promulga empresas serviço funerario.
# TF-IDF: promulga novos aparelhos de ginástica.
#
# ### Outras
# As outras leis eram: "_visualizar legislativo ba_".
# Ambas trouxeram textos idênticos.

# Ok! Massa! Funciona!
#
# Pelos resultados acima, TF-IDF se saiu melhor.
# Inclusive pra retornar semelhança
# por nomes de ruas e de bairros,
# que é o que a gente quer pras buscas.
#
# Mesmo com 28k features,
# o resultado foi bastante rápido.
# Caso tivessemos um corpus maior,
# poderíamos ainda usar PCA pra reduzir as dimensões
# e ainda assim calcular a similaridade
# mantendo as relações entre os documentos.

# ### Vetor de palavras - word embedding
#
# A ideia dessa representação é
# criar um vetor pra cada palavra,
# com base nas palavras vizinhas.
#
# Isto vem da hipótese linguística distribucional:
# uma palavra é parecida com outra se
# suas vizinhas são as mesmas.
#
# Ou ainda:
# "conhecerás a palavra pelas compainhas que ela mantém".
#
# Vamos utilizar um método
# baseado nesta hipótese chamado
# [word2vec](https://arxiv.org/pdf/1301.3781.pdf).
# Existem outros, como GloVe, FastText, etc.
# Para construir as representações word2vec,
# utilizaremos a biblioteca
# [Gensim](https://radimrehurek.com/gensim/).
#
# Cada palavra é representada por um vetor
# de _n_ dimensões. Estes vetores são
# inicializados de forma aleatória.
# A seguir, o modelo tenta prever uma palavra
# de acordo com as anteriores (CBOW) ou as
# palavras vizinhas (skip-gram) e vai ajustando
# os valores de cada vetor de acordo.
#
# Ao final do processo, os vetores possuem
# alguma informação semântica sobre as palavras.
# Por exemplo, o vetor de "rei" e "rainha" estarão
# próximos e distantes de "ônibus" e "avião",
# palavras utilizadas em outro contexto (vizinhança).
#
# Isto possibilita operações aritiméticas com as
# palavras. Por exemplo:
#
# `rei` - `homem` + `mulher` = `rainha`
#
# Mais informações sobre word2vec nas duas primeiras
# [aulas](https://www.youtube.com/watch?v=8rXD5-xhemo&list=PLoROMvodv4rOhcuXMZkNm7j3fVwBBY42z)
# deste curso. Se quiser saber mais sobre representações
# de texto, o gensim tem ótimos
# [tutoriais](https://radimrehurek.com/gensim/auto_examples/index.html).
# [Este repositório](https://github.com/RaRe-Technologies/movie-plots-by-genre)
# também possui um notebook tutorial que exemplifica
# representações e classificação de textos.
#
#
# Caso você tenha um material que explique
# representações de texto, especialmente em português,
# manda pra gente ou faz um PR pra adicionar ele aqui!
# Adoraríamos essa contribuição!
#

# In[ ]:


corpus = laws["texto_limpo"].apply(lambda x: x.split())
model_w2v = Word2Vec(sentences=corpus, window=5, min_count=5, workers=8)


# ### Palavras semelhantes
#
# Uma das vantagens desse modelo é que
# podemos explorar a semelhança entre palavras.
#
# No texto das Leis, quais as palavras mais semelhantes
# a `educação` ou `saúde`, por exemplo?
#
# Você pode explorar outras semelhanças modificando
# o código da próxima célula:

# In[ ]:


model_w2v.most_similar("transporte", topn=10)


# Semelhantes a `educação`:
# saúde, escolar, seduc, especialistas
# executiva, escolarização, cultura
# prevenção, professores, endemias.
#
# Semelhantes a `saúde`:
# educação, competirá, vigilância,
# seduc, médico-hospitalar, básico
# segunraça, sus, incumbida, rede
#
# Semelhantes a `segurança`:
# higiene, alimentar, nutricional,
# conforto, coletiva, zelar,
# garantir, engenharia, visando, melhor.
#
# Semelhantes a `transporte`:
# coletivo, passageiros, alternativo,
# cargas, táxi, convencional, veículos,
# individual, coeltivos, stiac.
#
# Embora muitas palavras de fato indiquem semelhanças,
# algumas palavras não possuem muita relação.
# Por exemplo: "saúde" e "competirá".
# Isto pode ocorrer porque a palavra "competirá"
# ocorre em contextos parecidos a "saúde".
#
# Uma forma de mitigar estes problemas é treinando
# com mais dados. Podemos, por exemplo, carregar todos
# os documentos de textos e treiná-los todos juntos.
# Este também é um bom exercício, se você está aprendendo.
# Faz um PR pra gente!

#

# ## Construindo a representação das Leis
#
# O Gensim também traz uma ferramenta para
# gerar embeddings de textos inteiros, chamada
# [Doc2Vec](https://radimrehurek.com/gensim/models/doc2vec.html#gensim.models.doc2vec.Doc2Vec).
# Esta técnica utiliza uma ideia semelhante ao Word2Vec,
# com adaptações para cobrir um texto inteiro.

# In[ ]:


# PS: Um compilador C torna o Doc2Vec em até 70x mais rápido
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(corpus)]
documents[:2]


# In[ ]:


model_d2v = Doc2Vec(vector_size=50, min_count=5, window=2, workers=8, epochs=40)  #
model_d2v.build_vocab(documents)
model_d2v.train(
    documents, total_examples=model_d2v.corpus_count, epochs=model_d2v.epochs
)


# In[ ]:


most_similar_idxs_d2v = []
for i in range(len(documents)):
    doc_vec = model_d2v.docvecs[i]
    most_similar_idx = model_d2v.docvecs.most_similar([doc_vec], topn=2)[1][0]
    most_similar_idxs_d2v.append(most_similar_idx)


# In[ ]:


dif_d2v_to_tfidf = most_similar_indexes_tfidf != most_similar_idxs_d2v
print(
    f"Porcentagem de resultados diferentes de TFIDF: {round(sum(dif_d2v_to_tfidf)*100 / len(dif_d2v_to_tfidf),2)}"
)


# ## Comparação Doc2Vec x TF-IDF
#
# A diferença de resultados mais semelhantes entre Doc2Vec e TF-IDF é

# In[ ]:


drafted_laws_idxs = get_disagreement_idxs(dif_d2v_to_tfidf, num_laws=5)
compare_methods(
    drafted_laws_idxs,
    most_similar_indexes_tfidf,
    most_similar_idxs_d2v,
    method_a_name="TF-IDF",
    method_b_name="Doc2Vec",
)


# ### Lei 2011:
#
# Conteúdo obsoleto:
# Este  Ato não tem mais efeito prático, pois o conteúdo é temporal.
# 22 de Dezembro de 2005.
#
# - TF-IDF trouxe Lei 2748:
#
#     Conteúdo obsoleto:
#     Este  Ato não tem mais efeito prático, pois o conteúdo é temporal.
#     20 de Junho de 2003.
#
# - Doc2Vec trouxe Lei 4046:
#
#     Lei Orgânica do Município.
#     Concede título de cidadão Feireense.
#
# TF-IDF muito melhor.
#
# PS: Não sabia que o conteúdo da Lei era apagado depois que o prazo vencia.
# Tá certo isso?
#
# ### Lei 5674:
#
# Mudança de nome de Rua Alegria pra Rua Maria Quitéria de Jesus, na Vila de Tiquarusú
#
# - TF IDF trouxe Lei 6014:
#
#     Nominada nova rua "Rua Congego Cupertino Lacerda" da Senador Quintino à Comandante Almiro.
#
# - Doc2Vec trouxe Lei 1142:
#
#     Mudança no texto das leis.
#
# Novamente TF-IDF chegou muito mais perto
#
# ### Lei 1943:
#
# Faço saber do Dia Municipal de Organizações da Sociedade Civil
#
# - TF IDF. Lei 3212:
#
#     Faço saber divuglando Associação Espírita Lar da Esperança
#
# - Doc2Vec. Lei 3070:
#
#     Faço saber Dia Municipal do Feirante.
#
# Dessa vez Doc2Vec se saiu melhor.
# Ambas trouxeram Faço saber,
# mas Doc2Vec trouxe um faço saber de feriado,
# enquanto a Lei mais semelhante por TF-IDF
# apresentou um faço saber de divulgação de associação espírita.
#
# ### Leis 5058 e 3799:
#
# Duas Leis idênticas, exceto os números,
# que não são considerados pelos métodos de busca:
#
# `"Visualizar Ato:Decreto Legislativo nº 33/2011 - Feira de Santana-BA"`
#
# Ambos os métodos trouxeram leis idênticas.
#
# - TF-IDF: 5105, 5105
# - Doc2Vec: 4207, 3953
#
#

# TF-IDF e sai um pouco melhor nas Leis analisadas.
#
# Como a diferença da Lei mais próxima entre TF-IDF e Do2Vec
# é grande (87%), acredito que TF-IDF seja uma opção melhor para utilizar.

# ## Outras opções
# ### Indexar
#
# Há outras formas de indexar os documentos e de recuperar, também simples.
#
# Uma outra forma de criar representações para indexar, por exemplo,
# é calcular a média dos vetores pra cada palavra do documento.
# Doc2Vec em geral é ligeramente melhor, mas precisamos testar
# no nosso corpus.
#
# Outra forma é contar n-gramas - por exemplo, bi-gramas:
# duas palavras juntas formando um token.
# Dessa forma, você possui uma matriz maior
# e de certa forma uma relação entre a sequencialidade das palavras,
# que pode ser útil pra nomes de pessoas e bairros, como citado acima.
#
# ### Recuperar
#
# Outra forma de recuperar é por local sensitive hashing:
# Dividir o espaço vetorial em vários planos múltiplas vezes
# e retornar os resultados que estão na mesma região da query.
# No entanto, o corpus não é grande o suficiente pra precisar essa estratégia,
# que é mais pra grandes corpora.
# O método acima (calcular a simlaridade cosseno e retornar os maiores valores)
# é rápido o suficiente pra parecer instantâneo.
# Talvez com uma demanda mais alta pelo servidor venha a necessidade de aumentar
# a velocidade da busca, porém por enquanto não é o caso.
# Mais sobre recuperação: Google lançou [novo método]
# (https://ai.googleblog.com/2020/07/announcing-scann-efficient-vector.html)
# e uma lib pra isso agora, dia 28 de Julho.
#
# ### Avaliação
#
# Com múltiplas formas de indexar e recuperar vem o dilema:
# como avaliar se uma é melhor que a outra?
# Repetir o processo acima pra todas as opções?
# Isto é, mostrar N melhores resultados e comparar manualmente?
# Ou colocar labels em algumas leis? Ex: essa lei trata disso, com tais entidades.
# Checar formas de avaliação.
# Se tivesse em produção, podia avaliar por CTR por ex, mas não é o caso
