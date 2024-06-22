import secrets
import string
import time


def generate_password():
    password = "".join(secrets.choice(string.digits) for _ in range(4))
    return password


def send_code(phone, code):
    time.sleep(4)
    print(code)



def generate_invited_code():
    return secrets.token_hex(3)
