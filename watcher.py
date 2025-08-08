import requests
import time
import json
from datetime import datetime

import config


def send_telegram(text):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": config.TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)


def send_tweet(text):
    # À implémenter avec requests.post vers Twitter API
    print("Tweet:", text)


while True:
    try:
        r = requests.get(config.BLOCKCHAIN_API_URL, timeout=10)
        data = r.json()
        for tx in data['txs']:
            value_satoshi = sum(out['value'] for out in tx['out'])
            value_btc = value_satoshi / 1e8
            value_eur = value_btc * 40000  # À remplacer par API prix

            if value_eur > config.MIN_VALUE_EUR:
                link = f"https://blockchain.com/btc/tx/{tx['hash']}"
                msg = f"🚨 {value_eur:,.0f}€ en BTC transférés !\n{link}"

                # Sauvegarde
                tx_data = {
                    "amount": f"{value_btc:.4f} BTC",
                    "value_eur": value_eur,
                    "currency": "BTC",
                    "link": link,
                    "explorer": "Blockchain.com",
                    "time": datetime.now().strftime("%H:%M")
                }
                with open('transactions.json', 'w') as f:
                    json.dump([tx_data], f)

                send_telegram(msg)
                send_tweet(msg)
    except Exception as e:
        print("Erreur BTC:", e)
    time.sleep(60)