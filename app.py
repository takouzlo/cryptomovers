from flask import Flask, render_template
import json

import config

app = Flask(__name__)

# Lecture des dernières transactions depuis un fichier
@app.route('/')
def home():
    try:
        with open('transactions.json', 'r') as f:
            txs = json.load(f)
    except:
        txs = []
    return render_template('index.html', transactions=txs)

@app.route('/premium')
def premium():
    return render_template('premium.html', pub_key=config.STRIPE_PUBLIC_KEY)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)