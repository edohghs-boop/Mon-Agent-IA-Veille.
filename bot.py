import os
import requests

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def obtenir_donnees():
    # 1. Le prix du Bitcoin en DOLLARS
    try:
        res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        prix_btc = res_crypto.json()['bitcoin']['usd']
        crypto_txt = f"💰 *Bitcoin :* {prix_btc:,} $"
    except:
        crypto_txt = "💰 *Bitcoin :* Indisponible"

    # 2. La Météo précise pour Zanguéra en Celsius
    try:
        # Le ?m à la fin force l'affichage en Celsius (°C)
        res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m")
        meteo_txt = f"🌤️ *Météo :* {res_meteo.text.strip()}"
    except:
        meteo_txt = "🌤️ *Météo :* Indisponible à Zanguéra"

    # 3. Motivation
    motivation = "✨ *Motivation :* Chaque petit pas te rapproche de ton grand objectif. Ne t'arrête jamais !"

    return f"🚀 *TON ASSISTANT IA*\n\n{meteo_txt}\n{crypto_txt}\n\n{motivation}\n\n☀️ Bonne journée !"

if __name__ == "__main__":
    rapport = obtenir_donnees()
    envoyer_telegram(rapport)
    
