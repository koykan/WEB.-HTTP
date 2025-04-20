import sys
from geocoder import get_toponym_info, get_coordinates
from business import find_businesses
from mapapi import show_pharmacies_map


def main():
    if len(sys.argv) < 2:
        print("Укажите адрес в качестве аргумента командной строки")
        return

    address = " ".join(sys.argv[1:])

    toponym = get_toponym_info(address)
    if not toponym:
        print("Адрес не найден")
        return

    try:
        address_coords = get_coordinates(toponym)
    except (KeyError, AttributeError):
        print("Не удалось получить координаты для указанного адреса")
        return

    pharmacies = find_businesses(address_coords, "аптека", 10)
    if not pharmacies:
        print("Аптеки не найдены")
        return

    print(f"\nНайдено {len(pharmacies)} аптек:")
    for i, pharmacy in enumerate(pharmacies, 1):
        meta = pharmacy["properties"]["CompanyMetaData"]
        print(f"\n{i}. {meta.get('name', 'Название не указано')}")
        print(f"   Адрес: {meta.get('address', 'нет данных')}")
        print(f"   Время работы: {meta.get('Hours', {}).get('text', 'нет данных')}")

    show_pharmacies_map(address_coords, pharmacies)


if __name__ == "__main__":
    main()
