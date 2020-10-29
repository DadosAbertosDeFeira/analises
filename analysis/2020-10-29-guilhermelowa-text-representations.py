#!/usr/bin/env python
# coding: utf-8

# # Semelhança de documentos
#
# A função desse notebook é criar representações para o texto dos documentos,
# exibir textos semelhantes e com isso avaliar as representações.
# Os textos semelhantes são um teste para a representação do texto:
# se os textos mostrados não são semelhantes, então a representação não é boa;
# se são semelhantes, então a representação um pouco melhor.
#
# ## Dados
#
# Embora a proposta deste notebook um template genérico para comparação de textos,
# neste notebook utilizamos o dataset das leis municipais, disponível
# [aqui](https://www.kaggle.com/anapaulagomes/leis-do-municpio-de-feira-de-santana/).
#

# In[ ]:


import sys

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scripts.parsers import clean_text
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

# In[48]:


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


# Exemplo de texto de lei
print(laws.loc[len(laws) - 1, "texto"])


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


# Com a matriz de documentos ~literalmente~ em mãos,
# vamos calcular a similaridade entre dois textos.
# A similaridade é calculada pela similaridade do cosseno (ver algebra linear).
# Existem outras medidas pra calcular similaridade / distância.
# Uma discussão sobre isso [aqui](https://cmry.github.io/notes/euclidean-v-cosine).

# In[ ]:


cos_sim_matrix = cosine_similarity(tf_representation, dense_output=True)
# sorts ascending, per row,
# the indexes of the documents according to their cossine similarity
cos_sim_argsort = np.argsort(cos_sim_matrix)


# In[ ]:


most_similar_indexes_tf = cos_sim_argsort[:, -2]  # -1 is the same text
tf_similarities = [
    cos_sim_matrix[i, ind] for i, ind in enumerate(most_similar_indexes_tf)
]


# In[ ]:


def print_laws(original_law_index, compared_law_index: int):
    print(f"- - - LEI: {original_law_index}: - - -\n\n")
    print(laws.loc[original_law_index, "texto"])
    print(f"\n\n- - - LEI COMPARADA: {compared_law_index} - - -\n\n")
    print(laws.loc[compared_law_index, "texto"])


# In[ ]:


max_sim_overall = np.max(tf_similarities)
print(f"Maior similaridade entre duas Leis: {max_sim_overall}")

original_law_index = np.argmax(tf_similarities)
most_similar_law_index = most_similar_indexes_tf[original_law_index]

print_laws(original_law_index, most_similar_law_index)


# As leis 5949 e 6026 são idênticas.
# Opa! Lei 13 e Lei 118 são a mesma lei, com 3 dias de diferença. Por que existe isso?

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

print("Dada a mesma lei anterior, " f"similaridade com TF-IDF é: {tfidf_similarity}")
print_laws(original_law_index, most_similar_law_idx)


# Mostram a mesma lei. O que faz sentido, já que as leis são idênticas.

# In[ ]:


most_similar_indexes_tfidf = cos_sim_tfidf_sorted_idxs[:, -2]

same_result = most_similar_indexes_tf == most_similar_indexes_tfidf
print(same_result)
print(f"Concordam em {sum(same_result) / len(same_result) * 100}% dos resultados")


# A lei mais semelhante de acordo com TF e TF-IDF é a mesma 40% das vezes.
#
# Vamos dar uma olhada em algumas leis onde os resultados diferem,
# para ter uma intuição sobre qual representação é melhor para as leis.
#
# Vamo sortear indices aleatorios desse vetor e
# ler as leis que eles representam e as similaridades

# In[ ]:


different_result_indexes = [i for i, _ in enumerate(same_result) if not same_result[i]]
comparisons_count = 10
drafted_indexes = np.random.randint(
    0, high=len(different_result_indexes) - 1, size=comparisons_count
)
drafted_laws = [different_result_indexes[i] for i in drafted_indexes]
print(drafted_laws)


# In[ ]:


for i in drafted_laws:
    print("\n\nCOMPARACAO UTILIZANDO TF:\n\n")
    print_laws(i, most_similar_indexes_tf[i])
    print("\n\nCOMPARACAO UTILIZANDO TF-IDF:\n\n")
    print_laws(i, most_similar_indexes_tfidf[i])


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
# ***AVISO! ESTA PARTE GASTA MUITA MEMÓRIA!***
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
# Na prática,
# vamos utilizar um método bem simples
# baseado nesta hipótese.
# Cada palavra é representada por um vetor
# de _n_ dimensões,
# onde _n_ é o tamanho do vocabulário.
# Os valores de cada dimensão são
# a frequência com que a palavra
# representada por esta dimensão
# aparece como vizinha da palavra sendo representada.
#
# A vizinhança pode variar.
# Neste caso,
# temos como vizinhas palavras até 2 tokens de distância.
# Portanto,
# na frase "dados abertos de feira é massa",
# a palavra "_de_" é vizinha de todas as palavras,
# exceto "_massa_".

# In[5]:


keep_execution = input(
    "O trecho a seguir consome muita memoria "
    "(em torno de 12 GB).\n"
    "Deseja prosseguir? (s/n)"
)
if keep_execution == "n":
    sys.exit()


# In[ ]:


cleaned_text = " ".join(laws["texto_limpo"].tolist())
cleaned_text = cleaned_text.split()
unique_words = set(cleaned_text)
print(f"Text length: {len(cleaned_text)}")
print(f"Vocabulary length: {len(unique_words)}")


# In[ ]:


word_indexes = {}
for i, word in enumerate(unique_words):
    word_indexes[word] = i


# In[ ]:


# Esta parte consome muita memória
# pra rodar esta parte, descomente a linha abaixo
word_embedding_matrix = np.zeros((len(unique_words), len(unique_words)), dtype=np.int16)
word_embedding_matrix


# In[ ]:


neighborhood = 2
for idx, word in enumerate(cleaned_text):
    for i in range(1, neighborhood):
        neighbor_word = cleaned_text[idx + i]

        word_idx = word_indexes[word]
        neighbor_index = word_indexes[neighbor_word]

        word_embedding_matrix[word_idx, neighbor_index] += 1
        word_embedding_matrix[neighbor_index, word_idx] += 1
    if idx == len(cleaned_text) - neighborhood:
        break
word_embedding_matrix


# In[ ]:


# Transform to sparse, to avoid memory consumption
word_embedding_matrix = csr_matrix(word_embedding_matrix)
word_embedding_matrix


# In[ ]:


# We have our word representation
# Lets test it checking the most similar words to 10 random words
words_cosine_similarity_matrix = cosine_similarity(
    word_embedding_matrix, dense_output=False
)
words_cosine_similarity_matrix


# In[ ]:


palavras_semelhantes = np.argsort(words_cosine_similarity_matrix[0].toarray())
len(palavras_semelhantes[0])


# In[ ]:


drafted_words_index = np.random.randint(len(unique_words), size=10)


def show_words(idx: int, similar_words: list, vocabulary: list):
    word = vocabulary[idx]
    print(f"Lista de palavras similares a {word} - {idx}:")
    for i in similar_words:
        word = vocabulary[i]
        print(f"{word} - {i}")
    print("\n- - - - - \n\n")


vocabulary = list(word_indexes.keys())
for idx in drafted_words_index:
    sorted_cosine_similarities_array = np.argsort(
        words_cosine_similarity_matrix[idx].toarray()
    )
    similar_words = sorted_cosine_similarities_array[0][-10:-1]
    show_words(idx, similar_words, vocabulary)


# Neste corpus, pra algumas palavras,
# a hipótese distribucional parece funcionar bem,
# pra outras nem tanto, pra outras não funciona.
#
# Semelhantes a "outorgar" temos:
# "permutar", "editar", "contratar", "doar",
# "conceder", "dispensar", "celebrar", "subscrever", "proibir".
# Embora a semântica (significado) não seja necessariamente próxima,
# todas as palavras são verbos, então a sintaxe é próxima.
#
# Semelhantes a "ibitita":
# "axixa", "ibirarema", "peritoro", "piracaia", "igarata",
# "erechim", "itaperuna", "piata", "vandinha".
# Todos parecem nomes de locais.
#
# Existem casos horríveis.
# Semelhantes à "coesao" temos:
# "sedeso", "his", "ctps", "zeis", "pnas", "cgfmhis", "snhis", "acemas".
# O que significam essas palavras?
# Talvez seja útil melhorar a qualidade do pré-processamento pra melhorar na indexação.
#
# Semelhantes à "separando" temos: "agrossilvopastoris", "cemiteriais", "solidos",
# "molhados", "domiciliares", "volumosos", "baldios", "antecedencia", "dimensao".
#
# Há casos mistos.
# Semelhantes `a "trasporte" (note o erro) temos:
# "meia" (talvez meia passagem?), "transporte" (a palavra correta aparece em segundo),
# "roletas", "vala" (?), "trafegos", "convencional" (?),
# "edificar" (?), "passageiros", "fretado".
#
# Talvez o corpus seja pequeno demais
# pra encontrar as relações entre as palavras só contando?
# Há de se testar se não é melhor então trabalhar com vetores de palavras,
# mesmo aprendidos em um corpus pequeno.
# Segundo o paper
# "Don't count, predict! a systematic comparison of context-counting vs.
# context-predicting semantic vectors (2014) - Baroni, Dinu, Kruszeweski",
# predizer é melhor que contar.
# Há de se testar se neste nosso contexto isso também se verifica.
#
# Por hora,
# vamos testar se a busca melhora ou não utilizando as palavras.
# Então vamos construir a representação das leis.
#
# # Construindo representação das leis com base na hipotese distribucional

#

# In[ ]:


# Cada lei vai ser a soma dos word_embedding_matrix de suas palavras
# Usando np.zeros gasta muita memoria, mas csr_matrix eh muito lento
word_embedding_representation = np.zeros(
    (len(laws["texto_limpo"]), word_embedding_matrix.shape[1])
)
for idx, law in enumerate(laws["texto_limpo"]):
    for word in law.split():
        word_index = word_indexes[word]
        word_embedding_representation[idx] += word_embedding_matrix[word_index]
word_embedding_representation


# In[ ]:


word_embedding_cosine_similarity = cosine_similarity(word_embedding_representation)


# In[ ]:


most_similar_indexes_word_embedding = [
    idx for idx in np.argsort(word_embedding_cosine_similarity)[:, -2]
]


# In[ ]:


# Diferenca de vetores pra TFIDF eh bem maior.
# Vamos samplear algumas dessas diferencas e
# mostrar uma lei q tanto TFIDF como Count erraram
different_result_from_tfidf = (
    most_similar_indexes_word_embedding != most_similar_indexes_tfidf
)
print(
    "Porcentagem de resultados diferentes de TFIDF: "
    f"{sum(different_result_from_tfidf)*100 / len(different_result_from_tfidf)}"
)


# In[ ]:


drafted_laws_index = np.random.randint(len(different_result_from_tfidf), size=10)
for i in drafted_laws_index:
    if different_result_from_tfidf[i]:
        print("\n\nVETOR DE PALAVRAS:\n\n")
        print_laws(i, most_similar_indexes_word_embedding[i])
        print("\n\nTF-IDF:\n\n")
        print_laws(i, most_similar_indexes_tfidf[i])


# Parece que TF-IDF é um pouco melhor na comparação de leis,
# pq traz resultados mais relevantes quando comparados nome de bairros e ruas.
# No entanto, a forma vetorizada parece ser boa pra reconhecer formatos da Lei em geral,
# uma especie de POS, reconhecendo que existe uma entidade alí ou verbo etc.
# Ao menos foi minha impressão.
# Cabe mais investigação a respeito.
#
# Vale salientar que a qualidade dos vetores parece não estar tão boa.
# Vide a semelhança de palavras. Como fazer pra consertar isso?
# Seria muito interessante corrigir isso pra ver as palavras mais semelhantes à
# educação,saúde etc e também pra visualizar com tsne os clusters gerados a partir daí.

# ## Outras opções
# ### Indexar
#
# Há outras formas de indexar os documentos e de recuperar, também simples.
# Uma outra forma de indexar, por exemplo,
# é fazer um vetor pra cada palavra contando as palavras vizinhas.
# E depois, o vetor do documento seria a soma dos vetores das palavras.
# É uma forma interessante porque pode gerar visualizações interessantes
# entre a similaridade das palavras.
# Por exemplo, no corpus das Leis Municipais,
# a quais palavras EDUCAÇÃO mais se assemelha? Ou SAÚDE? Etc.
#
# Outra forma é contar n-gramas - por exemplo, bi-gramas:
# duas palavras juntas formando um token.
# Dessa forma, você possui uma matriz maior
# e de certa forma uma relação entre a sequencialidade das palavras,
# que pode ser útil pra nomes de pessoas e bairros, como citado acima.
#
# ### Recuperar
#
# Outra forma de recuperar é por local sensitive hashing.
# Divide em vários planos múltiplas vezes
# e retorna os resultados que estão na mesma região da query.
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
