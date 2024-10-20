from decimal import Decimal

import stripe
from django.urls import reverse
from django.conf import settings

from borrow_payment.models import Payment
from borrowings.models import Borrowing


stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = "http://localhost:8000"
FINE_MULTIPLIER = Decimal(1.5)


def create_checkout_session(borrowing: Borrowing):
    money_to_pay = count_money_to_pay(borrowing)
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(money_to_pay * 100),
                    "product_data": {
                        "name": f"{borrowing.book.title} ({borrowing.book.title})"
                    }
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        cancel_url=DOMAIN + reverse("borrowing:borrowing-list"),
        success_url=DOMAIN + reverse("borrowing:borrowing-pay-return-borrowing", kwargs={"pk": borrowing.id}) + "?session_id={CHECKOUT_SESSION_ID}",
    )
    Payment.objects.create(
        borrowing=borrowing,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        money_to_pay=money_to_pay
    )
    breakpoint()
    return checkout_session


def count_money_to_pay(borrowing: Borrowing, fee: bool = False):
    days = (borrowing.expected_return_date - borrowing.borrow_date).days
    total = days * borrowing.book.daily_fee
    if fee:
        return round(total * FINE_MULTIPLIER, 2)
    return round(total, 2)
