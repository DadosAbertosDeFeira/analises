import os

import requests


def get_geocode_info(address, raise_exception=False):
    """Coleta informações de um endereço na HERE API."""
    if not address or len(address) < 3:
        if raise_exception:
            raise ValueError("Endereço inválido.")
        return []
    params = {
        "apiKey": os.getenv("HERE_API_KEY"),
        "q": address.strip(),
        "in": "countryCode:BRA",
    }
    response = requests.get(
        "https://geocode.search.hereapi.com/v1/geocode", params=params
    )
    if raise_exception:
        response.raise_for_status()

    results = []
    payload = response.json()

    if len(payload.get("items", [])) > 0:
        return payload["items"]
    return results
