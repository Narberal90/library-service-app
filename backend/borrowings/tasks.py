import logging

import httpx
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Borrowing

TELEGRAM_BOT_URL = "http://127.0.0.1:8002/send_message/"
logger = logging.getLogger(__name__)


@shared_task
def check_expected_return_dates():
    tomorrow = timezone.now().date() + timedelta(days=1)
    borrowings_due_tomorrow = Borrowing.objects.filter(
        expected_return_date=tomorrow,
        actual_return_date__isnull=True
    )

    for borrowing in borrowings_due_tomorrow:
        send_telegram_notification(borrowing.user.telegram_id, borrowing.book.title)


def send_telegram_notification(telegram_id, book_title):
    message = f"Reminder: You must return the book'{book_title}' tomorrow."

    payload = {
        "chat_id": telegram_id,
        "text": message
    }

    with httpx.Client() as client:
        response = client.post(TELEGRAM_BOT_URL, json=payload)

        if response.status_code != 200:
            print(
                f"Error sending message to user "
                f"{telegram_id}: {response.status_code}"
            )
