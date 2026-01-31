import os
import requests
import feedparser

def analyser_avec_gpt(texte):
    api_key = os.getenv('OPENAI_API_KEY')
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # On utilise gpt-4o-mini : c'est le moins cher et le plus rapide
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Tu es un expert business. Résume les news suivantes en une phrase percutante pour un entrepreneur."},
            {"role": "user", "content": texte}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return "L'IA GPT est indisponible. Vérifiez votre solde OpenAI."

def obtenir_donnees():
    # Météo et Crypto
    res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m").text.strip()
    res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
    prix_btc = f"{res_crypto['bitcoin']['usd']:,} $"

    # News
    url_rss = "https://news.google.com/rss/search?q=IA+tech+finance&hl=fr"
    flux = feedparser.parse(url_rss)
    titres = [entry.title for entry in flux.entries[:3]]
    
    # Analyse ChatGPT
    analyse_ia = analyser_avec_gpt(" | ".join(titres))

    return (
        f"🚀 *RAPPORT ÉLITE (GPT)*\n\n"
        f"📍 {res_meteo}\n"
        f"💰 BTC: {prix_btc}\n\n"
        f"🧠 *ANALYSE STRATÉGIQUE :*\n{analyse_ia}\n\n"
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
    
