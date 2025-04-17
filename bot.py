from config import API_TOKEN
import telebot
from telebot import types
import stripe

bot = telebot.TeleBot(token=API_TOKEN)

# Replace with your actual Stripe secret key
stripe.api_key = 'your_stripe_secret_key'

# Plans and their corresponding Stripe payment links
plans = {
    "Basic Plan 💳": "price_yourpriceid",  # Use your actual price ID
}

# Dictionary to store user subscription status
user_subscriptions = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = f"User {message.from_user.first_name}, welcome to the bot! Use /plans to see available plans."
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['plans'])
def show_plans(message):
    plans_text = (
        "*Ctrl + Money premium plan:*\n"
        "- Reselling\n"
        "- Fakes reselling\n"
        "- Sports Betting\n"
        "- Sports Arbitrage"
    )
    bot.send_message(message.chat.id, plans_text, parse_mode='Markdown')

    # Create inline keyboard
    markup = types.InlineKeyboardMarkup()

    for plan_name, plan_id in plans.items():
        button = types.InlineKeyboardButton(plan_name, url=create_checkout_session(message.from_user.id))
        markup.add(button)

    # Send the message with the inline keyboard
    bot.send_message(message.chat.id, "Select a plan:", reply_markup=markup)

def create_checkout_session(user_id):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': plans["Basic Plan 💳"],  # Use your actual price ID
                'quantity': 1,
            },
        ],
        mode='subscription',
        success_url='https://yourdomain.com/success',  # Redirect URL for successful payment
        cancel_url='https://yourdomain.com/cancel',    # Redirect URL for canceled payment
        client_reference_id=user_id  # Pass the user ID here
    )
    return session.url

@bot.message_handler(commands=['cancel'])
def cancel_subscription(message):
    user_id = message.from_user.id
    
    if user_id in user_subscriptions and user_subscriptions[user_id]:
        user_subscriptions[user_id] = False  # Update subscription status
        bot.send_message(message.chat.id, "Your subscription has been canceled.")
    else:
        bot.send_message(message.chat.id, "You do not have an active subscription to cancel.")

bot.polling()
