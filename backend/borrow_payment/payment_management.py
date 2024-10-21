from datetime import date
from decimal import Decimal

import stripe
from django.urls import reverse
from django.conf import settings
from stripe.billing_portal import Session

from borrow_payment.models import Payment
from borrowings.models import Borrowing


stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = "http://localhost:8080"
FINE_MULTIPLIER = Decimal(1.5)


def manage_checkout_session(borrowing: Borrowing, fine: bool = False) -> Session:
    if fine:
        days = days_overdue(borrowing)
        money_to_pay = count_money_to_pay(borrowing, days)

        checkout_session = create_checkout_session(
            borrowing, money_to_pay * FINE_MULTIPLIER
        )
        borrowing.payment.type = (
            "Fine" if borrowing.payment.type == "Payment" else "Fine"
        )
        borrowing.payment.session_url = checkout_session.url
        borrowing.payment.session_id = checkout_session.id
        borrowing.payment.save()

    else:
        days = days_for_payment(borrowing)
        money_to_pay = count_money_to_pay(borrowing, days)

        checkout_session = create_checkout_session(borrowing, money_to_pay)
        Payment.objects.create(
            borrowing=borrowing,
            session_url=checkout_session.url,
            session_id=checkout_session.id,
            money_to_pay=money_to_pay,
        )

    return checkout_session


def create_checkout_session(borrowing: Borrowing, money_to_pay: Decimal) -> Session:
    return stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(money_to_pay * 100),
                    "product_data": {
                        "name": f"{borrowing.book.title} ({borrowing.book.authors})"
                    },
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        cancel_url=DOMAIN + reverse("borrowing:borrowing-list"),
        success_url=DOMAIN
        + reverse("success-payments")
        + f"?borrow={borrowing.id}"
        + "&session_id={CHECKOUT_SESSION_ID}",
    )


def count_money_to_pay(borrowing: Borrowing, days: int) -> Decimal:

    return round(days * borrowing.book.daily_fee, 2)


def days_overdue(borrowing: Borrowing):
    return abs(borrowing.borrow_date - date.today()).days


def days_for_payment(borrowing: Borrowing):
    return abs(borrowing.expected_return_date - borrowing.borrow_date).days