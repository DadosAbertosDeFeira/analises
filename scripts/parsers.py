def currency_to_float(value):
    """Converte de R$ 69.848,70 (str) para 69848.70 (float)."""
    try:
        cleaned_value = value.replace("R$", "").replace(".", "").replace(",", ".")
        return float(cleaned_value)
    except ValueError:
        return


def clean_bidding_process(bidding_process: str):
    """Corrige typos no campo processo LICITATORIO no dataset de pagamentos
    Retorna o tipo do processo licitatorio em minúsculo"""
    if not isinstance(bidding_process, str):
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

    process = bidding_process.lower()

    if process in isento:
        return "isento"
    if process in pregao:
        return "pregao"
    if process in dispensa:
        return "dispensa"
    if process in concorrencia:
        return "concorrencia"
    if process in inexigibilidade:
        return "inexigibilidade"
    if process in tomada_de_preco:
        return "tomada de preco"
    return process
