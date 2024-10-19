from rest_framework import serializers

from borrow_payment.models import Payment
# from borrowings.serializers import BorrowingRetrieveSerializer

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

# class PaymentRetrieveSerializer(PaymentSerializer):
    # borrowing = BorrowingRetrieveSerializer(read_only=True)

