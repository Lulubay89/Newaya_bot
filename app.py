import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

# --- TELEGRAM APP ---
telegram_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("Cześć! Bot działa! 😊")

telegram_app.add_handler(CommandHandler("start", start))

# --- FLASK ---
app = Flask(__name__)

@app.get("/")
def index():
    return "Bot działa ✔️", 200

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)

    # uruchamiamy async update wewnątrz sync flask
    asyncio.get_event_loop().create_task(telegram_app.process_update(update))

    return "OK", 200

# --- URUCHOMIENIE ---
async def setup_webhook():
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(setup_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
