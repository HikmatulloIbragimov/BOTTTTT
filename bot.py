import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram import F

# Импортируем нашу асинхронную функцию
from utils.ai_logic import ask_deepseek

# Настройка
TOKEN = os.getenv("BOT_TOKEN")
NICKNAMES = ["дипсик", "deepseek", "дип", "deep"]

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# 1. Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Добавляем await, так как ask_deepseek — асинхронная!
    response = await ask_deepseek("", is_start=True)
    await message.answer(response)

# 2. Основной обработчик
@dp.message(F.text)
async def main_handler(message: types.Message):
    text_lower = message.text.lower()

    # --- ЧАСТЬ 1: Твои заготовленные ответы ---
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
            return 

    # --- ЧАСТЬ 2: Логика ИИ (Deep/Gemini) ---
    if any(name in text_lower for name in NICKNAMES):
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        # ОБЯЗАТЕЛЬНО await перед вызовом!
        ai_response = await ask_deepseek(message.text)
        await message.reply(ai_response)

async def main():
    print("🚀 Бот запущен и готов к работе!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")