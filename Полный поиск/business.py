import requests
from geocoder import get_toponym_coordinates, get_spn


def find_business(toponym_to_find, business_type):
    toponym = get_toponym_coordinates(toponym_to_find)
    if not toponym:
        return None

    toponym_coordinates = toponym["Point"]["pos"]
    address_ll = ",".join(toponym_coordinates.split())

    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": business_type,
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        return None

    json_response = response.json()
    if not json_response.get("features"):
        return None

    return json_response["features"][0]
