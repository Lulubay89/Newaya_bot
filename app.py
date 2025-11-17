import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

# Telegram application
telegram_app = Application.builder().token(TOKEN).build()


# ---- Handlery ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Bot jest online i działa poprawnie! 😊")


telegram_app.add_handler(CommandHandler("start", start))


# ---- Flask routes ----
@app.get("/")
def home():
    return "Bot działa! 🌍", 200


@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)

    asyncio.get_event_loop().create_task(telegram_app.process_update(update))
    return "OK", 200


# ---- Start Telegram bot on server startup ----
@app.before_first_request
def activate_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())


async def start_bot():
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    print("BOT POPRAWNIE URUCHOMIONY ✔")


# Flask start (render+gunicorn)
def start():
    app.run(host="0.0.0.0", port=5000)
