# weather_app_glass_cities.py
import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QComboBox
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

API_KEY = "c2a4d1266d197ad340d88be4ae677f1d"

# --- Список городов ---
CITIES = ["Saint Petersburg", "Moscow", "Astrakhan"]

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Погода на iPhone")
        self.setFixedSize(400, 800)

        self.city = "Saint Petersburg"  # город по умолчанию

        # --- Фон с телефоном ---
        self.phone_label = QLabel(self)
        pixmap = QPixmap("/Users/sdv7/Desktop/API/phone.webp")
        self.phone_label.setPixmap(pixmap)
        self.phone_label.setGeometry(0, 0, 400, 800)
        self.phone_label.setScaledContents(True)

        # --- Верхний текст ---
        self.instruction_label = QLabel(
            "Выберите город \n Нажмите 'Погода' ☁️", self)
        self.instruction_label.setFont(QFont("Arial", 20))
        self.instruction_label.setGeometry(20, 50, 360, 50)
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setStyleSheet("color: black;")

        # --- Панель выбора города (стеклянная) ---
        self.city_button = QComboBox(self)
        self.city_button.setGeometry(120, 640, 160, 35)
        self.city_button.addItems(["Санкт-Петербург", "Москва", "Астрахань"])
        self.city_button.currentIndexChanged.connect(self.change_city)
        self.city_button.setStyleSheet("""
            QComboBox {
                color: black;
                background: rgba(200, 200, 200, 0.3);
                border-radius: 20px;
                padding: 5px;
                font-weight: bold;
            }
            QComboBox QAbstractItemView {
                background: rgba(200, 200, 200, 0.4);
                selection-background-color: rgba(180,180,180,0.5);
                color: black;
            }
        """)

        # --- Кнопка "Погода" ---
        self.weather_button = QPushButton("Погода", self)
        self.weather_button.setGeometry(150, 700, 100, 40)
        self.weather_button.setStyleSheet("""
            color: black;
            background: rgba(255, 255, 255, 0.4);
            border-radius: 20px;
            font-weight: bold;
        """)
        self.weather_button.clicked.connect(self.show_weather)

        # --- Метка для иконки погоды ---
        self.icon_label = QLabel(self)
        self.icon_label.setGeometry(150, 250, 100, 100)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Метка для температуры ---
        self.temp_label = QLabel("", self)
        self.temp_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        self.temp_label.setGeometry(50, 370, 300, 80)
        self.temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp_label.setStyleSheet("""
            color: black;
            background: rgba(200, 200, 200, 0.3);
            border-radius: 30px;
            padding: 15px;
        """)

        # --- Метка для описания погоды ---
        self.desc_label = QLabel("", self)
        self.desc_label.setFont(QFont("Arial", 16))
        self.desc_label.setGeometry(50, 470, 300, 50)
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc_label.setStyleSheet("""
            color: black;
            background: rgba(200, 200, 200, 0.3);
            border-radius: 25px;
            padding: 10px;
        """)

    # --- Смена города ---
    def change_city(self, index):
        self.city = CITIES[index]

    # --- Получение погоды для выбранного города ---
    def get_weather(self):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={API_KEY}&units=metric&lang=ru"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            temp = data['main']['temp']
            weather_desc = data['weather'][0]['description'].lower()
            return temp, weather_desc
        except Exception as e:
            print("Ошибка при получении погоды:", e)
            return None, None

    # --- Показ погоды на экране ---
    def show_weather(self):
        temp, desc = self.get_weather()
        if temp is not None:
            self.temp_label.setText(f"{int(temp)}°C")
            self.desc_label.setText(desc.capitalize())

            # --- Выбор иконки для нового списка состояний ---
            if "снег" in desc and "дождь" in desc:
                pix = QPixmap("/Users/sdv7/Desktop/API/snow and rain.svg")
            elif "снег" in desc:
                pix = QPixmap("/Users/sdv7/Desktop/API/snow.png")
            elif "дождь" in desc:
                pix = QPixmap("/Users/sdv7/Desktop/API/rain.png")
            elif "гроза" in desc:
                pix = QPixmap("/Users/sdv7/Desktop/API/thunderstorm.png")
            elif "пасмурно" in desc or "облачно" in desc:
                pix = QPixmap("/Users/sdv7/Desktop/API/cloudy.svg")
            elif "облачно с прояснениями" in desc:
                pix = QPixmap("/Users/sdv7/Desktop/API/partly cloudy.png")
            elif "ясно" in desc or "sun" in desc:
                pix = QPixmap("/Users/sdv7/Desktop/API/sun.png")
            else:
                pix = QPixmap("")

            self.icon_label.setPixmap(pix)
            self.icon_label.setScaledContents(True)
        else:
            self.temp_label.setText("Ошибка")
            self.desc_label.setText("Не удалось получить данные")
            self.icon_label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
