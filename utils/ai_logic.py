import os
import re
from openai import OpenAI

# Инициализация клиента с заголовками для OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), 
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://railway.app", # Обязательно для OpenRouter
        "X-Title": "Telegram AI Bot",          # Название твоего приложения
    }
)

NICKNAMES_PATTERN = r"(?i)(дипсик|deepseek|дип|deep)"

def clean_text(text):
    cleaned = re.sub(NICKNAMES_PATTERN, "", text).strip()
    cleaned = re.sub(r"^[,\.\s!]+", "", cleaned)
    return cleaned

def ask_deepseek(user_text, is_start=False):
    key = os.getenv("OPENROUTER_API_KEY")
    
    # Если ключа нет в системе - мы это сразу увидим
    if not key:
        return "🤖 Ошибка: Railway не видит переменную OPENROUTER_API_KEY"

    # Печатаем в логи Railway первые 10 символов ключа для проверки
    print(f"DEBUG: Использую ключ {key[:10]}...")

    prompt = "Привет!" if is_start else clean_text(user_text)
    
    try:
        response = client.chat.completions.create(
            # Давай попробуем эту модель - она самая простая и безотказная
            model="google/gemini-2.0-flash-lite-preview-02-05:free",
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": "https://railway.app",
                "X-Title": "TelegramBot",
            }
        )
        return response.choices[0].message.content
    except Exception as e:
        # Если здесь вылетит 404, значит OpenRouter не нравится наш запрос
        return f"🤖 Ошибка API: {e}"
    # Если это /start
    if is_start:
        system_prompt = "Ты — крутой ИИ-ассистент. Поприветствуй всех, скажи, что тебя зовут Дип."
        user_prompt = "Представься группе."
    else:
        prompt = clean_text(user_text)
        if not prompt:
            return "Слушаю! Напиши что-нибудь после моего имени."
            
        system_prompt = "Ты — полезный и лаконичный ИИ-ассистент."
        user_prompt = prompt

    try:
        # Пробуем САМУЮ доступную сейчас бесплатную модель
        # Если хочешь именно DeepSeek, замени на "deepseek/deepseek-r1:free"
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-lite-preview-02-05:free", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        # Если 404 повторяется, попробуй в консоли Railway проверить переменную OPENROUTER_API_KEY
        return f"🤖 Упс, что-то пошло не так: {e}"