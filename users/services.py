import secrets
import string
import time


def generate_password() -> str:
    """Случайно генерирует код"""
    password = "".join(secrets.choice(string.digits) for _ in range(4))
    return password


def send_code(phone, code) -> None:
    """Отправляет sms с кодом
    :param phone: номер телефона
    :param code: код"""
    time.sleep(4)
    print(code)


def generate_invited_code() -> str:
    """Генерирует случайный код приглашения
    :return код приглашения"""
    return secrets.token_hex(3)
