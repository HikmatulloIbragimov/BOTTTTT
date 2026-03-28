import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

# Импортируем логику ИИ
from utils.ai_logic import ask_deepseek

# 1. Загружаем переменные
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
# Список имен-триггеров
NICKNAMES = ["дипсик", "deepseek", "дип", "deep"]

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# 2. Инициализируем бота
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # ИИ генерирует приветствие
    response = ask_deepseek("", is_start=True)
    await message.answer(response)

# Основной обработчик сообщений
@dp.message()
async def main_handler(message: types.Message):
    if not message.text:
        return

    text_lower = message.text.lower()

    # --- ЧАСТЬ 1: Твои заготовленные ответы (Food & Slang) ---
    responses = {
        "шаверма": "🥙 <b>Шаверма</b> — это очень вкусная еда!",
        "пицца": "🍕 <b>Пицца</b> — классика!",
        "пошел нахуй": "Тотак",
        "хелло": "Хаваю?",
        "фке": "Сокнма блад",
        "хн": "Хн",
        "бля": "Бладь",
        "далбаеб": "хм"
    }

    for key, val in responses.items():
        if key in text_lower:
            await message.reply(val)
            return  # Если сработал триггер, ИИ уже не трогаем

    # --- ЧАСТЬ 2: Логика DeepSeek ---
    if any(name in text_lower for name in NICKNAMES):
        # Показываем статус "печатает"
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        # Запрос к ИИ
        ai_response = ask_deepseek(message.text)
        await message.reply(ai_response)

async def main():
    print("Бот запущен и готов к работе через Aiogram 3!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")