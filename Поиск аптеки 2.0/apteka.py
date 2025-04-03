import sys
from geocoder import get_toponym_info, get_coordinates
from business import find_nearest_business
from distance import calculate_distance
from mapapi import show_map


def main():
    if len(sys.argv) < 2:
        return

    address = " ".join(sys.argv[1:])

    toponym = get_toponym_info(address)
    if not toponym:
        print("Адрес не найден")
        return

    address_coords = get_coordinates(toponym)

    pharmacy = find_nearest_business(address_coords, "аптека")
    if not pharmacy:
        print("Аптека не найдена")
        return

    pharmacy_coords = pharmacy["geometry"]["coordinates"]
    pharmacy_meta = pharmacy["properties"]["CompanyMetaData"]

    distance = calculate_distance(address_coords, pharmacy_coords)

    print("\nИнформация об аптеке:")
    print(f"Название: {pharmacy_meta['name']}")
    print(f"Адрес: {pharmacy_meta['address']}")
    print(f"Время работы: {pharmacy_meta.get('Hours', {}).get('text', 'нет данных')}")
    print(f"Расстояние: {round(distance, 2)} метров")

    show_map(address_coords, pharmacy_coords)


if __name__ == "__main__":
    main()
