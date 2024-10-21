import os

import httpx
from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowings.models import Borrowing


@receiver(post_save, sender=Borrowing)
def send_borrowing_notification(sender, instance, created, **kwargs):
    if created:
        telegram_id = instance.user.telegram_id
        book_title = instance.book.title
        message = (
            f"Ready to dive into a new adventure? "
            f"You've successfully taken the book: {book_title}."
        )

        payload = {
            "chat_id": telegram_id,
            "text": message
        }

        url = os.getenv("TELEGRAM_URL_SEND") + "/send_message/"
        with httpx.Client() as client:

            response = client.post(url, json=payload)
            if response.status_code != 200:
                print("Error sending message:", response.json())
