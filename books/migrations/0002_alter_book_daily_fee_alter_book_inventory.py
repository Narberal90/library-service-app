# Generated by Django 5.1.2 on 2024-10-18 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="daily_fee",
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name="book",
            name="inventory",
            field=models.IntegerField(),
        ),
    ]
