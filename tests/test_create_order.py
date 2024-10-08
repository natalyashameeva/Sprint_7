import requests
import pytest
from config import BASE_URL


class TestCreateOrder:

    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order(self, color):
        order_data = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "Москва, Проспект Мира, 3",
            "metroStation": 4,
            "phone": "+7 800 555 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-11-26",
            "comment": "Комментарий",
            "color": color
        }
        response = requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)
        assert response.status_code == 201
        assert "track" in response.json()
