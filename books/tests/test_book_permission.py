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
        self.user = get_user_model().objects.create_superuser(
            email="TonyStark@gmail.com", password="TonyStarkHasTheHeart", is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.book_payload = {
            "title": "The Great Gatsby",
            "authors": "F. Scott Fitzgerald",
            "cover": "Hard",
            "inventory": 5,
            "daily_fee": "2.50"
        }
        self.book = Book.objects.create(**self.book_payload)

    def test_admin_create_book_success(self):
        create_payload = {
            "title": "The Great",
            "authors": "Scott",
            "cover": "Soft",
            "inventory": 7,
            "daily_fee": "23.00"
        }
        url = reverse("book:book-detail", args=[self.book.id])
        res = self.client.put(url, create_payload)

        self.book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_update_book_success(self):
        update_payload = {
            "title": "The Great Gatsby (Updated)",
            "authors": "F. Scott Fitzgerald",
            "cover": "Soft",
            "inventory": 10,
            "daily_fee": "3.00"
        }
        url = reverse("book:book-create", args=[self.book.id])
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

        def test_create_book_missing_fields(self):
        create_payload = {
            "authors": "Scott",
            "cover": "Soft",
        }
        url = reverse("book:book-list")
        res = self.client.post(url, create_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book_invalid_inventory(self):
        update_payload = {
            "title": "Invalid Book",
            "authors": "Author",
            "cover": "Soft",
            "inventory": -1,
            "daily_fee": "3.00"
        }
        url = reverse("book:book-detail", args=[self.book.id])
        res = self.client.put(url, update_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_book_success(self):
        url = reverse("book:book-detail", args=[self.book.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], self.book.title)
