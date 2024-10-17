from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverChoice(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=128, unique=True)
    authors = models.CharField(max_length=128, unique=True)
    cover = models.CharField(max_length=32, choices=CoverChoice, default=CoverChoice.HARD)
    inventory = models.IntegerField(validators=[MinValueValidator(-1)])
    daily_fee = models.DecimalField(decimal_places=2, max_digits=6, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.title} ({self.authors}), available: {self.inventory}"
