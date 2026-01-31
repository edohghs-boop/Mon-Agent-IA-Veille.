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
            {
                "role": "system", 
                "content": "Tu es un expert en business et tech. Résume les news suivantes en une seule phrase percutante pour un entrepreneur africain. Sois direct et motivant."
            },
            {"role": "user", "content": texte}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return "L'IA est en train de réfléchir pour le prochain rapport. Profitez de ces news en attendant !"

def obtenir_donnees():
    # 1. Météo Zanguéra
    res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m").text.strip()
    
    # 2. Crypto (Bitcoin)
    res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
    prix_btc = f"{res_crypto['bitcoin']['usd']:,} $"

    # 3. Récupération des news
    url_rss = "https://news.google.com/rss/search?q=IA+tech+finance+Afrique&hl=fr"
    flux = feedparser.parse(url_rss)
    titres = [entry.title for entry in flux.entries[:3]]
    liens = [entry.link for entry in flux.entries[:3]]
    
    # 4. Analyse IA avec Groq
    analyse_ia = analyser_avec_groq(" | ".join(titres))

    return (
        f"🌟 *RAPPORT DÉCIDEUR (GROQ IA)*\n\n"
        f"📍 {res_meteo}\n"
        f"💰 BTC : {prix_btc}\n\n"
        f"🧠 *L'ANALYSE DE TON ASSISTANT :*\n_{analyse_ia}_\n\n"
        f"🔗 *ACTUALITÉS CLÉS :*\n"
        f"1️⃣ [{titres[0]}]({liens[0]})\n"
        f"2️⃣ [{titres[1]}]({liens[1]})"
    )

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    })

if __name__ == "__main__":
    rapport = obtenir_donnees()
    envoyer_telegram(rapport)
    
