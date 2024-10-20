from datetime import timedelta, date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)

BORROWING_URL = reverse("borrowing:borrowing-list")


def detail_url(borrowing_id):
    return reverse("borrowing:borrowing-detail", args=[borrowing_id])


def sample_borrowing(**params):
    user = get_user_model().objects.create_user(
        email="sample@user.com",
        password="sampletest"
    )
    book = Book.objects.create(
        title="Test",
        authors="Test",
        cover="Soft",
        inventory=5,
        daily_fee="15.00"
    )
    defaults = {
        "user": user,
        "book": book,
        "expected_return_date": "2024-12-24"
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_borrowing_list(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@email.test",
            password="password_test"
        )
        self.client.force_authenticate(self.user)
        self.borrowing_1 = Borrowing.objects.create(
            user=self.user,
            book=Book.objects.create(
                title="book 1",
                authors="Test 1",
                cover="Soft",
                inventory=2,
                daily_fee="5.00"
            ),
            expected_return_date="2025-01-24"
        )
        self.borrowing_2 = Borrowing.objects.create(
            user=self.user,
            book=Book.objects.create(
                title="book 2",
                authors="Test 2",
                cover="Hard",
                inventory=5,
                daily_fee="7.00"
            ),
            expected_return_date="2025-01-24"
        )

    def test_borrowing_list(self):
        """Test successful access to the list
        of borrowings for an authorized use"""
        borrowing = sample_borrowing()
        res = self.client.get(BORROWING_URL)
        borrowings = Borrowing.objects.filter(user=self.user)
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(borrowing, res.data)
        self.assertEqual(
            list(res.data["results"]),
            list(serializer.data)
        )

    def test_filter_borrowing_list_by_book_title(self):
        res = self.client.get(BORROWING_URL, {"book_title": "book 1"})
        serializer = BorrowingListSerializer(self.borrowing_1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"][0], serializer.data)

    def test_filter_borrowing_list_by_active_status_true(self):
        res = self.client.get(BORROWING_URL, {"is_active": True})

        borrowings = Borrowing.objects.filter(actual_return_date__isnull=True)
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_borrowing_list_by_active_status_false(self):
        borrowing = sample_borrowing(user=self.user)
        res = self.client.get(BORROWING_URL, {"is_active": False})

        borrowings = Borrowing.objects.filter(actual_return_date__isnull=False)
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_borrowing_detail(self):
        res = self.client.get(detail_url(self.borrowing_1.id))
        serializer = BorrowingDetailSerializer(self.borrowing_1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_expected_return_date_before_borrow_date(self):
        self.borrowing_1.expected_return_date = self.borrowing_1.borrow_date - timedelta(days=1)

        with self.assertRaises(ValidationError) as context:
            self.borrowing_1.full_clean()

        self.assertIn(
            "The expected return date must be after the borrow date.",
            str(context.exception)
        )

    def test_actual_return_date_before_borrow_date(self):
        self.borrowing_2.actual_return_date = self.borrowing_2.borrow_date - timedelta(days=1)

        with self.assertRaises(ValidationError) as context:
            self.borrowing_2.full_clean()

        self.assertIn("The actual return date cannot be before the borrow date.", str(context.exception))

    def test_valid_return_dates(self):
        self.borrowing_2.actual_return_date = self.borrowing_2.borrow_date + timedelta(days=5)
        try:
            self.borrowing_2.full_clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly!")


class BorrowingSerializerTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="serializer test",
            authors="serializer",
            cover="Hard",
            inventory=5,
            daily_fee="3.00"
        )
        self.user = get_user_model().objects.create_user(
            email="serializer@email.com",
            password="PassworD"
        )
        self.valid_data = {
            "book": self.book,
            "borrow_date": date.today(),
            "expected_return_date": date.today() + timedelta(days=10),
            "user": self.user
        }
        self.serializer = BorrowingSerializer()

    def test_create_borrowing_with_available_inventory(self):
        """The test verifies that a book can be borrowed if copies are available"""
        borrowing = self.serializer.create(self.valid_data)
        self.book.refresh_from_db()

        self.assertEqual(self.book.inventory, 4)
        self.assertIsInstance(borrowing, Borrowing)
