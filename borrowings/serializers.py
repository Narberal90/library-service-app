from rest_framework import serializers

from books.serializers import BookSerializer
from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        ]
        read_only_fields = ["id", "borrow_date", "actual_return_date"]

    def create(self, validated_data):
        book = validated_data["book"]
        print(f"Inventory before borrowing: {book.inventory}")
        print(book.inventory <= 0)
        if book.inventory <= 0:
            raise serializers.ValidationError("No available copies for borrowing.")
        book.inventory -= 1
        book.save()
        print("я тут")
        return super().create(validated_data)


class BorrowingListSerializer(serializers.ModelSerializer):
    book_title = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "book_title",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        ]

    def get_book_title(self, obj):
        return obj.book.title


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        ]


class ReturnBookSerializer(BorrowingSerializer):
    class Meta(BorrowingSerializer.Meta):
        model = Borrowing

        read_only_fields = [
            "id",
            "borrow_date",
            "actual_return_date",
            "expected_return_date",
        ]
