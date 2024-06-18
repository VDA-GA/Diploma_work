from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, views, status, generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from users.models import User
from users.serializers import UserCreateSerializer, UserSerializer

from users.services import generate_password, send_code, generate_invited_code


class UpdateCreateUser(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def get_object(self):
        phone = self.request.data.get("phone")
        return User.objects.get(phone=phone)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(generate_password())
        user.invite_code = generate_invited_code()
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


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        user = serializer.save()
        activate_code = self.request.data.get("activate_code")
        if activate_code:
            user.invited_by = User.objects.filter(invite_code=activate_code).first()
        user.save()




