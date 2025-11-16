from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # ustawisz później w Render

app = Flask(__name__)

# Tworzymy aplikację Telegram
telegram_app = Application.builder().token(TOKEN).build()

# ---- HANDLERY ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Bot jest online i działa poprawnie! 😊")

telegram_app.add_handler(CommandHandler("start", start))


# ---- FLASK ROUTES ----
@app.get("/")
def home():
    return "Bot działa!"

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"


# ---- URUCHOMIENIE ----
if __name__ == "__main__":
    # 🔥 uruchamiamy serwer Flask (Render tego potrzebuje)
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )