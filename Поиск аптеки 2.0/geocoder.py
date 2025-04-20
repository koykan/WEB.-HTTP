import requests


def get_toponym_info(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": address,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return None

    json_response = response.json()
    try:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return toponym
    except (IndexError, KeyError):
        return None


def get_coordinates(toponym):
    pos = toponym["Point"]["pos"]
    return list(map(float, pos.split()))
