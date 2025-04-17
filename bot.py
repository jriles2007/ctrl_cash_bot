from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import threading
import os

# Load tokens from environment
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Create Telegram bot app
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Received /start from {update.effective_user.username}")
    keyboard = [[
        InlineKeyboardButton("Buy Plan 💸", url="https://buy.stripe.com/test_4gw8zUahE3MdcgMdQQ")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Ctrl + Cash 👋\nChoose your plan below:", reply_markup=reply_markup)

# Add handler to bot
telegram_app.add_handler(CommandHandler("start", start))

# Flask web server for Render
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "✅ Bot is running."

# Optional: Stripe webhook route (not active yet)
@flask_app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    print("Received Stripe webhook:", payload)
    return "", 200

# Run Telegram bot in background thread
def run_bot():
    telegram_app.run_polling()

# Start both bot and Flask
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)

@app.route("/")
def index():
    return "Bot is running."
