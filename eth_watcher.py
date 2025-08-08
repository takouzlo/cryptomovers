# eth_watcher.py
import requests
import time
import json
from datetime import datetime
import config
from watcher import send_telegram, send_tweet


def get_eth_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=eur")
        return r.json()['ethereum']['eur']
    except:
        return 3000  # valeur de secours

def watch_eth():
    eth_price = get_eth_price()
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address=0x0000000000000000000000000000000000000000&startblock=0&endblock=99999999&sort=desc&apikey={config.ETHERSCAN_API_KEY}"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        for tx in data['result'][:5]:
            value_wei = int(tx['value'])
            value_eth = value_wei / 1e18
            value_eur = value_eth * eth_price

            if value_eur > config.MIN_VALUE_EUR:
                link = f"https://etherscan.io/tx/{tx['hash']}"
                msg = f"🚨 {value_eur:,.0f}€ en ETH transférés !\n{link}"

                # Sauvegarde
                tx_data = {
                    "amount": f"{value_eth:.4f} ETH",
                    "value_eur": value_eur,
                    "currency": "ETH",
                    "link": link,
                    "explorer": "Etherscan",
                    "time": datetime.now().strftime("%H:%M")
                }

                # Ajoute à l'historique
                try:
                    with open('transactions.json', 'r') as f:
                        txs = json.load(f)
                except:
                    txs = []

                txs = [tx_data] + [t for t in txs if t != tx_data][:4]  # Garder 5 derniers

                with open('transactions.json', 'w') as f:
                    json.dump(txs, f)

                send_telegram(msg)
                send_tweet(msg)
    except Exception as e:
        print("Erreur ETH:", e)