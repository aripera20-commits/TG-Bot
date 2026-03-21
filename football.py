def get_ai_prediction(home, away, league):
    # Твой токен
    HF_TOKEN = "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" 
    
    # Промпт: просим быть экспертом и писать на русском
    prompt = f"<s>[INST] Ты профессиональный футбольный аналитик. Дай очень короткий прогноз на матч {home} vs {away} ({league}). Кто победит и какой ожидаемый счет? Ответь на русском языке, максимум 2 предложения. [/INST]"
    
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers_hf = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        response = requests.post(api_url, headers=headers_hf, json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 150, "temperature": 0.7}
        })
        result = response.json()
        
        if isinstance(result, list) and 'generated_text' in result[0]:
            # Убираем сам промпт из ответа, оставляя только текст нейросети
            full_text = result[0]['generated_text']
            ai_text = full_text.split("[/INST]")[-1].strip()
            return ai_text if ai_text else "🤖 Будет жаркая игра, шансы равны!"
        
        return "🤖 По моим данным, обе команды в отличной форме. Ждем голы!"
    except Exception as e:
        print(f"HF Error: {e}")
        return "🤖 Нейросеть изучает составы... Но матч точно будет интересным! ⚽️"
