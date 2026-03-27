import os
import re
from openai import OpenAI

# Инициализация клиента
# Переменную DEEPSEEK_API_KEY нужно добавить в Settings -> Variables на Railway
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url=os.getenv("BASE_URL")
)

# Список прозвищ для очистки (чтобы ИИ не получал их в запросе)
NICKNAMES_PATTERN = r"(?i)(дипсик|deepseek|дип|deep)"

def clean_text(text):
    """Убирает прозвище из сообщения, чтобы оставить только суть вопроса"""
    cleaned = re.sub(NICKNAMES_PATTERN, "", text).strip()
    # Убираем лишние запятые и знаки препинания, которые могли остаться после обращения
    cleaned = re.sub(r"^[,\.\s!]+", "", cleaned)
    return cleaned

def ask_deepseek(user_text, is_start=False):
    """Основная функция для общения с ИИ"""
    
    # Если это первый запуск (команда /start)
    if is_start:
        system_prompt = "Ты — крутой ИИ-ассистент в группе. Поприветствуй всех, скажи, что откликнешься на имя 'Дип' или 'Дипсик'."
        user_prompt = "Представься группе."
    else:
        # Очищаем текст сообщения от прозвищ
        prompt = clean_text(user_text)
        
        # Если после очистки текста не осталось (написали просто "Дип")
        if not prompt:
            return "Слушаю! Есть какой-то вопрос или задача? Просто добавь её после моего имени."
            
        system_prompt = "Ты — полезный и лаконичный ИИ-ассистент. Отвечай прямо и по делу."
        user_prompt = prompt

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat:free", # Модель DeepSeek-V3
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        # Если API выдает ошибку (например, кончились деньги или лимиты)
        return f"🤖 Упс, что-то пошло не так: {e}"

# Эту функцию можно использовать для тестирования прямо в консоли:
if __name__ == "__main__":
    # Проверка: замени ключ на реальный, если хочешь протестить без бота
    # print(ask_deepseek("Дип, как дела?"))
    pass