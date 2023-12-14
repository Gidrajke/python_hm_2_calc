import requests
import json

url = 'http://127.0.0.1:5000/calculate'
data = {'expression': '10/0'}  # ваше математическое выражение


# Отправка POST-запроса на сервер с JSON-данными
response = requests.post(url, json=data)

# Вывод результата запроса
print(response.json())
