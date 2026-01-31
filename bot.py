import os
import requests

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def obtenir_donnees():
    # 1. On récupère le prix du Bitcoin
    try:
        res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur")
        prix_btc = res_crypto.json()['bitcoin']['eur']
        crypto_txt = f"💰 *Bitcoin :* {prix_btc} €"
    except:
        crypto_txt = "💰 *Bitcoin :* Indisponible pour le moment"

    # 2. Une petite dose de motivation
    motivation = "✨ *Motivation :* Le succès n'est pas final, l'échec n'est pas fatal : c'est le courage de continuer qui compte."

    return f"🚀 *TON RAPPORT MATINAL*\n\n{crypto_txt}\n\n{motivation}\n\n☀️ Passe une excellente journée !"

if __name__ == "__main__":
    rapport = obtenir_donnees()
    envoyer_telegram(rapport)
    
