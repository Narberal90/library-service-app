from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token_obtain_pair")
ME_URL = reverse("users:manage")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test public users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid credential is success"""
        payload = {
            "username": "userTest",
            "email": "user@test.com",
            "password": "password"
        }

        resp = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**resp.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", resp.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            "username": "userTest",
            "email": "user@test.com",
            "password": "password"
        }
        create_user(**payload)

        resp = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            "username": "testname",
            "email": "test@name.com",
            "password": "1g8"
        }
        resp = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            "username": "testname",
            "email": "test@name.com",
            "password": "test123",
        }
        create_user(**payload)

        resp = self.client.post(TOKEN_URL, payload)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
