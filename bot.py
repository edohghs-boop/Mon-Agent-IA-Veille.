import os
import requests
import feedparser

def analyser_avec_groq(texte):
    api_key = os.getenv('GROQ_API_KEY')
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": f"Résume en une phrase motivante : {texte}"}]
    }
    
    try:
        # Timeout réduit à 5 secondes pour ne pas attendre indéfiniment
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        return response.json()['choices'][0]['message']['content']
    except:
        return "L'IA est occupée, mais reste focus sur tes objectifs !"

def obtenir_donnees():
    # On utilise des timeouts partout pour la rapidité
    try:
        res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m", timeout=3).text.strip()
    except:
        res_meteo = "Météo Zanguéra"

    try:
        res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=3).json()
        prix_btc = f"{res_crypto['bitcoin']['usd']:,} $"
    except:
        prix_btc = "Indisponible"

    # News
    flux = feedparser.parse("https://news.google.com/rss/search?q=IA+tech+Afrique&hl=fr")
    titres = [entry.title for entry in flux.entries[:2]]
    liens = [entry.link for entry in flux.entries[:2]]
    
    analyse = analyser_avec_groq(" | ".join(titres))

    return (
        f"🚀 *POINT RAPIDE*\n\n"
        f"📍 {res_meteo}\n"
        f"💰 BTC : {prix_btc}\n\n"
        f"🧠 *CONSEIL IA :*\n_{analyse}_\n\n"
        f"🔗 *TOP NEWS :*\n1️⃣ [{titres[0]}]({liens[0]})"
    )

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                  json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True})

if __name__ == "__main__":
    envoyer_telegram(obtenir_donnees())
    
