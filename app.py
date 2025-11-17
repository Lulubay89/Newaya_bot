import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://newaya-bot.onrender.com/webhook

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


# --- Handlery ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot działa! 😊")


telegram_app.add_handler(CommandHandler("start", start))


# --- Flask routes ---
@app.get("/")
def home():
    return "Bot działa! ✔", 200


@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.create_task(telegram_app.process_update(update))
    return "OK", 200


# --- Start Telegram Webhook ---
@app.before_request
def init_bot():
    if not telegram_app.running:
        telegram_app.initialize()
        telegram_app.start()
        telegram_app.bot.set_webhook(WEBHOOK_URL)


