import requests
import random
import string
from config import BASE_URL


# Метод регистрации нового курьера возвращает список из логина и пароля
# Если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # Метод генерирует строку, состоящую только из букв нижнего регистра
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # Создаём список, чтобы метод мог его вернуть
    login_pass = []

    # Генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # Собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # Отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(f"{BASE_URL}/api/v1/courier", json=payload)

    # Если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # Возвращаем список
    return login_pass
