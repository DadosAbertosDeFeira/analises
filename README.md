# Análises

Repositório para abrigar as análises dos Dados Abertos de Feira.
A coleta é feita pela [Maria Quitéria](https://github.com/DadosAbertosDeFeira/maria-quiteria).

## Dados

| Base de dados | Fonte | Descrição        | Coleta          | Banco de dados | Download |
| ------------- | ------------- | ------------- |:-------------:|:-----:|:-----:|
| Agenda (`citycouncil.py`) | Câmara Municipal | Agenda (ordem do dia, homenagens, sessões ordinárias etc) da Câmara Municipal. | :heavy_check_mark: | :heavy_check_mark: | 🔜 |
| Atas das sessões (`citycouncil.py`) | Câmara Municipal | Atas das sessões da Câmara Municipal. | :heavy_check_mark: | :heavy_check_mark: | 🔜 |
| Lista de Presença (`citycouncil.py`) | Câmara Municipal | Assiduidade dos vereadores da Câmara Municipal. | :heavy_check_mark: | :heavy_check_mark: | 🔜 |
| Despesas (`citycouncil.py`) | Câmara Municipal | Gastos realizados pela Câmara Municipal. | :heavy_check_mark: | :heavy_check_mark: | [Kaggle](https://www.kaggle.com/anapaulagomes/despesas-da-cmara-municipal) |
| Contratos (`cityhall.py`) | Prefeitura | Contratos realizados pela prefeitura entre 2016 e 2017. | :heavy_check_mark: | 🔜 | [Kaggle](https://www.kaggle.com/anapaulagomes/contratos-da-prefeitura-de-feira-de-santana) |
| Diário Oficial (`gazette.py`) | Prefeitura/Câmara de Vereadores | Diário oficial do executivo e legislativo desde 2015. | :heavy_check_mark: | :heavy_check_mark: | [Kaggle](https://www.kaggle.com/anapaulagomes/dirios-oficiais-de-feira-de-santana)  |
| Diário Oficial (legado - antes de 2015) (`gazette.py`) | Prefeitura | Leis e decretos entre 1999 e 2015. | :heavy_check_mark: | :heavy_check_mark: | [Kaggle](https://www.kaggle.com/anapaulagomes/dirios-oficiais-de-feira-de-santana-at-2015) |
| Licitações (`cityhall.py`) | Prefeitura | Licitações realizadas pela prefeitura desde 2015. | :heavy_check_mark: | 🔜 | [Kaggle](https://www.kaggle.com/anapaulagomes/licitaes-da-prefeitura-de-feira-de-santana) |
| Pagamentos (`cityhall.py`) | Prefeitura | Pagamentos realizados pela prefeitura desde 2010. | :heavy_check_mark: | 🔜 | [Kaggle](https://www.kaggle.com/anapaulagomes/pagamentos-da-prefeitura-de-feira-de-santana) |

## Estrutura

* analysis: onde todos os jupyter notebooks devem estar
* docs: documentos como manuais e dicionários de dados devem estar lá
* etl: onde colocamos scripts Python que ajudam na coleta e preparação para análises
* publish: arquivos prontos para serem publicados e divulgados

Os dados não serão armazenados nesse repositório porém todos os passos
para limpeza e análise devem ser reproduzidos a partir dos dados baixados.

## Contribuindo para o projeto

Contribuições são muito bem-vindas. Veja como contribuir no nosso [Guia de Contribuição](CONTRIBUTING.md).

Toda a comunicação e demais interações do Dados Abertos de Feira estão sujeitas
ao nosso [Código de Conduta](https://github.com/DadosAbertosDeFeira/maria-quiteria/blob/master/CODE_OF_CONDUCT.md).
