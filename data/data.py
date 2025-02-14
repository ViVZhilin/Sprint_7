from symtable import Class

import requests
import random
import string

class Data:
    test_login = "zhilin_17@yandex.ru"
    test_password = "123456"
    test_firstName = "viktor"
    first_name = "Иван"
    last_name = "Иванов"
    address = "Москва, ул. Ленина, 10"
    metro_station = 5
    phone = "+79999999999"
    rent_time = 3
    delivery_date = "2023-10-10"
    comment = "Тестовый заказ"
    base_url = "https://qa-scooter.praktikum-services.ru"
    courier_url = f"{base_url}/api/v1/courier"
    login_url = f"{base_url}/api/v1/courier/login"


    # метод регистрации нового курьера возвращает список из логина и пароля
    # если регистрация не удалась, возвращает пустой список
    def register_new_courier_and_return_login_password(self):
        # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        # создаём список, чтобы метод мог его вернуть
        login_pass = []

        # генерируем логин, пароль и имя курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post(Data.courier_url, data=payload)

        # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)

        # возвращаем список
        return login_pass