from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework import viewsets

from borrow_payment.models import Payment
from borrow_payment.serializers import PaymentListSerializer, PaymentSerializer
from borrowings.models import Borrowing


def success_session(request: HttpRequest):
    session_id = request.GET["session_id"]
    borrow_id = request.GET["borrow"]
    borrowing = Borrowing.objects.get(id=borrow_id)

    if borrowing.payment.session_id == session_id:
        borrowing.payment.status = "Paid"
        borrowing.payment.save()
        url = reverse("borrowing:borrowing-detail", kwargs={"pk": borrow_id})

        return redirect(url)

    return redirect(reverse("borrowings:borrowing-list"))


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all().select_related()

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        return PaymentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_staff:
            show_all = self.request.query_params.get("show_all", "None")

            if show_all == "true":
                return queryset

        return queryset.filter(borrowing__user=self.request.user)
