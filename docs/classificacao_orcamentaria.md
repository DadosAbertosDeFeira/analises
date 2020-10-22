# Classificação orçamentária

Ou Classificação da Receita e Despesa Orçamentária por Natureza.

O ato nº 456/2019 do Tribunal de Contas dos Municípios do Estado da Bahia
estabelece classificações da receita e da despesa orçamentárias.
Ambas estão disponíveis na [seção de contabilidade do site do TCM-BA](https://www.tcm.ba.gov.br/contabilidade-municipal/).

## Natureza das despesas

O código da natureza das despesas tem 8 dígitos e cada posição representa um grupo ou subgrupos.

Exemplos:

| Código   | Descrição                                                    | Código Superior |
| -------- | ------------------------------------------------------------ | --------------- |
| 30000000 | Despesas Correntes                                           | 0               |
| 31000000 | Pessoal e Encargos Sociais                                   | 30000000        |
| 31300000 | Transferências a Estados e ao Distrito Federal               | 31000000        |
| 31301100 | Vencimentos e Vantagens Fixas - Pessoal Civil                | 31300000        |
| 31301101 | Vencimento e vantagens fixas Pessoal Civil (Vencimento Básico) | 31301100        |

Na pasta `data` deste repositório já temos todos os arquivos. Se você quiser fazer
alguma análise que envolve a natureza das despesas pode utilizar métodos que criamos
para facilitar a limpeza dos dados e enriquecimento das suas análises. São eles:

```python
from scripts.parsers import all_expenses_nature_from_tcmba, extract_nature


# para identificar um possível código de natureza da despesa
# passe a string desejada para `extract_nature`

text = "339030120000000000 - Genero Alimenticios - Outros"
possible_nature = extract_nature(text)  # retorna 33903012

# para acessar todos os códigos e descrições das naturezas da despesa
# do TCM-BA utilize `all_expenses_nature_from_tcmba`

# informe o ano desejado ou não passe nada para o último ano disponível

expenses_nature = all_expenses_nature_from_tcmba(2019)

# o método vai retornar um dicionário como esse, com todas as
# naturezas da despesa:
{
    "30000000": {
        "code": "30000000",
        "description": "Despesas Correntes",
        "superior_group_code": None,
    }
}

# você só precisa do código (já retornado por `extract_nature` sem máscara)
# para acessar as informações de uma natureza da despesa

expenses_nature.get("30000000")
```

Com esses dois métodos você poderá identificar possíveis códigos
de uma natureza da despesa e depois fazer o _match_ com a lista
completa.
