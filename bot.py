import os
import requests

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        print("Erreur : Les clés Telegram sont absentes !")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Message envoyé avec succès !")
        else:
            print(f"❌ Erreur lors de l'envoi : {response.text}")
    except Exception as e:
        print(f"⚠️ Erreur de connexion : {e}")

if __name__ == "__main__":
    envoyer_telegram("🚀 Coucou ! Ton robot est enfin opérationnel et connecté à GitHub !")
  
