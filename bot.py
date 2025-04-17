from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import stripe
import os
import threading

# 🔐 Environment Variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# 🧠 Telegram Setup
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# 💬 Telegram Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Buy Plan", url="https://buy.stripe.com/test_1234567890abcdef")]  # Replace with real link
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Ctrl + Cash 💸", reply_markup=reply_markup)

telegram_app.add_handler(CommandHandler("start", start))

# 🖥️ Flask App for Render
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "✅ Bot is running."

@flask_app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    print("Received Stripe webhook:", payload)
    return "", 200

# ▶️ Run Telegram Bot in Background
def run_bot():
    telegram_app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)

@app.route("/")
def index():
    return "Bot is running."
