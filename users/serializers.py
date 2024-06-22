from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField(read_only=True)

    def get_invited_users(self, user):
        invited_users = User.objects.filter(invited_by=user)
        return [i.phone for i in invited_users]

    class Meta:
        model = User
        fields = ["id", "phone", "invite_code", "activate_code", "invited_users"]
        read_only_fields = ("id", "phone", "invite_code", "invited_users")

    def validate_activate_code(self, value):
        pk_user = self.context["request"].user.pk
        user = User.objects.filter(pk=pk_user).first()
        invite_user = User.objects.filter(invite_code=value).first()
        if user.activate_code:
            raise serializers.ValidationError("Код уже активирован!")
        elif User.objects.filter(invite_code=value).exists() is False:
            raise serializers.ValidationError("Пользователя с введенным кодом не найдено")
        elif user == invite_user:
            raise serializers.ValidationError("Код должен отличаться от Вашего")
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone"]

    def validate_phone(self, value):
        if value.isdigit() is False:
            raise serializers.ValidationError("Номер телефона неверный. Введите номер по образцу: 88888888888")
        return value
