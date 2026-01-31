import os
import requests
import feedparser

def analyser_avec_groq(texte):
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        return "Erreur : La clé GROQ_API_KEY est introuvable."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Utilisation du modèle Llama 3.3 70B (le plus performant)
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": "Tu es un expert business. Résume ces news en une phrase courte et motivante pour un entrepreneur au Togo."
            },
            {"role": "user", "content": texte}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        res_data = response.json()
        
        # Gestion des erreurs renvoyées par l'API
        if 'error' in res_data:
            return f"Note : L'IA se repose. Erreur : {res_data['error']['code']}"
            
        return res_data['choices'][0]['message']['content']
    except Exception as e:
        return "L'IA prépare sa prochaine analyse."

def obtenir_donnees():
    # 1. Météo
    try:
        res_meteo = requests.get("https://wttr.in/Zanguera?format=3&m").text.strip()
    except:
        res_met
        
