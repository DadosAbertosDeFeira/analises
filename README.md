# Análises

![CI](https://github.com/DadosAbertosDeFeira/analises/workflows/CI/badge.svg)
![Converte Notebook para script Python](https://github.com/DadosAbertosDeFeira/analises/workflows/Converte%20Notebook%20para%20script%20Python/badge.svg)

Repositório para abrigar as análises dos Dados Abertos de Feira.
A coleta é feita pela [Maria Quitéria](https://github.com/DadosAbertosDeFeira/maria-quiteria).

## Dados

Os dados disponíveis para análise podem ser vistos no repositório da [Maria Quitéria](https://github.com/DadosAbertosDeFeira/analises#dados)
ou diretamente no nosso [Kaggle](https://www.kaggle.com/dadosabertosdefeira/).

Frequentemente utilizamos dados exportados diretamente dos portais da transparência da
[Prefeitura de Feira de Santana](http://www.transparencia.feiradesantana.ba.gov.br/),
da [Câmara de Vereadores](https://www.transparencia.feiradesantana.ba.leg.br/)
ou de outros sites como [Tribunal de Contas dos Municípios da Bahia (TCM-BA)](https://www.tcm.ba.gov.br/).

## Estrutura

* `analysis`: onde todos os jupyter notebooks devem estar
* `docs`: documentos como manuais e dicionários de dados devem estar lá
* `scripts`: onde colocamos scripts Python que ajudam na coleta e preparação para análises
* `publish`: arquivos prontos para serem publicados e divulgados

Os dados não serão armazenados nesse repositório porém todos os passos
para limpeza e análise devem ser reproduzidos a partir dos dados baixados.

## Contribuindo para o projeto

Contribuições são muito bem-vindas. Veja como contribuir no nosso [Guia de Contribuição](CONTRIBUTING.md).

### Python

Utilizamos a versão 3.8 do Python. Recomendamos fortemente o uso de _virtual environments_ para isolamento
das dependências e prevenção de possíveis conflitos com dependências de outros projetos.

### Dependências

```
pip install -r requirements.txt
```

### Testes

Para executar os testes, execute:

```
pytest
```

Toda a comunicação e demais interações do Dados Abertos de Feira estão sujeitas
ao nosso [Código de Conduta](https://github.com/DadosAbertosDeFeira/maria-quiteria/blob/master/CODE_OF_CONDUCT.md).
