import os
import requests
import feedparser

def analyser_avec_groq(texte):
    api_key = os.getenv('GROQ_API_KEY')
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Tu es un expert business. Résume les news suivantes en une phrase percutante en français."},
            {"role": "user", "content": texte}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except:
        return "L'analyse IA est indisponible pour le moment."

def obtenir_donnees():
    # Météo et Crypto
    res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m").text.strip()
    res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
    prix_btc = f"{res_crypto['bitcoin']['usd']:,} $"

    # News
    url_rss = "https://news.google.com/rss/search?q=IA+tech+finance&hl=fr"
    flux = feedparser.parse(url_rss)
    titres = [entry.title for entry in flux.entries[:3]]
    
    # Analyse Groq
    analyse_ia = analyser_avec_groq(" | ".join(titres))

    return (
        f"🚀 *RAPPORT STRATÉGIQUE (IA GROQ)*\n\n"
        f"📍 {res_meteo}\n"
        f"💰 BTC: {prix_btc}\n\n"
        f"🧠 *L'ANALYSE DE L'IA :*\n{analyse_ia}\n\n"
        f"🔗 *SOURCE :* {titres[0]}"
    )

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                  json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    rapport = obtenir_donnees()
    envoyer_telegram(rapport)
    
