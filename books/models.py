from decimal import Decimal

from django.db import models
from rest_framework.exceptions import ValidationError


class Book(models.Model):
    class CoverChoice(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=128, unique=True)
    authors = models.CharField(max_length=128)
    cover = models.CharField(max_length=32, choices=CoverChoice, default=CoverChoice.HARD)
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return f"{self.title} ({self.authors}), available: {self.inventory}"

    @staticmethod
    def validate_non_negative_num(inventory: int, daily_fee: Decimal):
        for num_attr_value, num_attr_name in [
            (inventory, "inventory"),
            (daily_fee, "daily_fee"),
        ]:
            if not 0 >= num_attr_value:
                raise ValidationError(
                    f"{num_attr_name} "
                    "number value must be greater than equal 0. "
                    f"Actual: {num_attr_value} < 0"
                )

    def clean(self):
        Book.validate_non_negative_num(self.inventory, self.daily_fee)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Book, self).save(force_insert, force_update, using, update_fields)
