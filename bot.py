import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# 1. Загружаем переменные
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# 2. Инициализируем бота ОДИН РАЗ (через переменную из .env)
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

@dp.message()
async def food_trigger(message: types.Message):
    if not message.text:
        return

    text = message.text.lower()

    # Твоя логика ответов
    responses = {
        "шаверма": "🥙 <b>Шаверма</b> — это очень вкусная еда!",
        "пицца": "🍕 <b>Пицца</b> — классика!",
        "пошел нахуй": "Тотак",
        "хелло": "Хаваю?",
        "фке": "Сокнма блад",
        "хн": "Хн",
        "бля": "Бладь"
    }

    for key, val in responses.items():
        if key in text:
            await message.reply(val)
            break # Отвечаем один раз, даже если в тексте несколько ключей

async def main():
    print("Бот запущен и готов к работе!")
    # Удаляем вебхуки и пропущенные сообщения перед стартом
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")