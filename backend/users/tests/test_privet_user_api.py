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


class PrivetUSerApiTests(TestCase):
    """TEST API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email="test@admin.com",
            password="adminpass"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "id": self.user.id,
                "email": self.user.email,
                "is_staff": self.user.is_staff,
            },
        )

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        resp = self.client.post(ME_URL, {})

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {"username": "new_user", "password": "goodpass"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
