import logging
import os

import requests

from telegram.bot import bot

logger = logging.getLogger(__name__)

API_URL = os.getenv("API_URL")


# Bot handler
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "👋 Hello! Please enter your email so we can contact you.")


@bot.message_handler(func=lambda message: True)
def handle_email(message):
    email = message.text
    telegram_id = message.from_user.id
    logger.info(f"Received email: {email}, Telegram ID: {telegram_id}")
    response = requests.post(API_URL, json={
        "email": email,
        "telegram_id": telegram_id
    })

    if response.status_code == 200:
        bot.reply_to(message, "Thank you, now we can notify you of updates")
    else:
        bot.reply_to(message, "It looks like you entered an incorrect email address,"
                              " or you haven't registered on the site yet.")
