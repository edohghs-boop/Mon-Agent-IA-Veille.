import os
import requests

# Récupération sécurisée des secrets que tu as enregistrés
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def envoyer_rapport():
    # C'est ici que ton robot s'exprime
    message = "🚀 ALERTE CLOUD : Ton bot GitHub Actions est opérationnel ! Il vient de s'exécuter tout seul."
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

if __name__ == "__main__":
    envoyer_rapport()
  
