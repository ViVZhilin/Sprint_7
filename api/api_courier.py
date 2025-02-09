import requests

class CourierApi:
    def __init__(self):
        self.base_url = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

    def create_courier(self, login, password, first_name):
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return requests.post(self.base_url, data=payload)

    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        return requests.post(f"{self.base_url}/login", data=payload)