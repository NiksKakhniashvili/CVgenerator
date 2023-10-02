from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UserRegistrationAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/users/register/"  # Replace with the actual URL of your registration endpoint
        self.valid_payload = {
            "email": "test@makingscience.com",
            "password": "test",
            "username": "test",
            "first_name": "test",
            "last_name": "test"
        }
        self.invalid_payload = {
            "email": "user@example.com",
            "password": "string",
            "username": "string",
            "first_name": "string",
            "last_name": "string"
        }

    def test_register_user_valid_payload(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_invalid_payload(self):
        response = self.client.post(self.url, self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.url = "/users/account/"

    def test_get_user_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

