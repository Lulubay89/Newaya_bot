import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

# Tworzymy Telegram application
telegram_app = Application.builder().token(TOKEN).build()


# ===== HANDLERY =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot działa! 🎉")


telegram_app.add_handler(CommandHandler("start", start))


# ===== FLASK ROUTES =====
@app.route("/", methods=["GET"])
def home():
    return "Bot działa — strona główna.", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)

    asyncio.get_event_loop().create_task(
        telegram_app.process_update(update)
    )

    return "OK", 200


# ===== START BOT =====
async def start_bot():
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())

    app.run(host="0.0.0.0", port=5000)
