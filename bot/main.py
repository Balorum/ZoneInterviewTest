import logging
import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv

load_dotenv()


# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# BOT_TOKEN = "7533994208:AAF1Pl9NUoCkiplfJBBn32OR_8Q-N87fbAE"
BOT_TOKEN= os.getenv("BOT_TOKEN")
SERVER_URL = os.getenv("SERVER_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я AI-асистент для клієнтської підтримки. Як можу допомогти?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = requests.post("{SERVER_URL}/ask", json={"query": user_text})
    answer = response.json().get("answer", "Виникла помилка")
    zapier_dict = {
        "query": user_text,
        "response": answer,
        "user_id": update.message.from_user.id,
        "username": update.message.from_user.username,
        "first_name": update.message.from_user.first_name,
        "last_name": update.message.from_user.last_name,
        "timestamp": update.message.date.isoformat()
    }
    requests.post("{SERVER_URL}/webhook", json=zapier_dict)
    await update.message.reply_text(answer)


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Запуск бота (постійне опитування)
    application.run_polling()

if __name__ == '__main__':
    main()