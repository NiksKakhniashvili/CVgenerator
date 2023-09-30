import os

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import (
    UserRegistrationSerializer,
    CustomUserSerializer, )


class UserRegistrationAPIView(GenericAPIView):
    """
        An endpoint for the client to create a new User.

        This view allows unauthenticated users to create a new user account.

        Required Permissions:
        - None (AllowAny)

        Returns:
        - 201 Created: The new user account is successfully created, and authentication tokens are provided.
        - 400 Bad Request: Invalid data provided in the request.

    """

    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)


class UserAPIView(RetrieveAPIView):
    """
        Get user information.

        This view allows authenticated users to retrieve their own user information.

        Required Permissions:
        - User must be authenticated.

        Returns:
        - 200 OK: User information is successfully retrieved.
        - 401 Unauthorized: User is not authenticated.

    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


class GoogleLoginView(SocialLoginView):
    """
       Login with Google account.

       This view allows users to log in using their Google account credentials.

       Required Permissions:
       - None (Open to all)

       Returns:
       - 200 OK: Login is successful, and authentication tokens are provided.
       - 401 Unauthorized: Google authentication failed.
       - 400 Bad Request: Invalid data provided in the request.

    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.environ.get("CALLBACK_URL")
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            token = RefreshToken.for_user(self.user)
            response.data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return response
