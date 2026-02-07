import os
from telegram.ext import Application
from dotenv import load_dotenv
from app.bot.handlers import register_handlers

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def run_bot():
    print("🚀 Starting Telegram bot...")

    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

    app = Application.builder().token(BOT_TOKEN).build()
    register_handlers(app)

    print("✅ Bot is polling")
    app.run_polling()

if __name__ == "__main__":
    run_bot()
