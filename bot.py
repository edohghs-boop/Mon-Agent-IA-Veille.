import os
import requests
import feedparser

def analyser_avec_gemini(texte):
    api_key = os.getenv('GEMINI_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"Résume en une phrase : {texte}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        # Si Google renvoie une erreur, on l'affiche clairement
        if 'error' in data:
            return f"❌ Erreur Google : {data['error']['message']}"
            
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"❌ Problème technique : {str(e)}"

def obtenir_donnees():
    res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m").text.strip()
    res_crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
    prix_btc = f"{res_crypto['bitcoin']['usd']:,} $"

    url_rss = "https://news.google.com/rss/search?q=IA+tech+finance&hl=fr"
    flux = feedparser.parse(url_rss)
    titres = [entry.title for entry in flux.entries[:3]]
    
    # On teste l'analyse
    analyse_ia = analyser_avec_gemini(" | ".join(titres))

    return f"🛠️ **TEST DIAGNOSTIC**\n\n📍 {res_meteo}\n💰 BTC: {prix_btc}\n\n🤖 **RÉPONSE IA :**\n{analyse_ia}"

def envoyer_telegram(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                  json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    rapport = obtenir_donnees()
    envoyer_telegram(rapport)
    
