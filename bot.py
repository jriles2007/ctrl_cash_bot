from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)

telegram_app = ApplicationBuilder().token(bot_token).build()

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Buy Plan - $10", callback_data='buy_plan')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a plan:", reply_markup=reply_markup)

# Button press
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Plan A"},
                "unit_amount": 1000,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"https://t.me/YourBotUsername?start=paid_{user_id}",
        cancel_url="https://t.me/YourBotUsername",
    )
    await query.message.reply_text(f"Pay here: {session.url}")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button))

# Flask webhook for Stripe
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    event = stripe.Webhook.construct_event(payload, sig_header, os.environ.get("STRIPE_ENDPOINT_SECRET"))

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # You could store to DB or notify user here
        print("Payment success:", session)

    return '', 200

# Telegram bot runner
@app.route("/")
def index():
    telegram_app.run_polling()
    return "Bot is running."

