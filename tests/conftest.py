import pytest
import requests
import random
import string
import sys
import os

# Добавляем корневую директорию проекта в путь поиска модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import BASE_URL
from helpers import register_new_courier_and_return_login_password


@pytest.fixture(scope="function")
def create_and_delete_courier():
    """Фикстура для создания и удаления курьера."""
    # Регистрируем нового курьера с помощью вспомогательной функции
    login_pass = register_new_courier_and_return_login_password()

    if not login_pass:
        pytest.fail("Не удалось создать курьера для теста")

    courier_data = {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }

    # Возвращаем данные курьера для использования в тестах
    yield courier_data

    # После завершения теста удаляем курьера
    login_data = {"login": courier_data["login"], "password": courier_data["password"]}
    login_response = requests.post(f"{BASE_URL}/courier/login", json=login_data)
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")


@pytest.fixture(scope="function")
def unique_courier_data():
    """Фикстура для создания уникальных данных курьера."""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return {
        "login": f"unique_login_{random_suffix}",
        "password": "unique_password",
        "firstName": "Unique"
    }
