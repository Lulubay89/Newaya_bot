from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

# Pobranie tokena z Render Environment Variables
TOKEN = os.getenv("BOT_TOKEN")

# Tworzymy Flask
app = Flask(__name__)

# Tworzymy Telegram Application
telegram_app = Application.builder().token(TOKEN).build()

# Komenda /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Bot jest online i działa poprawnie! 😊")

# Dodajemy handler
telegram_app.add_handler(CommandHandler("start", start))

# Endpoint testowy
@app.route("/", methods=["GET"])
def home():
    return "Bot działa! 🌍", 200

# Główny webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)

    # Wrzucamy update do kolejki asynchronicznego przetwarzania
    asyncio.get_event_loop().create_task(telegram_app.process_update(update))

    return "OK", 200


# Uruchamianie webhookowego worker’a (Render zawoła to automatycznie)
if __name__ == "__main__":
    print("Startuję lokalnie (Render użyje gunicorn).")
    app.run(host="0.0.0.0", port=5000)