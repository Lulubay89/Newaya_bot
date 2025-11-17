import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


# ---- HANDLER ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Bot działa poprawnie! 😊")


telegram_app.add_handler(CommandHandler("start", start))


# ---- HOME PAGE ----
@app.get("/")
def home():
    # Ustaw webhook przy pierwszym wejściu
    asyncio.run(set_webhook_once())
    return "Bot działa! Webhook ustawiony.", 200


# ---- ODBIÓR WEBHOOKA ----
@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)

    asyncio.run(telegram_app.process_update(update))
    return "OK", 200


# ---- FUNKCJA USTAWIAJĄCA WEBHOOK ----
webhook_set = False

async def set_webhook_once():
    global webhook_set
    if not webhook_set:
        await telegram_app.initialize()
        await telegram_app.start()
        await telegram_app.bot.set_webhook(WEBHOOK_URL)
        webhook_set = True
        print(">>> Webhook ustawiony!")
