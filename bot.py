import os
import requests
import feedparser

def analyser_avec_groq(texte):
    # Le robot va chercher la clé que tu as enregistrée dans les secrets GitHub
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
                "content": "Tu es un expert en business. Résume ces news en une seule phrase courte et motivante pour un entrepreneur au Togo."
            },
            {"role": "user", "content": texte}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except:
        return "L'IA prépare son analyse pour le prochain rapport."

def obtenir_donnees():
    # Météo Zanguéra
    res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m").text.strip()
    
    # Crypto
    res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
    prix_btc = f"{res_crypto['bitcoin']['usd']:,} $"

    # News (IA et Tech en Afrique)
    url_rss = "https://news.google.com/rss/search?q=IA+tech+finance+Afrique&hl=fr"
    flux = feedparser.parse(url_rss)
    titres = [entry.title for entry in flux.entries[:2]]
    liens = [entry.link for entry in flux.entries[:2]]
    
    # Analyse avec ta clé Groq
    analyse_ia = analyser_avec_groq(" | ".join(titres))

    return (
        f"🌟 *RAPPORT STRATÉGIQUE*\n\n"
        f"📍 {res_meteo}\n"
        f"💰 BTC : {prix_btc}\n\n"
        f"🧠 *CONSEIL DE TON IA :*\n_{analyse_ia}_\n\n"
        f"🔗 *ACTUALITÉS :*\n1️⃣ [{titres[0]}]({liens[0]})\n2️⃣ [{titres[1]}]({liens[1]})"
    )

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                  json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True})

if __name__ == "__main__":
    envoyer_telegram(obtenir_donnees())
    
