from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

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
