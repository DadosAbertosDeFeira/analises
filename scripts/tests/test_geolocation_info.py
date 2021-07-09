import pytest
from scripts.geolocation_info import get_geocode_info

here_geocoder_api_payload = {
    "items": [
        {
            "address": {
                "city": "Feira de Santana",
                "countryCode": "BRA",
                "countryName": "Brasil",
                "label": "Avenida Getúlio Vargas, Feira de Santana - BA, Brasil",
                "state": "Bahia",
                "stateCode": "BA",
                "street": "Avenida Getúlio Vargas",
            },
            "id": "here:af:streetsection:W6ZqoDi2lzPsqbE8oSDyGD",
            "mapView": {
                "east": -38.93226,
                "north": -12.25508,
                "south": -12.25626,
                "west": -38.96541,
            },
            "position": {"lat": -12.25585, "lng": -38.94944},
            "resultType": "street",
            "scoring": {
                "fieldScore": {"city": 1.0, "streets": [1.0]},
                "queryScore": 1.0,
            },
            "title": "Avenida Getúlio Vargas, Feira de Santana - BA, Brasil",
        }
    ]
}


@pytest.fixture
def mock_here_api(mocker):
    mock_get = mocker.patch("scripts.geolocation_info.requests.get")
    mock_get.return_value.json.return_value = here_geocoder_api_payload
    return mock_get


def test_geolocation_info_from_address(mock_here_api):
    results = get_geocode_info("Rua Quitino Bocaiuva 100")

    assert results != []
    assert isinstance(results, list)


@pytest.mark.parametrize("address", [None, False, "A", "Av"])
def test_do_not_call_api_if_address_is_invalid_or_short(mock_here_api, address):
    with pytest.raises(ValueError):
        get_geocode_info(address, raise_exception=True)


def test_return_empty_dict_when_cannot_find_results(mocker):
    mock_get = mocker.patch("scripts.geolocation_info.requests.get")
    mock_get.return_value.json.return_value = {"items": []}

    assert get_geocode_info("Karl-Marx Alle 100") == []
