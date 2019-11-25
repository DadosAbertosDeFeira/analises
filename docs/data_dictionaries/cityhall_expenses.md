# Prefeitura - Despesas

São todos os [gastos feitos pela Prefeitura de Feira de Santana](http://www.transparencia.feiradesantana.ba.gov.br/index.php?view=despesa). As Despesas são divididas em:

* **Despesas correntes**: Aquelas necessárias à manutenção dos serviços
públicos, como as despesas com material de consumo, telefone, pessoal,
serviços de terceiros, etc.
* **Despesas de capital**: São os investimentos, ou seja, gastos com
novos equipamentos e obras, como construção e reforma de escolas,
hospitais, postos de saúde, pavimentação, etc.

Os registros de classificação da despesa são efetuados por meio de
rotinas específicas e de forma geral podem ser assim tratadas:

* **Valor Orçado (Dotação Orçamentária)**: Dependem de autorização
legislativa e correspondem ao valor a ser utilizado para a manutenção
da Administração Pública;
* **Valor Empenhado**: Consiste na reserva da dotação orçamentária para
um fim específico, devendo registrar o nome/razão social do credor, valor
e descrição do que será pago;
* **Valor Liquidado**: Registra efetivamente a despesa executada. No entanto,
por ocasião do encerramento do exercício, conforme as normas da Lei Federal 
n° 4.320/1964, as despesas empenhadas e ainda não liquidadas são inscritas
em restos a pagar não processados;
* **Valor Pago**: Consiste na entrega do numerário ao credor e só pode ser
efetuado após regular liquidação da despesa.

Fonte: http://www.transparencia.feiradesantana.ba.gov.br/index.php?view=despesasinfo (acessado em 25 de Novembro de 2019)

| Atributo | Campo        | Formato           | Exemplo  |
| ------------- | ------------- |:-------------:| -----:|
| Data da publicação | `data_publicacao`      | Data: DD/MM/YYYY | 18/01/2010 |
| Fase | `fase`      | Texto: `EMPENHO`, `LIQUIDAÇÃO` ou `PAGAMENTO` | LIQUIDAÇÃO |
| Credor | `credor`      | Texto: nome fantasia ou nome de uma pessoa | DIVIMED COM. PROD. HOSPITALARE |
| Valor | `valor`      | Texto | R$         91,60 |
| Número | `numero`      | Texto | 00194/10 |
| CNPJ ou CPF | `cpf_ou_cnpj`      | Texto | 00.242.167/0001-18 |
| Data do pagamento | `data_pagamento`      | Data: DD/MM/YYYY | 18/01/2010 |
| Número do processo | `numero_processo`      | Texto | 21123021/09 |
| Bem ou serviço prestado | `bem_ou_servico_prestado`      | Texto | COMPRA DE SABONETE LIQUIDO |
| Natureza | `natureza`      | Texto | 339030210000 - Mat. de Limpeza e Prod.de Higieniza |
| Ação | `acao`      | Texto | 2075 - Manutencao da FHFS |
| Função<a name="function-note">1</a> | `funcao`      | Texto | 10 - SAUDE |
| Subfunção<a name="function-note">1</a> | `subfuncao`      | Texto | 302 - ASSISTENCIA HOSPITALAR E AMBUL |
| Processo licitatório | `processo_licitatorio`      | Texto | TOMADA DE PRECO |
| Fonte de Recurso | `fonte_recurso`      | Texto | 0002 - REC.IMP.TRANSF.IMP.SAUDE 15% |

<sup>[1](#function-note)</sup> Uma lista com funções e subfunções pode ser encontrada [aqui](http://www.tesouro.fazenda.gov.br/documents/10180/456785/Classifica%C3%A7%C3%A3o+Funcional.pdf/aa2723e7-850f-4098-9c4c-4e194f0f914c) no site do Ministério da Fazenda.
