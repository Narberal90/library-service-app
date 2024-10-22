# Generated by Django 5.1.2 on 2024-10-21 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("borrowings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                (
                    "status",
                    models.CharField(
                        choices=[("Pending", "Pending"), ("Paid", "Paid")],
                        default="Pending",
                        max_length=32,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("Payment", "Payment"), ("Fine", "Fine")],
                        default="Payment",
                        max_length=32,
                    ),
                ),
                ("session_url", models.URLField()),
                ("session_id", models.CharField(max_length=124)),
                ("money_to_pay", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "borrowing",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment",
                        to="borrowings.borrowing",
                    ),
                ),
            ],
        ),
    ]