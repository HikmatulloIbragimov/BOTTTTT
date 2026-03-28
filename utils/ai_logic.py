import os
from openai import AsyncOpenAI

# Инициализируем асинхронный клиент
# Он будет брать ключ из переменных Railway
client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://railway.app",
        "X-Title": "MyAiBot"
    }
)

async def ask_deepseek(user_text, is_start=False):
    """
    ВАЖНО: функция теперь async. 
    Мы добавили аргумент is_start для обработки команды /start.
    """
    try:
        if is_start:
            system_prompt = "Ты — крутой ИИ-ассистент. Поприветствуй всех и скажи, что откликаешься на имя Дип."
            user_content = "Представься."
        else:
            system_prompt = "Ты — полезный ИИ-ассистент. Отвечай кратко."
            user_content = user_text

        completion = await client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"🤖 Ошибка ИИ: {e}"