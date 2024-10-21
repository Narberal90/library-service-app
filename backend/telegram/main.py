import logging
import os
import threading

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from telegram.bot import bot
import telegram.handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()
token = os.getenv("TELEGRAM_BOT_TOKEN")


def start_bot_polling():
    bot.polling(none_stop=True)


@app.on_event("startup")
async def startup_event():
    threading.Thread(target=start_bot_polling, daemon=True).start()


class SendMessagePayload(BaseModel):
    chat_id: int
    text: str


@app.post("/send_message/")
async def send_message(payload: SendMessagePayload):
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = {
        "chat_id": payload.chat_id,
        "text": payload.text
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)

    if response.status_code != 200:
        return {"error": "Failed to send message", "details": response.json()}

    return {"status": response.status_code, "response": response.json()}
