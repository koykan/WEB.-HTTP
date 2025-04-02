from geocoder import get_toponym_coordinates


def calculate_distance(address1, address2):
    toponym1 = get_toponym_coordinates(address1)
    toponym2 = get_toponym_coordinates(address2)

    if not toponym1 or not toponym2:
        return None

    coords1 = list(map(float, toponym1["Point"]["pos"].split()))
    coords2 = list(map(float, toponym2["Point"]["pos"].split()))

    distance = ((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2) ** 0.5
    return distance
