import telebot
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


#command uvicorn telegram.main:app --host 127.0.0.1 --port 8000 --reload
