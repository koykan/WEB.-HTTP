from io import BytesIO
import requests
from PIL import Image
from geocoder import get_toponym_coordinates, get_spn


def show_map(toponym_to_find):
    toponym = get_toponym_coordinates(toponym_to_find)
    if not toponym:
        print("Адрес не найден")
        return False

    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_latitude = toponym_coordinates.split(" ")
    spn = get_spn(toponym)

    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    map_params = {
        "ll": f"{toponym_longitude},{toponym_latitude}",
        "spn": spn,
        "apikey": apikey,
        "l": "map",
        "pt": f"{toponym_longitude},{toponym_latitude},pm2rdm"
    }

    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print("Ошибка загрузки карты")
        return False

    image = Image.open(BytesIO(response.content))
    image.show()
    return True
