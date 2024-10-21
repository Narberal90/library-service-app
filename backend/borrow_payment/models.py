from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"

    class TypeChoice(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"

    status = models.CharField(
        max_length=32, choices=StatusChoice, default=StatusChoice.PENDING
    )
    type = models.CharField(
        max_length=32, choices=TypeChoice, default=TypeChoice.PAYMENT
    )
    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE, related_name="payment")
    session_url = models.URLField(max_length=500)
    session_id = models.CharField(max_length=252)
    money_to_pay = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return self.status
