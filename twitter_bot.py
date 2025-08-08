# twitter_bot.py
import requests
import config

def send_tweet(text):
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {config.TWITTER_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"text": text}
    r = requests.post(url, json=data, headers=headers)
    if r.status_code == 201:
        print("✅ Tweet envoyé")
    else:
        print("❌ Erreur Twitter:", r.text)

# Pour envoyer une image + texte, il faudra uploader l'image d'abord (un peu plus complexe)