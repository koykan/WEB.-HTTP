import requests


def find_businesses(coords, business_type, results=10):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": business_type,
        "lang": "ru_RU",
        "ll": f"{coords[0]},{coords[1]}",
        "type": "biz",
        "results": results
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        return None

    json_response = response.json()
    return json_response.get("features", [])
