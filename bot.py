import os
import requests
import feedparser

def analyser_avec_gemini(texte):
    api_key = os.getenv('GEMINI_API_KEY')
    # Utilisation du modèle flash, rapide et gratuit
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"Tu es un analyste financier et tech. Voici les titres de l'actualité : {texte}. Fais-en un résumé très court (2 phrases maximum) qui explique la tendance d'aujourd'hui pour un entrepreneur."
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        # On extrait la réponse de Gemini
        resultat = response.json()
        return resultat['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"L'IA est en pause (Vérifie ta clé GEMINI_API_KEY). Erreur : {str(e)[:50]}"

def obtenir_donnees():
    # 1. Météo Zanguéra
    try:
        res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m").text.strip()
    except:
        res_meteo = "Météo indisponible"

    # 2. Prix du Bitcoin en Dollars
    try:
        res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
        prix_btc = f"{res_crypto['bitcoin']['usd']:,} $"
    except:
        prix_btc = "Indisponible"

    # 3. News IA, Tech, Finance
    url_rss = "https://news.google.com/rss/search?q=IA+tech+finance&hl=fr&gl=FR&ceid=FR:fr"
    flux = feedparser.parse(url_rss)
    # On récupère les 3 premiers titres complets
    titres = [entry.title for entry in flux.entries[:3]]
    liens = [entry.link for entry in flux.entries[:3]]
    
    # 4. Analyse par l'IA Gemini
    analyse_ia = analyser_avec_gemini(" | ".join(titres))

    # Construction du message final sans coupure
    message = (
        f"🚀 *VOTRE VEILLE STRATÉGIQUE*\n\n"
        f"📍 {res_meteo}\n"
        f"💰 BTC : {prix_btc}\n\n"
        f"🧠 *ANALYSE DE GEMINI :*\n{analyse_ia}\n\n"
        f"🔗 *SOURCES DÉTAILLÉES :*\n"
        f"1️⃣ [{titres[0]}]({liens[0]})\n\n"
        f"2️⃣ [{titres[1]}]({liens[1]})\n\n"
        f"3️⃣ [{titres[2]}]({liens[2]})"
    )
    return message

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    rapport = obtenir_donnees()
    envoyer_telegram(rapport)
    
