import asyncio
import os
from datetime import datetime
from datetime import timedelta

import httpx
from celery import shared_task

from borrow_payment.payment_management import manage_checkout_session
from borrowings.models import Borrowing


TELEGRAM_URL_SEND = os.getenv("TELEGRAM_URL_SEND")


@shared_task
def check_expiration():
    borrowings = Borrowing.objects.all()

    for borrowing in borrowings:
        if borrowing.expected_return_date < datetime.now().date():
            manage_checkout_session(borrowing, fine=True)


@shared_task
def check_expected_return_dates():
    tomorrow = datetime.now().date() + timedelta(days=1)

    borrowings_due_tomorrow = Borrowing.objects.filter(
        expected_return_date=tomorrow, actual_return_date__isnull=True
    )

    for borrowing in borrowings_due_tomorrow:
        send_telegram_notification(
            borrowing.user.telegram_id,
            borrowing.book.title
        )


def send_telegram_notification(telegram_id, book_title):
    message = f"Notification: you have to return book '{book_title}' tomorrow."

    payload = {"chat_id": telegram_id, "text": message}

    with httpx.Client() as client:
        response = client.post(TELEGRAM_URL_SEND, json=payload)

        if response.status_code != 200:
            print(
                "Error occurred during sending notification for user "
                f"{telegram_id}: {response.status_code}"
            )


@shared_task
def send_borrowing_notification(payload: dict, **kwargs):
    with httpx.Client() as client:

        response = client.post(TELEGRAM_URL_SEND, json=payload)
        if response.status_code != 200:
            print("Error sending message:", response.json())
