import asyncio
from datetime import datetime
from datetime import timedelta

import httpx
from celery import shared_task
from django.utils import timezone

from borrow_payment.payment_management import manage_checkout_session
from borrowings.models import Borrowing

TELEGRAM_BOT_URL = "http://localhost:8000/send_message/"  # URL твоєї ендпоінт бота

@shared_task
def check_expiration():
    borrowings = Borrowing.objects.all()

    for borrowing in borrowings:
        if borrowing.expected_return_date < datetime.now().date():
            manage_checkout_session(borrowing, fine=True)


@shared_task
def check_expected_return_dates():
    tomorrow = timezone.now().date() + timedelta(days=1)
    borrowings_due_tomorrow = Borrowing.objects.filter(expected_return_date=tomorrow, actual_return_date__isnull=True)

    for borrowing in borrowings_due_tomorrow:
        asyncio.run(send_telegram_notification(borrowing.user.telegram_id, borrowing.book.title))


async def send_telegram_notification(telegram_id, book_title):
    message = f"Нагадування: ви повинні повернути книгу '{book_title}' завтра."

    data = {
        "telegram_id": telegram_id,
        "message": message
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TELEGRAM_BOT_URL, json=data)

        if response.status_code != 200:
            print(f"Помилка при надсиланні повідомлення для користувача {telegram_id}: {response.status_code}")
