from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import UserRegistrationAPIView, UserAPIView, ProfileAPIView, GoogleLoginView

app_name = "users"

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user-registration"),
    path("login/", TokenObtainPairView.as_view(), name="user-login"),
    path("account/", UserAPIView.as_view(), ),
    path("profile/", ProfileAPIView.as_view(), name="user-profile"),
    path("login/google/", GoogleLoginView.as_view(), name='google-login'),
]
