import requests
from io import BytesIO
from PIL import Image


def show_map(point1, point2):
    map_api_server = "https://static-maps.yandex.ru/1.x/"

    center_lon = (point1[0] + point2[0]) / 2
    center_lat = (point1[1] + point2[1]) / 2

    delta_lon = abs(point1[0] - point2[0]) * 1.5
    delta_lat = abs(point1[1] - point2[1]) * 1.5

    map_params = {
        "l": "map",
        "ll": f"{center_lon},{center_lat}",
        "spn": f"{delta_lon},{delta_lat}",
        "pt": f"{point1[0]},{point1[1]},pm2rdm~{point2[0]},{point2[1]},pm2blm"
    }

    response = requests.get(map_api_server, params=map_params)
    if not response:
        return False

    Image.open(BytesIO(response.content)).show()
    return True
