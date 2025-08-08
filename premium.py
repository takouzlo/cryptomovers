# premium.py
from flask import Flask, request
import stripe
import config

app = Flask(__name__)
stripe.api_key = config.STRIPE_API_KEY

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Abonnement CryptoMovers Pro',
                    'description': 'Alertes SMS, filtres, export CSV',
                },
                'unit_amount': 500,  # 5.00 €
            },
            'quantity': 1,
        }],
        mode='subscription',  # ou 'payment' pour achat unique
        success_url='https://cryptomovers.com/success',
        cancel_url='https://cryptomovers.com/cancel',
    )
    return {'id': session.id}