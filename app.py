from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()

@app.get("/")
def home():
    return "Bot działa! 😊"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Bot jest online i działa poprawnie! 😊")

telegram_app.add_handler(CommandHandler("start", start))

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"

if __name__ == "__main__":
    telegram_app.run_polling()