import telebot
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


#command uvicorn backend.telegram.main:app --host 127.0.0.1 --port 8002 --reload
#command uvicorn backend.telegram.main:app --host 127.0.0.1 --port 8002 --reload
