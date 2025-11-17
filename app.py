import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


# --- HANDLERY ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Bot działa! 😊")


telegram_app.add_handler(CommandHandler("start", start))


# --- WEBHOOK ENDPOINT ---
@app.post("/webhook")
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, telegram_app.bot)
        telegram_app.create_task(telegram_app.process_update(update))
        return "OK", 200
    except Exception as e:
        print("⚠️ WEBHOOK ERROR:", e)
        return "ERROR", 500


# --- ROOT ---
@app.get("/")
def root():
    return "Bot działa 🙂"


# --- START APP ---
if __name__ == "__main__":
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path="/webhook",
        webhook_url=WEBHOOK_URL,
    )