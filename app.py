from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")

# Handlery Telegrama
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Bot jest online i działa poprawnie! 😊")

# Tworzenie aplikacji Telegrama
telegram_app = Application.builder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))

@app.get("/")
def home():
    return "Bot działa!"

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"

if __name__ == "__main__":
    # Render wymaga aplikacji webowej na porcie PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)