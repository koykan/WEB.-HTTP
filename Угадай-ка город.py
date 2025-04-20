import random
import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

CITIES = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
    "Нижний Новгород", "Челябинск", "Самара", "Омск", "Ростов-на-Дону"
]

GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
MAPS_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"


class CityGuessingGame:
    def __init__(self):
        self.cities = CITIES.copy()
        random.shuffle(self.cities)
        self.current_city_index = 0
        self.root = tk.Tk()
        self.root.title("Угадай город")
        self.setup_ui()

    def setup_ui(self):
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.next_button = tk.Button(
            self.root,
            text="Следующий город",
            command=self.show_next_city
        )
        self.next_button.pack()

        self.answer_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.answer_label.pack()

        self.show_button = tk.Button(
            self.root,
            text="Показать ответ",
            command=self.show_answer
        )
        self.show_button.pack()

        self.show_next_city()

    def get_city_coordinates_and_size(self, city_name):
        geocoder_params = {
            "apikey": GEOCODER_API_KEY,
            "geocode": city_name,
            "format": "json"
        }
        response = requests.get(
            "http://geocode-maps.yandex.ru/1.x/",
            params=geocoder_params
        )

        if response.ok:
            json_response = response.json()
            try:
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                pos = toponym["Point"]["pos"]

                envelope = toponym["boundedBy"]["Envelope"]
                lower_corner = list(map(float, envelope["lowerCorner"].split()))
                upper_corner = list(map(float, envelope["upperCorner"].split()))

                size_lon = abs(upper_corner[0] - lower_corner[0])
                size_lat = abs(upper_corner[1] - lower_corner[1])

                return {
                    "coords": list(map(float, pos.split())),
                    "size": max(size_lon, size_lat) * 0.5
                }
            except (IndexError, KeyError):
                return None
        return None

    def get_city_map(self, city_name):
        city_data = self.get_city_coordinates_and_size(city_name)
        if not city_data:
            return None

        coords = city_data["coords"]
        city_size = city_data["size"]

        spn = min(max(city_size * 0.3, 0.02), 0.1)

        map_params = {
            "l": "map",
            "ll": f"{coords[0]},{coords[1]}",
            "spn": f"{spn},{spn}",
            "apikey": MAPS_API_KEY
        }

        response = requests.get(
            "https://static-maps.yandex.ru/1.x/",
            params=map_params
        )

        if response.ok:
            return Image.open(BytesIO(response.content))
        return None

    def show_next_city(self):
        if self.current_city_index >= len(self.cities):
            self.current_city_index = 0
            random.shuffle(self.cities)

        city = self.cities[self.current_city_index]
        city_map = self.get_city_map(city)

        if city_map:
            width, height = city_map.size
            cropped_map = city_map.crop((50, 50, width - 50, height - 50))

            photo = ImageTk.PhotoImage(cropped_map)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.answer_label.config(text="")
            self.current_city_index += 1
        else:
            self.answer_label.config(text=f"Не удалось загрузить карту для {city}")

    def show_answer(self):
        if self.current_city_index > 0:
            city = self.cities[self.current_city_index - 1]
            self.answer_label.config(text=f"Правильный ответ: {city}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = CityGuessingGame()
    game.run()
