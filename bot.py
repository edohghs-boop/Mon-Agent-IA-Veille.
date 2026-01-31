import os
import requests
import datetime

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def recuperer_info():
    # Ici, on simule une veille. On peut ajouter des actus plus tard !
    date = datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")
    return f"📢 *RAPPORT DE VEILLE*\n\n✅ Connexion établie le {date}.\n🚀 Statut : Ton IA est prête à recevoir des missions plus complexes !"

if __name__ == "__main__":
    infos = recuperer_info()
    envoyer_telegram(infos)
    
