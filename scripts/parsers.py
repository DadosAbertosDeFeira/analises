def currency_to_float(value):
    """Converte de R$ 69.848,70 (str) para 69848.70 (float)."""
    try:
        cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
        return float(cleaned_value)
    except ValueError:
        return


def limpa_processo_licitatorio(procecimento: str):
    """Corrige typos no campo PROCESSO LICITATORIO no dataset de pagamentos
    Retorna o tipo do processo licitatorio em minúsculo"""
    if not isinstance(procecimento, str):
        return

    isento = ["isento", "ento", "sento"]
    pregao = ["pregao", "regao", "egao"]
    dispensa = ["dispensa", "spensa", "ispensa", "pensa"]
    concorrencia = ["concorrencia", "concorencia", "oncorrencia", "ncorrencia"]
    inexigibilidade = [
        "inexigibilidade",
        "nexigibilidade",
        "inexibilidade",
        "xigibilidade",
        "exigibilidade",
    ]
    tomada_de_preco = ["tomada de preco", "omada de preco"]

    processo = procecimento.lower()

    if processo in isento:
        return "isento"
    if processo in pregao:
        return "pregao"
    if processo in dispensa:
        return "dispensa"
    if processo in concorrencia:
        return "concorrencia"
    if processo in inexigibilidade:
        return "inexigibilidade"
    if processo in tomada_de_preco:
        return "tomada de preco"
    return procecimento
