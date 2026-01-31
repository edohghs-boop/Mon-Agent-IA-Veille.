import os
import requests
import feedparser # Pour lire les actus

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": False}
    requests.post(url, json=payload)

def recuperer_actus():
    # On choisit un flux d'actualité Tech/Business (ici Google News Tech)
    url_rss = "https://news.google.com/rss/search?q=IA+tech+finance&hl=fr&gl=FR&ceid=FR:fr"
    flux = feedparser.parse(url_rss)
    
    actus = "📰 *DERNIÈRES INFOS TECH & BIZ*\n\n"
    # On prend les 3 premiers articles
    for entry in flux.entries[:3]:
        actus += f"🔹 [{entry.title}]({entry.link})\n\n"
    return actus

def obtenir_donnees():
    # Prix du Bitcoin
    try:
        res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        prix_btc = res_crypto.json()['bitcoin']['usd']
        crypto_txt = f"💰 *Bitcoin :* {prix_btc:,} $\n"
    except:
        crypto_txt = ""

    # Météo Zanguéra
    try:
        res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m")
        meteo_txt = f"🌤️ *Zanguéra :* {res_meteo.text.strip()}\n"
    except:
        meteo_txt = ""

    actus_txt = recuperer_actus()
    
    return f"🚀 *TON RAPPORT STRATÉGIQUE*\n\n{meteo_txt}{crypto_txt}\n{actus_txt}"

if __name__ == "__main__":
    rapport = obtenir_donnees()
    envoyer_telegram(rapport)
    
