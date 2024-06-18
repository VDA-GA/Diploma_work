from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=35, unique=True, verbose_name="номер телефона")
    invite_code = models.CharField(max_length=6, verbose_name="инвайт код")
    activate_code = models.CharField(max_length=6, **NULLABLE, verbose_name="инвайт код пригласившего пользователя")
    invited_by = models.ForeignKey(
        "self", on_delete=models.RESTRICT, **NULLABLE, verbose_name="пригласивший пользователь"
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
