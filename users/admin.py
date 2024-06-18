from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "phone", "invite_code", "activate_code", "invited_by"]
    list_filter = ["id", "phone"]
