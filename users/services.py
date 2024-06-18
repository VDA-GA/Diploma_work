import secrets
import string

from users.models import User


def generate_password():
    password = ''.join(secrets.choice(string.digits) for i in range(4))
    print(password)
    return password


def send_code(phone):
    user = User.objects.get(phone=phone)


def generate_invited_code():
    return secrets.token_hex(3)