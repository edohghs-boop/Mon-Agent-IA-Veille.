import os
import requests
import feedparser

def analyser_avec_gemini(texte):
    api_key = os.getenv('GEMINI_API_KEY')
    # URL de l'API Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"Tu es un expert en business et tech. Résume ces actualités en une phrase percutante pour un entrepreneur : {texte}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "L'IA n'a pas pu analyser les news ce matin."

def obtenir_donnees():
    # 1. Crypto & Météo
    res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m").text.strip()
    res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
    prix_btc = res_crypto['bitcoin']['usd']

    # 2. News
    url_rss = "https://news.google.com/rss/search?q=IA+tech+finance&hl=fr"
    flux = feedparser.parse(url_rss)
    titres = [entry.title for entry in flux.entries[:3]]
    
    # 3. Analyse Gemini
    analyse_ia = analyser_avec_gemini(" | ".join(titres))

    return (
        f"🚀 *RAPPORT INTELLIGENT*\n\n"
        f"📍 {res_meteo}\n"
        f"💰 BTC: {prix_btc:,} $\n\n"
        f"📰 *L'essentiel :*\n{analyse_ia}\n\n"
        f"🔗 *Sources :*\n1. {titres[0][:50]}...\n2. {titres[1][:50]}..."
    )

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                  json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    rapport = obtenir_donnees()
    envoyer_telegram(rapport)
    
