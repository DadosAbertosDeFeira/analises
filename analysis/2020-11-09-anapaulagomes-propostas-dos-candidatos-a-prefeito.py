import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import texthero as hero
from scripts.nlp import remove_portuguese_stopwords
from texthero import preprocessing
from wordcloud import WordCloud

target_state = "BA"  # sigla do estado
target_city = "feira-de-santana"  # nome da cidade separado por hífens
proposals_directory = "propostas"  # sem a barra final
proposals_and_cities = {}

# estrutura: estado > cidade > proposta-<candidato>.txt
for folder, _, files in os.walk(proposals_directory):
    if files:
        index_city = folder.rfind("/")
        city = folder[index_city + 1 :]
        index_state = folder[:index_city].rfind("/")
        state = folder[index_state + 1 : index_city]
        proposals_and_cities[f"{state}/{city}"] = files
proposals_and_cities[f"{target_state}/{target_city}"]


custom_pipeline = [
    preprocessing.remove_digits,
    preprocessing.remove_diacritics,
    preprocessing.remove_whitespace,
]

candidates_and_proposals = {}
for file_name in proposals_and_cities[f"{target_state}/{target_city}"]:
    candidate_name = file_name[12:]
    candidate_name = candidate_name.replace(".txt", "")
    candidate_name = candidate_name.replace("-", " ")
    candidate_name = candidate_name.title()
    print(candidate_name)
    content = open(
        f"{proposals_directory}/{target_state}/{target_city}/{file_name}"
    ).read()
    custom_stop_words = [
        "feira",
        "santana",
        "municipio",
        "municipal",
        "município",
        "municipais",
        "cidade",
        "publico",
        "publica",
    ]
    cleaned_text = remove_portuguese_stopwords(content, custom_stop_words)
    cleaned_text = pd.Series(cleaned_text)
    cleaned_text = hero.clean(cleaned_text, custom_pipeline)
    candidates_and_proposals[candidate_name] = cleaned_text


for candidate, proposal in candidates_and_proposals.items():
    print(f"------------------------ {candidate}")
    text = " ".join(proposal)
    wordcloud = WordCloud(
        background_color="white",
        width=2000,
        height=800,
        colormap="PuOr",
        collocations=False,
    ).generate(text)
    fig = plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    fig.savefig(
        f"nuvem-de-palavras-das-propostas-de-{candidate.replace(' ', '-').lower()}.png",
        dpi=fig.dpi,
    )
    plt.show()

all_proposals = []
for _, proposal in candidates_and_proposals.items():
    all_proposals.extend(proposal)

imagem = cv2.imread("images/caixa-dagua-do-tomba.jpg")
gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

text = " ".join(all_proposals)
wordcloud = WordCloud(
    background_color="white", mask=mask, collocations=False, colormap="Set2"
).generate(text)
fig = plt.figure(figsize=(20, 10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
fig.savefig(f"nuvem-de-palavras-dos-candidatos-a-prefeito-de-feira.png", dpi=fig.dpi)
plt.show()


custom_pipeline = [
    preprocessing.remove_digits,
    preprocessing.remove_diacritics,
    preprocessing.remove_whitespace,
]

all_proposals = []
for city, proposals in proposals_and_cities.items():
    if city.startswith(target_state):
        for proposal in proposals:
            content = open(f"{proposals_directory}/{city}/{proposal}").read()
            custom_stop_words = ["municipio", "municipal", "município"]
            cleaned_text = remove_portuguese_stopwords(content, custom_stop_words)
            cleaned_text = pd.Series(cleaned_text)
            cleaned_text = hero.clean(cleaned_text, custom_pipeline)
            all_proposals.extend(cleaned_text)

text = " ".join(all_proposals)

wordcloud = WordCloud(
    background_color="white",
    width=2000,
    height=800,
    colormap="Set2",
    collocations=False,
).generate(text)
fig = plt.figure(figsize=(20, 10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
fig.savefig(f"nuvem-de-palavras-dos-candidatos-prefeito-bahia.png", dpi=fig.dpi)
plt.show()
