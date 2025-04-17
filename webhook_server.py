from flask import Flask, request, jsonify
import stripe

app = Flask(__name__)

# Replace with your actual Stripe secret key
stripe.api_key = 'your_stripe_secret_key'
# Replace with your actual Stripe webhook secret
endpoint_secret = 'your_webhook_secret'

# Dictionary to store user subscription status
user_subscriptions = {}

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    
    # Verify the webhook signature
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': str(e)}), 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['client_reference_id']  # Assuming you set this when creating the checkout session
        # Update user subscription status in your dictionary
        user_subscriptions[user_id] = True  # Set to active
        
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(port=5000)
