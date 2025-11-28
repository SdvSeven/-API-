import requests

API_KEY = "ВАШ_API_КЛЮЧ"
city = "Saint Petersburg"

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"

response = requests.get(url)
data = response.json()

print("Температура:", data["main"]["temp"], "°C")
print("Ощущается как:", data["main"]["feels_like"], "°C")
print("Влажность:", data["main"]["humidity"], "%")
print("Описание:", data["weather"][0]["description"])
