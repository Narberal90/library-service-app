import telebot
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
