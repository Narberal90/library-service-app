# Generated by Django 5.1.2 on 2024-10-20 22:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("books", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrowing",
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
                ("borrow_date", models.DateField(auto_now_add=True)),
                ("expected_return_date", models.DateField()),
                ("actual_return_date", models.DateField(blank=True, null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="books.book"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Borrowing",
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(
                            ("expected_return_date__gt", models.F("borrow_date"))
                        ),
                        name="expected_return_after_borrow",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(
                            ("actual_return_date__gte", models.F("borrow_date")),
                            ("actual_return_date__isnull", True),
                            _connector="OR",
                        ),
                        name="actual_return_after_borrow",
                    ),
                    models.UniqueConstraint(
                        condition=models.Q(("actual_return_date__isnull", True)),
                        fields=("user", "book"),
                        name="unique_active_user_book",
                    ),
                ],
            },
        ),
    ]
