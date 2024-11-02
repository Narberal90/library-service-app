from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowings.models import Borrowing
from borrowings.tasks import send_borrowing_notification


@receiver(post_save, sender=Borrowing)
def borrowing_post_save(sender, instance, created, **kwargs):
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
        send_borrowing_notification.delay(payload)
