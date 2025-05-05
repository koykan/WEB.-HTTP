import random
import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from math import radians, cos, sin, asin, sqrt

CITIES = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
    "Нижний Новгород", "Челябинск", "Самара", "Омск", "Ростов-на-Дону",
    "Сочи", "Краснодар", "Владивосток", "Ярославль", "Иркутск"
]

GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
MAPS_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"


class CityGuessingGame:
    def __init__(self):
        self.cities = CITIES.copy()
        random.shuffle(self.cities)
        self.current_city_index = 0
        self.score = 0
        self.root = tk.Tk()
        self.root.title("Угадай город")
        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("800x650")

        # Main image frame
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # UI elements
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.score_label = tk.Label(control_frame, text="Счёт: 0", font=("Arial", 12))
        self.score_label.pack(side=tk.LEFT)

        self.answer_entry = tk.Entry(control_frame, font=("Arial", 12), width=25)
        self.answer_entry.pack(side=tk.LEFT, padx=5)
        self.answer_entry.bind("<Return>", self.check_answer)

        self.check_button = tk.Button(
            control_frame,
            text="Проверить",
            command=self.check_answer,
            font=("Arial", 12)
        )
        self.check_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(
            control_frame,
            text="Следующий",
            command=self.show_next_city,
            font=("Arial", 12)
        )
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.answer_label = tk.Label(
            control_frame,
            text="",
            font=("Arial", 12, "bold"),
            width=30
        )
        self.answer_label.pack(side=tk.LEFT, padx=5)

        self.show_next_city()

    def haversine(self, lon1, lat1, lon2, lat2):
        """Calculate distance between two points on Earth"""
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        return 2 * 6371 * asin(sqrt(a)) * 1000  # meters

    def get_city_data(self, city_name):
        """Get city coordinates and boundaries"""
        geocoder_params = {
            "apikey": GEOCODER_API_KEY,
            "geocode": city_name,
            "format": "json"
        }

        try:
            response = requests.get(
                "http://geocode-maps.yandex.ru/1.x/",
                params=geocoder_params,
                timeout=5
            )

            if response.ok:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                pos = toponym["Point"]["pos"]

                # Get city boundaries
                envelope = toponym["boundedBy"]["Envelope"]
                lower_corner = list(map(float, envelope["lowerCorner"].split()))
                upper_corner = list(map(float, envelope["upperCorner"].split()))

                # Calculate city center and size
                center_lon = (lower_corner[0] + upper_corner[0]) / 2
                center_lat = (lower_corner[1] + upper_corner[1]) / 2
                city_width = self.haversine(lower_corner[0], center_lat, upper_corner[0], center_lat)
                city_height = self.haversine(center_lon, lower_corner[1], center_lon, upper_corner[1])

                return {
                    "center": [center_lon, center_lat],
                    "bounds": [lower_corner, upper_corner],
                    "size": max(city_width, city_height)  # in meters
                }
        except Exception as e:
            print(f"Geocoder error: {e}")

        return None

    def get_city_map(self, city_name):
        """Get map image without city name"""
        city_data = self.get_city_data(city_name)
        if not city_data:
            return None

        # Случайная точка в пределах города (избегаем центр)
        bounds = city_data["bounds"]
        offset_lon = random.uniform(0.2, 0.8) * (bounds[1][0] - bounds[0][0])
        offset_lat = random.uniform(0.2, 0.8) * (bounds[1][1] - bounds[0][1])
        random_lon = bounds[0][0] + offset_lon
        random_lat = bounds[0][1] + offset_lat

        # Фиксированный небольшой масштаб
        span_degrees = 0.03  # Оптимально для скрытия подписей

        map_params = {
            "l": "sat",  # Спутник без подписей
            "ll": f"{random_lon},{random_lat}",
            "spn": f"{span_degrees},{span_degrees}",
            "size": "650,450",
            "apikey": MAPS_API_KEY
        }

        try:
            response = requests.get(
                "https://static-maps.yandex.ru/1.x/",
                params=map_params,
                timeout=5
            )
            if response.ok:
                return Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"Ошибка: {e}")
        return None

    def show_next_city(self):
        """Show next city map"""
        max_attempts = len(self.cities) * 2  # Максимальное число попыток
        attempts = 0

        while attempts < max_attempts:
            if self.current_city_index >= len(self.cities):
                self.current_city_index = 0
                random.shuffle(self.cities)
                self.answer_label.config(text="Городы закончились! Начинаем заново.")

            self.current_city = self.cities[self.current_city_index]
            city_map = self.get_city_map(self.current_city)

            if city_map:
                # Resize while maintaining aspect ratio
                city_map.thumbnail((700, 500), Image.LANCZOS)

                photo = ImageTk.PhotoImage(city_map)
                self.image_label.config(image=photo)
                self.image_label.image = photo
                self.answer_label.config(text="")
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
                self.current_city_index += 1
                return  # Успешно загрузили карту, выходим из метода

            # Если карта не загрузилась, переходим к следующему городу
            self.current_city_index += 1
            attempts += 1
            print(f"Ошибка загрузки города: {self.current_city}. Пропускаем.")

        # Если все попытки исчерпаны
        self.answer_label.config(text="Не удалось загрузить карты. Проверьте интернет или API-ключи.")

    def check_answer(self, event=None):
        """Check user's answer"""
        user_answer = self.answer_entry.get().strip()

        if not user_answer:
            return

        if user_answer.lower() == self.current_city.lower():
            self.score += 1
            self.score_label.config(text=f"Счёт: {self.score}")
            self.answer_label.config(text="Правильно!", fg="green")
        else:
            self.answer_label.config(text=f"Неверно! Это {self.current_city}", fg="red")

        self.root.after(2000, self.show_next_city)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = CityGuessingGame()
    game.run()
