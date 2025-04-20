import requests
from io import BytesIO
from PIL import Image


def get_point_color(pharmacy):
    hours = pharmacy["properties"]["CompanyMetaData"].get("Hours", {})
    if not hours:
        return "pm2grm"

    hours_text = hours.get("text", "").lower()
    if "круглосуточно" in hours_text:
        return "pm2gnm"
    return "pm2blm"


def show_pharmacies_map(address_coords, pharmacies):
    map_api_server = "https://static-maps.yandex.ru/1.x/"

    points = []
    for pharmacy in pharmacies:
        try:
            coords = pharmacy["geometry"]["coordinates"]
            color = get_point_color(pharmacy)
            points.append(f"{coords[0]},{coords[1]},{color}")
        except (KeyError, TypeError):
            continue

    points.append(f"{address_coords[0]},{address_coords[1]},pm2rdm")

    if not points:
        print("Нет точек для отображения на карте")
        return False

    all_coords = [address_coords] + [pharmacy["geometry"]["coordinates"] for pharmacy in pharmacies]
    min_lon = min(c[0] for c in all_coords)
    max_lon = max(c[0] for c in all_coords)
    min_lat = min(c[1] for c in all_coords)
    max_lat = max(c[1] for c in all_coords)

    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2
    delta_lon = max(0.01, (max_lon - min_lon) * 1.2)
    delta_lat = max(0.01, (max_lat - min_lat) * 1.2)

    map_params = {
        "l": "map",
        "ll": f"{center_lon},{center_lat}",
        "spn": f"{delta_lon},{delta_lat}",
        "pt": "~".join(points),
        "size": "650,450"
    }

    try:
        response = requests.get(map_api_server, params=map_params)
        if not response.ok:
            print(f"Ошибка API: {response.status_code} - {response.reason}")
            print(f"Полный URL: {response.url}")
            return False

        Image.open(BytesIO(response.content)).show()
        return True
    except Exception as e:
        print(f"Ошибка при загрузке карты: {str(e)}")
        return False
