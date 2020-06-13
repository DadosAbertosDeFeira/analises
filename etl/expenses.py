import re


def identify_code_and_description(row):
    """Identifica classificação da despesa e sua descrição.
    
    Exemplo de entradas esperadas:

    CO	GD	MA	ED	SED	Código	     Código sem máscara   Descrição
    3	0	00	00	00	3.0.00.00.00 30000000 Despesas Correntes
    3 	1	00	00	00	3.1.00.00.00 31000000 Pessoal e Encargos Sociais
    3	1	71	00	00	3.1.71.00.00 31710000 Transferências a Consórcios Públicos Mediante Contrato de Rateio
    3	1	71	70	00	3.1.71.70.00 31717000 Rateio pela Participação em Consórcio Público
    3	1	90	01	01	3.1.90.01.01 31900101 Aposentadorias Custeadas com Recursos do RPPS
    """
    from_pandas = False
    try:
        import pandas as pd
        if isinstance(row, pd.Series) or isinstance(row, pd.DataFrame):
            from_pandas = True
    except:
        pass
    if from_pandas:
        if row.empty or len(row) < 7:
            return
    elif not row or len(row) < 7:
            return

    code_and_description = {'code': row[5], 'description': row[7]}

    is_gd_empty = row[1] == '0'
    is_ma_empty = row[2] == '00'
    is_ed_empty = row[3] == '00'
    is_sed_empty = row[4] == '00'

    is_co = all([
        is_gd_empty,
        is_ma_empty,
        is_ed_empty,
        is_sed_empty,
    ])
    if is_co:
        code_and_description['value'] = row[0]
        code_and_description['group'] = 'CO'
        return code_and_description
    is_gd = all([
        is_ma_empty,
        is_ed_empty,
        is_sed_empty,
    ])
    if is_gd:
        code_and_description['value'] = row[1]
        code_and_description['group'] = 'GD'
        return code_and_description
    is_ma = all([
        is_ed_empty,
        is_sed_empty,
    ])
    if is_ma:
        code_and_description['value'] = row[2]
        code_and_description['group'] = 'MA'
        return code_and_description
    is_ed = is_sed_empty
    if is_ed:
        code_and_description['value'] = row[3]
        code_and_description['group'] = 'ED'
        return code_and_description
    is_sed = not all([
        is_gd_empty,
        is_ma_empty,
        is_ed_empty,
        is_sed_empty,
    ])
    if is_sed:
        code_and_description['value'] = row[4]
        code_and_description['group'] = 'SED'
        return code_and_description


def extract_classification(string):
    """Extrai classificação da natureza de uma string e retorna seu código.

    Formato: `339030040000000000 - Medicamentos`
    Deve retornar: `33903004`
    """
    match = re.match(r'\d{8}', string)
    if match:
        return match.group(0)
