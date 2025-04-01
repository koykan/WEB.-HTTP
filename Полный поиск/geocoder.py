def get_spn(toponym):
    toponym_delta_1 = list(
        map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split()))
    toponym_delta_2 = list(
        map(float, toponym['boundedBy']['Envelope']['upperCorner'].split()))
    delta1 = str(abs(toponym_delta_1[0] - toponym_delta_2[0]))
    delta2 = str(abs(toponym_delta_1[1] - toponym_delta_2[1]))
    return delta1, delta2
