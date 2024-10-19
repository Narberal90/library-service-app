from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book

BOOK_URL = reverse("book:book-list")


class TestBookAdmin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="TonyStark@gmail.com", password="TonyStarkHasTheHeart", is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.book_payload = {
            "title": "The Great Gatsby",
            "authors": "F. Scott Fitzgerald",
            "cover": "Hard",
            "inventory": 5,
            "daily_fee": "2.50",
        }
        self.book = Book.objects.create(**self.book_payload)

    def test_admin_update_book_success(self):
        update_payload = {
            "title": "The Great Gatsby (Updated)",
            "authors": "F. Scott Fitzgerald",
            "cover": "Soft",
            "inventory": 10,
            "daily_fee": "3.00",
        }
        url = reverse("book:book-detail", args=[self.book.id])
        res = self.client.put(url, update_payload)

        self.book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book.title, update_payload["title"])
        self.assertEqual(self.book.cover, update_payload["cover"])

    def test_admin_delete_book_success(self):
        url = reverse("book:book-detail", args=[self.book.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())


class TestBookNonAdmin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.non_admin_user = get_user_model().objects.create_user(
            email="test@gmail.com", password="test"
        )
        self.client.force_authenticate(self.non_admin_user)

        self.payload = {
            "title": "test",
            "authors": "test",
            "cover": "Hard",
            "inventory": 5,
            "daily_fee": "2.50",
        }

    def test_non_admin_user_create_book_forbidden(self):
        res = self.client.post(BOOK_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
