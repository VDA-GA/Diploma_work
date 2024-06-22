from django.shortcuts import redirect
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status, views
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from users.models import User
from users.serializers import UserCreateSerializer, UserSerializer
from users.services import generate_invited_code, generate_password, send_code


class APICodeGetAPIView(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericAPIView):
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
        send_code(user.phone, invite_code)
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        password = generate_password()
        user.set_password(password)
        send_code(user.phone, password)
        user.save()

    def post(self, request, *args, **kwargs):
        if self.request.data.get("phone"):
            phone = self.request.data.get("phone")
            if User.objects.filter(phone=phone).exists():
                return self.update(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)


class CodeGetAPIView(APICodeGetAPIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def post(self, request, *args, **kwargs):
        if self.request.data.get("phone"):
            phone = self.request.data.get("phone")
            if User.objects.filter(phone=phone).exists():
                self.update(request, *args, **kwargs)
            else:
                self.create(request, *args, **kwargs)
        return redirect(reverse("users:login"))


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk).first()


class ActivationAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [SessionAuthentication, JWTTokenUserAuthentication]

    def get_object(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk).first()

    def perform_update(self, serializer):
        user = serializer.save()
        activate_code = self.request.data.get("activate_code")
        if activate_code:
            user.invited_by = User.objects.filter(invite_code=activate_code).first()
        user.save()


class UserProfile(views.APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    template_name = "users/profile.html"

    @swagger_auto_schema(
        operation_description="GET /accounts/profile/", responses={status.HTTP_200_OK: UserSerializer()}
    )
    def get(self, request):
        user = User.objects.filter(pk=request.user.pk)[0]
        return Response({"user": user})
