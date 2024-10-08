import requests
import pytest
from config import BASE_URL


class TestCourierCreate:
    # Тест на создание курьера
    def test_create_courier_success(self, unique_courier_data):
        response = requests.post(f"{BASE_URL}/api/v1/courier", json=unique_courier_data)

        assert response.status_code == 201, "Неверный статус код для успешного создания"
        assert response.json() == {"ok": True}, "Ответ должен содержать ok: true"

        # Удаление курьера
        login_data = {"login": unique_courier_data["login"], "password": unique_courier_data["password"]}
        login_response = requests.post(f"{BASE_URL}/courier/login", json=login_data)
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

    # Тест на создание курьера с дублирующим логином
    def test_create_courier_duplicate(self, create_and_delete_courier):
        duplicate_courier_data = {
            "login": create_and_delete_courier["login"],
            "password": "another_password",
            "firstName": "DuplicateCourier"
        }

        response = requests.post(f"{BASE_URL}/api/v1/courier", json=duplicate_courier_data)

        assert response.status_code == 409
        assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    # Тест на отсутствие обязательных полей (логина или пароля)
    def test_create_courier_missing_fields(self, unique_courier_data, missing_field):

        # Удаляем одно из обязательных полей ('login' или 'password')
        unique_courier_data.pop(missing_field)

        response = requests.post(f"{BASE_URL}/api/v1/courier", json=unique_courier_data)

        # Проверка, что при отсутствии обязательного поля возвращается ошибка 400
        assert response.status_code == 400
        assert "message" in response.json()


