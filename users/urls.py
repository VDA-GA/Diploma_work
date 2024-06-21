from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import ActivationAPIView, LoginUser, UserProfile, UserRetrieveAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("", LoginUser.as_view(), name="sms_code"),
    path("token/", TokenObtainPairView.as_view(permission_classes=[AllowAny]), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=[AllowAny]), name="token_refresh"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", UserRetrieveAPIView.as_view(), name="api_user_detail"),
    path("accounts/profile/", UserProfile.as_view(), name="profile"),
    path("activate/", ActivationAPIView.as_view(), name="code_activation"),
]
