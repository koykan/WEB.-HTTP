import sys
import requests

# Возможные значения параметра kind в Geocoder API:
# - house: дом
# - street: улица
# - metro: станция метро
# - district: район (административный)
# - locality: населенный пункт
# - country: страна
# - province: регион
# - area: область
# - hydro: водный объект
# - railway: железная дорога
# - route: маршрут
# - other: другие объекты

API_KEY_GEOCODE = '8013b162-6b42-4997-9691-77b7074026e0'
SERVER_ADDRESS = 'http://geocode-maps.yandex.ru/1.x/'


def get_toponym_district(address):
    geocoder_params = {
        "apikey": API_KEY_GEOCODE,
        "geocode": address,
        "format": "json"
    }

    response = requests.get(SERVER_ADDRESS, params=geocoder_params)
    if not response.ok:
        return None

    json_response = response.json()
    try:
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        pos = toponym["Point"]["pos"]
        lon, lat = pos.split()
    except (IndexError, KeyError):
        return None

    reverse_geocoder_params = {
        "apikey": API_KEY_GEOCODE,
        "geocode": f"{lon},{lat}",
        "kind": "district",
        "format": "json",
        "results": 10
    }

    response = requests.get(SERVER_ADDRESS, params=reverse_geocoder_params)
    if not response.ok:
        return None

    json_response = response.json()
    try:
        features = json_response["response"]["GeoObjectCollection"]["featureMember"]
        for feature in features:
            geo_object = feature["GeoObject"]
            meta = geo_object["metaDataProperty"]["GeocoderMetaData"]

            if (meta["kind"] == "district" and
                    "район" in geo_object["name"].lower() and
                    not any(word in geo_object["name"].lower()
                            for word in ["жилой", "комплекс", "квартал"])):
                return geo_object["name"]

        for feature in features:
            geo_object = feature["GeoObject"]
            if geo_object["metaDataProperty"]["GeocoderMetaData"]["kind"] == "district":
                return geo_object["name"]
    except (KeyError, IndexError):
        return None

    return None


def main():
    if len(sys.argv) < 2:
        print("Укажите адрес в качестве аргумента командной строки")
        return

    address = " ".join(sys.argv[1:])
    district = get_toponym_district(address)

    if district:
        print(f"\nАдрес '{address}' находится в районе: {district}")
    else:
        print(f"\nНе удалось определить район для адреса: {address}")


if __name__ == "__main__":
    main()
