from rest_framework import serializers

from borrow_payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "status", "type", "session_url", "money_to_pay"]
