import os
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route
from starlette.requests import Request


from telegram import Update
from telegram.ext import Application, CommandHandler


TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL") # https://your-domain.onrender.com/webhook


# --- Telegram application (PTB 21.x)
telegram_app = Application.builder().token(TOKEN).build()




async def start(update, context):
await update.message.reply_text("Cześć! Bot działa! 😊")




telegram_app.add_handler(CommandHandler("start", start))




# --- Web handlers (Starlette)
async def homepage(request: Request):
return PlainTextResponse("Bot działa ✔")




async def webhook(request: Request):
data = await request.json()
update = Update.de_json(data, telegram_app.bot)
await telegram_app.process_update(update)
return JSONResponse({"status": "ok"})




routes = [
Route("/", endpoint=homepage, methods=["GET"]),
Route("/webhook", endpoint=webhook, methods=["POST"]),
]


app = Starlette(routes=routes)




# --- Set up bot on startup
@app.on_event("startup")
async def startup_event():
# initialize & start the telegram application and set webhook
await telegram_app.initialize()
await telegram_app.start()
if WEBHOOK_URL:
await telegram_app.bot.set_webhook(WEBHOOK_URL)
print("Webhook ustawiony:", WEBHOOK_URL)
else:
print("UWAGA: WEBHOOK_URL nie ustawiony w env vars")
