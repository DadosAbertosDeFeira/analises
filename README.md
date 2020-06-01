# Análises

![CI](https://github.com/DadosAbertosDeFeira/analises/workflows/CI/badge.svg)
![Converte Notebook para script Python](https://github.com/DadosAbertosDeFeira/analises/workflows/Converte%20Notebook%20para%20script%20Python/badge.svg)

Repositório para abrigar as análises dos Dados Abertos de Feira.
A coleta é feita pela [Maria Quitéria](https://github.com/DadosAbertosDeFeira/maria-quiteria).

## Estrutura

* analysis: onde todos os jupyter notebooks devem estar
* docs: documentos como manuais e dicionários de dados devem estar lá
* etl: onde colocamos scripts Python que ajudam na coleta e preparação para análises
* publish: arquivos prontos para serem publicados e divulgados

Os dados não serão armazenados nesse repositório porém todos os passos
para limpeza e análise devem ser reproduzidos a partir dos dados baixados.

## Como contribuir

Para contribuir, basta fazer um _fork_ desse repositório, fazer as modificações
e abrir um _pull request_. Se for contribuir com uma análise, certifique-se de que
seu Jupyter Notebook está no diretório correto e que está limpo.

Para verificar se está limpo, execute:

```
nb-clean check -i analysis/Camara-e-COVID19.ipynb
```

Para limpar seu notebook:

```
nb-clean clean -i analysis/Camara-e-COVID19-sujo.ipynb > analysis/Camara-e-COVID19.ipynb
```

Ao abrir um _pull request_, o GitHub Actions vai gerar os arquivos
Python automaticamente. Isso facilita a revisão do código.

Não esqueça de documentar o que você fez. Deixe uma descrição do seu
trabalho no _pull request_.
