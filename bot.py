from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

TOKEN = os.environ.get("TOKEN")

async def start(update, context):
    await update.message.reply_text("Selam! Ben senin botun!")

async def mesaj(update, context):
    await update.message.reply_text(f"Dedin: {update.message.text}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, mesaj))
app.run_polling
