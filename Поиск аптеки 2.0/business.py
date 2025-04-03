import requests


def find_nearest_business(coords, business_type):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    search_params = {
        "apikey": api_key,
        "text": business_type,
        "lang": "ru_RU",
        "ll": f"{coords[0]},{coords[1]}",
        "type": "biz",
        "results": 1
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        return None

    json_response = response.json()
    if not json_response.get("features"):
        return None

    return json_response["features"][0]
