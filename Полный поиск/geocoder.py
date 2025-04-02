import requests


def get_toponym_coordinates(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
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


def get_spn(toponym):
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = envelope["lowerCorner"].split()
    upper_corner = envelope["upperCorner"].split()

    delta_lon = str(abs(float(upper_corner[0]) - float(lower_corner[0])) / 2)
    delta_lat = str(abs(float(upper_corner[1]) - float(lower_corner[1])) / 2)

    return f"{delta_lon},{delta_lat}"
