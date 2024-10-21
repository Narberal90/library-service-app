from rest_framework import serializers
from rest_framework.decorators import action

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "authors", "cover", "inventory", "daily_fee"]

    def validate(self, attrs):
        Book.validate_non_negative_num(
            inventory=attrs["inventory"], daily_fee=attrs["daily_fee"]
        )
        return attrs


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "image"]


class BookRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "authors", "cover", "inventory", "daily_fee", "image"]
