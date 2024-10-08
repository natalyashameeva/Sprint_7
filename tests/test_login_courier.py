import requests
import pytest
from config import BASE_URL
from conftest import create_and_delete_courier

class TestLoginCourier:

    # Тест на успешный логин курьера
    def test_login_courier(self, create_and_delete_courier):
        courier_data = create_and_delete_courier
        login_data = {"login": courier_data["login"], "password": courier_data["password"]}
        response = requests.post(f"{BASE_URL}/api/v1/courier/login", json=login_data)
        assert response.status_code == 200
        assert "id" in response.json()

    # Тест на неверный логин или пароль
    @pytest.mark.parametrize("login, password", [
        ("wrong_login", "courier_password_test"),
        ("courier_login_test", "wrong_password")
    ])
    def test_login_wrong_credentials(self, login, password):
        login_data = {"login": login, "password": password}
        response = requests.post(f"{BASE_URL}/api/v1/courier/login", json=login_data)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    # Тест на отсутствие обязательных полей при логине
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, missing_field):
        login_data = {"login": "courier_login_test", "password": "courier_password_test"}
        del login_data[missing_field]
        response = requests.post(f"{BASE_URL}/api/v1/courier/login", json=login_data)
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.json()["message"]
