from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(expected_return_date__gt=models.F("borrow_date")),
                name="expected_return_after_borrow",
            ),
            models.CheckConstraint(
                check=models.Q(actual_return_date__gte=models.F("borrow_date"))
                | models.Q(actual_return_date__isnull=True),
                name="actual_return_after_borrow",
            ),
            models.UniqueConstraint(
                fields=["user", "book"],
                condition=models.Q(actual_return_date__isnull=True),
                name="unique_active_user_book",
            ),
        ]
        verbose_name = "Borrowing"

    def clean(self):
        if self.expected_return_date and self.expected_return_date <= self.borrow_date:
            raise ValidationError(
                "The expected return date must be after the borrow date."
            )
        if self.actual_return_date:
            if self.actual_return_date < self.borrow_date:
                raise ValidationError(
                    "The actual return date cannot be before the borrow date."
                )

    def return_book(self):
        if self.actual_return_date:
            raise ValidationError("This borrowing has already been returned.")

        if self.payment.status != "Paid":
            raise ValidationError("This borrowing has to be paid first.")

        self.actual_return_date = date.today()
        self.book.inventory += 1
        self.book.save()
        self.save()

    def pay(self):
        self.payment.status = "Paid"
        self.payment.save()
