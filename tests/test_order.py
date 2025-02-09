import pytest
import allure
import requests

from api.api_order import OrderApi
from data.data import Data

@pytest.fixture
def order():
    return OrderApi()

class TestOrder:
    @allure.title("Проверка оформления заказа")
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_different_colors(self, order, color):

        response = order.create_order(
            first_name=Data.first_name,
            last_name=Data.last_name,
            address=Data.address,
            metro_station=Data.metro_station,
            phone=Data.phone,
            rent_time=Data.rent_time,
            delivery_date=Data.delivery_date,
            comment=Data.comment,
            color=color
        )
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Проверка получения списка заказов")
    def test_get_orders_list(self, order):
        response = order.get_orders_list()

        # Проверяем, что возвращается список заказов
        assert response.status_code == 200
        assert "orders" in response.json()