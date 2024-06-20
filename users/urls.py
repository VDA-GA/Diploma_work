from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import ActivationAPIView, LoginUser, UserRetrieveAPIView, UserProfile

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(permission_classes=[AllowAny]), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=[AllowAny]), name="token_refresh"),
    path("api/user/", UserRetrieveAPIView.as_view(), name="api_user_detail"),
    path("user/", UserProfile.as_view(), name="user_detail"),
    path("activate/", ActivationAPIView.as_view(), name="code_activation"),
]
