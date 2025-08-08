from flask import Flask, render_template
import json

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
    return render_template('premium.html')

if __name__ == '__main__':
    app.run(debug=False)