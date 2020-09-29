def currency_to_float(value):
    """Converte de R$ 69.848,70 (str) para 69848.70 (float)."""
    try:
        cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
        return float(cleaned_value)
    except ValueError:
        return

def limpa_proc_licitatorio(proc: str) -> str:
    """Corrige typos no campo PROCESSO LICITATORIO no dataset de pagamentos
    Retorna o tipo do processo licitatorio em minúsculo"""
    
    isento = ['ISENTO', 'ENTO', 'Isento', 'SENTO', 'sento']
    pregao = ['PREGAO', 'REGAO', 'Pregao', 'EGAO', 'egao']
    dispensa = ['DISPENSA', 'SPENSA', 'ISPENSA', 'Dispensa', 'PENSA', 'pensa']
    concorrencia = ['CONCORENCIA', 'ONCORRENCIA', 'NCORRENCIA']
    inexigibilidade = ['INEXIGIBILIDADE', 'NEXIGIBILIDADE', 'Inexibilidade', 'XIGIBILIDADE',
     'xigibilidade', 'EXIGIBILIDADE', 'exigibilidade']
    tomada_de_preco = ['TOMADA DE PRECO', 'OMADA DE PRECO', 'omada de preco']

    if (type(proc) != str):
        return None
    try:
        if (proc in isento):
            return 'isento'
        elif (proc in pregao):
            return 'pregao'
        elif (proc in dispensa):
            return 'dispensa'
        elif (proc in concorrencia):
            return 'concorrencia'
        elif (proc in inexigibilidade):
            return 'inexigibilidade'
        elif (proc in tomada_de_preco):
            return 'tomada de preco'
        else:
            return proc.lower()
    except TypeError:
        pass
