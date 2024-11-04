from rest_framework import serializers
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from users.serializers import AuthTokenSerializer


class TestLoginSerializer(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@email.com",
            password="testpassword",
            is_active=True
        )

    @patch("users.serializers.authenticate")
    def test_successful_login(self, mock_authenticate):
        """Successful authentication test"""

        mock_authenticate.return_value = self.user

        serializer = AuthTokenSerializer(data={
            "email": "testuser@email.com",
            "password": "testpassword"
        })
        serializer.is_valid()

        self.assertEqual(serializer.validated_data["user"], self.user)

    @patch("users.serializers.authenticate")
    def test_disabled_user(self, mock_authenticate):
        """Test with disabled account"""

        self.user.is_active = False
        self.user.save()
        mock_authenticate.return_value = self.user

        serializer = AuthTokenSerializer(data={
            "email": "testuser@email.com",
            "password": "testpassword"
        })

        with self.assertRaises(serializers.ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("User account is disabled.", str(context.exception))

    @patch("users.serializers.authenticate")
    def test_invalid_credentials(self, mock_authenticate):
        """Test with invalid credentials"""

        mock_authenticate.return_value = None

        serializer = AuthTokenSerializer(data={
            "email": "testuser@email.com",
            "password": "wrongpassword"
        })

        with self.assertRaises(serializers.ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("Unable to log in with provided credentials.", str(context.exception))

    def test_missing_fields(self):
        """Test for missing fields"""

        serializer = AuthTokenSerializer(data={})

        with self.assertRaises(serializers.ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("This field is required.", str(context.exception))
        self.assertIn("This field is required.", str(context.exception))
