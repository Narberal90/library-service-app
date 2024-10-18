# Generated by Django 5.1.2 on 2024-10-18 16:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0003_alter_book_authors"),
        ("borrowings", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="borrowing",
            name="unique_user_book",
        ),
        migrations.RemoveConstraint(
            model_name="borrowing",
            name="actual_return_before_expected_return",
        ),
        migrations.AddConstraint(
            model_name="borrowing",
            constraint=models.UniqueConstraint(
                condition=models.Q(("actual_return_date__isnull", True)),
                fields=("user", "book"),
                name="unique_active_user_book",
            ),
        ),
    ]