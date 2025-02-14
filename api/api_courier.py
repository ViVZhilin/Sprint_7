import requests
from data.data import Data

class CourierApi:
    def __init__(self):
        self.base_url = Data.courier_url

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