from datetime import datetime

from borrow_payment.payment_management import manage_checkout_session
from borrowings.models import Borrowing


def check_expiration():
    borrowings = Borrowing.objects.all()

    for borrowing in borrowings:
        if borrowing.expected_return_date < datetime.now().date():
            manage_checkout_session(borrowing, fine=True)

