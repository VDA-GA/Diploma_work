from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import UpdateCreateUser, UserRetrieveAPIView, UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("", UpdateCreateUser.as_view(permission_classes=[AllowAny]), name="login"),
    path("token/", TokenObtainPairView.as_view(permission_classes=[AllowAny]), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=[AllowAny]), name="token_refresh"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("user/<int:pk>/activate/", UserUpdateAPIView.as_view(), name="user_update"),
]
