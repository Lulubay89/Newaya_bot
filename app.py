import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # np. https://twoja-domena.onrender.com/webhook

app = Flask(__name__)

# Tworzymy telegram application (bez .run_polling!)
telegram_app = Application.builder().token(TOKEN).build()


# ---- HANDLERY ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Bot jest online i działa poprawnie! 😊")


telegram_app.add_handler(CommandHandler("start", start))


# ---- ROUTES ----
@app.get("/")
def home():
    return "Bot działa! 🌍", 200


@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)

    update = Update.de_json(data, telegram_app.bot)

    # Tworzymy task w bieżącej pętli
    asyncio.get_event_loop().create_task(telegram_app.process_update(update))

    return "OK", 200


# Start dispatchera (WAŻNE!)
async def start_bot():
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)


# ---- MAIN ----
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())

    app.run(host="0.0.0.0", port=5000)