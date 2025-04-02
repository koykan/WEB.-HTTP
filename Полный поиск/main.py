import sys
from mapapi_PG import show_map

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    toponym_to_find = " ".join(sys.argv[1:])
    if not show_map(toponym_to_find):
        sys.exit(1)
