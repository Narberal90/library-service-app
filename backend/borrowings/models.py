from django.db import models
from django.db.models import UniqueConstraint

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "book",], name="unique_user_book")
        ]
        verbose_name = "Borrowing"
