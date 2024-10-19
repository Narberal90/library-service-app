from rest_framework import serializers

from borrow_payment.models import Payment
from borrowings.serializers import BorrowingDetailSerializer

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay"
        ]

class PaymentDetailSerializer(PaymentSerializer):
    borrowing = BorrowingDetailSerializer(read_only=True)

