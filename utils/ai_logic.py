import os
import asyncio
from openai import AsyncOpenAI  # Используем АСИНХРОННЫЙ клиент
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# 🔑 Берем ключи из переменных окружения (Railway)
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

# ✅ Настройка асинхронного клиента
client = AsyncOpenAI(
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://railway.app", # Чтобы OpenRouter не давал 404
        "X-Title": "MyAiBot"
    }
)

bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

@dp.message(F.text)
async def ai_chat(message: Message):
    # Убираем прозвища (если нужно) или просто шлем текст
    user_input = message.text

    try:
        # ✅ Используем await, чтобы бот не зависал
        completion = await client.chat.completions.create(
            model="google/gemini-2.0-flash-lite-preview-02-05:free", # Самая стабильная бесплатная модель
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        
        reply = completion.choices[0].message.content
        await message.answer(reply)
        
    except Exception as e:
        await message.answer(f"🤖 Ошибка: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())