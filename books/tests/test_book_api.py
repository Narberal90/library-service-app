from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book
from books.serializers import BookSerializer, BookRetrieveSerializer

BOOK_URL = reverse("book:book-list")


def sample_book(**params):
    defaults = {
        "title": "TestBook",
        "authors": "Author Test",
        "cover": "Hard",
        "inventory": 3,
        "daily_fee": "10.10"
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def detail_url(book_id):
    return reverse("book:book-detail", args=[book_id])


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@email.com",
            password="password"
        )
        self.client.force_authenticate(self.user)

    def test_book_list(self):
        sample_book()
        sample_book(
            title="Test",
            authors="Test",
            cover="Soft",
            inventory=5,
            daily_fee="15.00"
        )
        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_book_detail(self):
        book = sample_book()
        res = self.client.get(detail_url(book.id))
        serializer = BookRetrieveSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_forbidden(self):
        payload = {
            "title": "Testing",
            "authors": "Some Test",
            "cover": "Hard",
            "inventory": 1,
            "daily_fee": "2.00"
        }
        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_forbidden(self):
        book = sample_book()
        payload = {
            "title": "Testing",
            "authors": "Some Test",
            "cover": "Hard",
            "inventory": 1,
            "daily_fee": "2.00"
        }

        res = self.client.put(detail_url(book.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_forbidden(self):
        book = sample_book()
        res = self.client.delete(detail_url(book.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
