import sys
import requests


def get_toponym_district(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": address,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response.ok:
        return None

    json_response = response.json()
    try:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        pos = toponym["Point"]["pos"]
        lon, lat = pos.split()
    except (IndexError, KeyError):
        return None

    reverse_geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": f"{lon},{lat}",
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=reverse_geocoder_params)
    if not response.ok:
        return None

    json_response = response.json()
    try:
        features = json_response["response"]["GeoObjectCollection"]["featureMember"]
        for feature in features:
            geo_object = feature["GeoObject"]
            meta = geo_object["metaDataProperty"]["GeocoderMetaData"]

            if meta["kind"] in ["district", "province"] and "район" in geo_object["name"].lower():
                return geo_object["name"]

            if "AddressDetails" in meta:
                for component in meta["AddressDetails"]["Country"]["AddressLine"]:
                    if "район" in component.lower():
                        return component
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
