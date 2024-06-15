from django.shortcuts import render
from rest_framework import viewsets, views, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from users.models import User
from users.serializers import UserCreateSerializer, MyTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.services import generate_password, send_code, generate_invited_code
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import mixins


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



