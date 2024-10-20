# Generated by Django 5.1.2 on 2024-10-19 12:09

import books.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128, unique=True)),
                ("authors", models.CharField(max_length=128)),
                (
                    "cover",
                    models.CharField(
                        choices=[("Hard", "Hard"), ("Soft", "Soft")],
                        default="Hard",
                        max_length=32,
                    ),
                ),
                ("inventory", models.IntegerField()),
                ("daily_fee", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "image",
                    models.ImageField(
                        null=True, upload_to=books.models.book_image_path
                    ),
                ),
            ],
        ),
    ]