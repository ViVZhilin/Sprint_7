import string

import pytest
import requests
import allure
import random

from api.api_courier import CourierApi
from data.data import Data

@pytest.fixture
def courier():
    return CourierApi()

class TestCourierCreation:

    @allure.title("Регистрация нового курьера")
    def test_courier_creation(self):
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

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
        assert response.text == '{"ok":true}'


    @allure.title("Проверка невозможности создания курьера с теми же данными")
    def test_cannot_create_duplicate_courier(self):

        self.courier = Data.register_new_courier_and_return_login_password(self)
        self.base_url = Data.courier_url
        payload = {
            'login' : self.courier[0],
            'password': self.courier[1],
            'first_name' : self.courier[2]
        }
        response = requests.post(Data.courier_url, data=payload)
        assert response.status_code == 409

    @allure.title("Проверка заполнения всех обязательных параметров")
    def test_required_fields_for_courier_creation(self):

        self.base_url = Data.courier_url
        for field in ["login", "password", "firstName"]:
            payload = {
                "login": Data.register_new_courier_and_return_login_password(self)[0],
                "password": Data.register_new_courier_and_return_login_password(self)[1],
                "firstName": Data.register_new_courier_and_return_login_password(self)[2]
            }
            del payload[field]
            response = requests.post(self.base_url, data=payload)
            assert response.status_code == 400, (
                f"При отсутствии поля '{field}' код должен быть 400, получено {response.status_code}. "
                f"Ответ сервера: {response.text}"
            )

class TestCourierLogin:

    @allure.title("Авторизация существующим курьером")
    def test_courier_login(self):
        payload = {
            "login": "zhilin_17@yandex.ru",
            "password": "123456",
        }

        self.base_url = Data.login_url
        response = requests.post(self.base_url, data = payload)
        assert response.status_code == 200

        response_data = response.json()
        assert "id" in response_data
        print(f"ID курьера - {response_data['id']}")

    @allure.title("Проверка пустых значений обязательных полей при авторизации")
    def test_empty_required_fields_for_courier_login(self):
        base_url = Data.login_url

        # Проверяем оба обязательных поля
        for field in ["login", "password"]:
            with allure.step(f"Проверка авторизации с пустым полем '{field}'"):
                # Создаем копию тестовых данных
                payload = {
                    "login": Data.test_login,
                    "password": Data.test_password
                }

                # Заменяем значение проверяемого поля на пустую строку
                payload[field] = ""

                # Отправляем запрос с таймаутом
                response = requests.post(base_url, data=payload, timeout=(5, 10))

                # Проверяем ответ
                assert response.status_code == 400