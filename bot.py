import os
import logging
import asyncio
from datetime import datetime
from telegram import Bot
from telegram.ext import Application, CommandHandler

# Load environment variables
BOT_TOKEN = os.getenv("8067216971:AAG_bk0_xlDyNTWoYJn0q8WIzSngqmuskZQ")
START_DATE = os.getenv("START_DATE", "2025-01-01")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot
bot = Bot(token=BOT_TOKEN)

async def send_countdown(context):
    """Sends a daily countdown message."""
    chat_id = os.getenv("1254738042")
    if not chat_id:
        logger.error("CHAT_ID is not set.")
        return
    
    start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
    today = datetime.today()
    remaining_days = (start_date - today).days
    
    message = f"⏳ Countdown: {remaining_days} days remaining!"
    await bot.send_message(chat_id=chat_id, text=message)

async def start(update, context):
    """Handles the /start command."""
    await update.message.reply_text("Hello! This bot sends a daily countdown.")

def main():
    """Starts the bot."""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    job_queue = application.job_queue
    job_queue.run_daily(send_countdown, time=datetime.time(9, 0))  # Sends at 9 AM daily
    
    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
