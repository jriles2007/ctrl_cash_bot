from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import threading
import os
import stripe

# Load tokens from environment
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_ENDPOINT_SECRET = os.getenv("STRIPE_ENDPOINT_SECRET")

# Configure Stripe
stripe.api_key = STRIPE_SECRET_KEY

# Create Telegram bot app
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Received /start from {update.effective_user.username}")
    keyboard = [
        [InlineKeyboardButton("Buy Plan 💸", url="https://buy.stripe.com/test_4gw8zUahE3MdcgMdQQ")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Ctrl + Cash 👋\nChoose your plan below:", reply_markup=reply_markup)

# Add handler to bot
telegram_app.add_handler(CommandHandler("start", start))

# Flask web server for Render
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "✅ Bot is running."

# Stripe webhook route
@flask_app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': str(e)}), 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # Contains a stripe.PaymentIntent
        print(f"PaymentIntent was successful! {payment_intent}")
        # Here you can send a message to the user or update your database

    return jsonify({'status': 'success'}), 200

# Run Telegram bot in background thread
def run_bot():
    telegram_app.run_polling()

# Start both bot and Flask
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)
