from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserCreateSerializer, UserSerializer
from users.services import generate_invited_code, generate_password, send_code


class LoginUser(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def get_object(self):
        phone = self.request.data.get("phone")
        return User.objects.get(phone=phone)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(generate_password())
        while True:
            invite_code = generate_invited_code()
            if User.objects.filter(invite_code=invite_code).exists():
                continue
            else:
                user.invite_code = invite_code
                break
        send_code(user.phone)
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(generate_password())
        send_code(user.phone)
        user.save()

    def post(self, request, *args, **kwargs):
        if self.request.data.get("phone"):
            phone = self.request.data.get("phone")
            if User.objects.filter(phone=phone).exists():
                return self.update(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk).first()


class ActivationAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk).first()

    def perform_update(self, serializer):
        user = serializer.save()
        activate_code = self.request.data.get("activate_code")
        if activate_code:
            user.invited_by = User.objects.filter(invite_code=activate_code).first()
        user.save()
