from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import UserRegistrationAPIView, UserAPIView, GoogleLoginView

app_name = "users"

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user-registration"),
    path("login/", TokenObtainPairView.as_view(), name="user-login"),
    path("account/", UserAPIView.as_view(), ),
    path("login/google/", GoogleLoginView.as_view(), name='google-login'),
]
