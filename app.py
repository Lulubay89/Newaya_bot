import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.requests import Request

from telegram import Update
from telegram.ext import Application, CommandHandler


TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://newaya-bot.onrender.com/webhook


# --- Telegram Application ---
telegram_app = Application.builder().token(TOKEN).build()


async def start(update, context):
    await update.message.reply_text("Bot działa! 🌿")


telegram_app.add_handler(CommandHandler("start", start))


# --- Handlers for Web Server ---
async def homepage(request):
    return PlainTextResponse("Bot działa ✔")


async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return JSONResponse({"status": "ok"})


routes = [
    Route("/", homepage),
    Route("/webhook", webhook, methods=["POST"]),
]


app = Starlette(routes=routes)


# --- On startup: set webhook ---
@app.on_event("startup")
async def start_bot():
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
