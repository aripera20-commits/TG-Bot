import telebot
import requests
import os
from flask import Flask
from threading import Thread

# --- ЖИВИТЕЛЬНЫЙ СЕРВЕР ДЛЯ RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Бот в порядке!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- КЛЮЧИ ---
TOKEN = '8624691803:AAHONwvZ3e6A99Aac-JjwEdUvJgpqiqM1m0'
FOOTBALL_API_KEY = 'f2539298091241a187bf9394eb390ab7'
HF_TOKEN = "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"

bot = telebot.TeleBot(TOKEN)

def get_ai_prediction(home, away, league):
    # Промпт для Mistral
    prompt = f"<s>[INST] Ты футбольный эксперт. Кратко (1-2 предложения) на русском: кто победит в матче {home} - {away} ({league}) и какой счет? [/INST]"
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        response = requests.post(api_url, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 100}}, timeout=10)
        result = response.json()
        
        if isinstance(result, list):
            full_text = result[0].get('generated_text', "")
            return full_text.split("[/INST]")[-1].strip()
        return "🤖 Шансы равны, будет битва!"
    except:
        return "🤖 Нейросеть отдыхает, но матч обещает быть жарким!"

def get_match_data(team_query):
    headers = {'X-Auth-Token': FOOTBALL_API_KEY}
    try:
        res = requests.get("https://api.football-data.org/v4/matches", headers=headers, timeout=10).json()
        matches = res.get('matches', [])
    except:
        return "⚠️ Ошибка футбольного API.", ""
    
    q = team_query.lower()
    for m in matches:
        h, a = m['homeTeam']['name'], m['awayTeam']['name']
        if q in h.lower() or q in a.lower():
            analysis = get_ai_prediction(h, a, m['competition']['name'])
            text = f"🏟 **Матч:** {h} vs {a}\n🏆 **Лига:** {m['competition']['name']}\n\n🧠 **Прогноз:**\n{analysis}"
            return text, m['homeTeam']['crest']
    return f"🤷‍♂️ Матч для '{team_query}' не найден.", ""

@bot.message_handler(func=lambda m: True)
def handle(m):
    if m.text == "/start":
        bot.reply_to(m, "Напиши команду!")
        return
    status = bot.reply_to(m, "⏳ Собираю аналитику...")
    text, logo = get_match_data(m.text)
    if logo:
        bot.send_photo(m.chat.id, logo, caption=text, parse_mode='Markdown')
        bot.delete_message(m.chat.id, status.message_id)
    else:
        bot.edit_message_text(text, m.chat.id, status.message_id)

if __name__ == "__main__":
    keep_alive()
    print("✅ БОТ СТАРТОВАЛ!")
    bot.infinity_polling()
