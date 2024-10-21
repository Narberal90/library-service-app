from datetime import timedelta, date

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from rest_framework.exceptions import ValidationError


from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
)
from borrowings.signals import send_borrowing_notification


class BorrowingSerializerTests(TestCase):
    def setUp(self):
        post_save.disconnect(send_borrowing_notification, sender=Borrowing)
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
        """The test verifies that a book can be borrowed if
        copies are available"""

        borrowing = self.serializer.create(self.valid_data)
        self.book.refresh_from_db()

        self.assertEqual(self.book.inventory, 4)
        self.assertIsInstance(borrowing, Borrowing)

    def test_create_borrowing_with_no_available_inventory(self):
        """The test verifies that you cannot borrow
         a book if there are no copies"""

        self.book.inventory = 0
        self.book.save()

        with self.assertRaises(ValidationError) as context:
            self.serializer.create(self.valid_data)

        self.assertIn(
            "No available copies for borrowing.",
            str(context.exception)
        )

    def test_inventory_not_negative_after_borrowing(self):
        """The test checks that the inventory does not become negative"""

        self.book.inventory = 1
        self.book.save()

        borrowing = self.serializer.create(self.valid_data)
        self.book.refresh_from_db()

        self.assertEqual(self.book.inventory, 0)
        self.assertIsInstance(borrowing, Borrowing)
