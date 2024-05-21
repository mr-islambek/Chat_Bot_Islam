import requests, json
from aiogram import Bot, Dispatcher, types
from aiogram import executor
import os
from dotenv import load_dotenv


load_dotenv()

# Токен API Gemini AI
GEMINI_AI_TOKEN = os.getenv("GEMINI_AI_TOKEN")
# Токен вашего Телеграм бота
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


# Функция отправки запроса к API Gemini AI
async def get_gemini_ai_response(text: str) -> str:
    # headers = {"Authorization": f"Bearer {GEMINI_AI_TOKEN}"}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_AI_TOKEN}"
    headers = {"Content-Type": "application/json"}

    data = {"contents": [{"parts": [{"text": f"{text}"}]}]}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    json_data = response.json()
    text2 = json_data["candidates"][0]["content"]["parts"][0]["text"]
    return text2


# Обработка команды /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я помощник Ислама. Задайте мне свой вопрос.")


# Обработка текстовых сообщений
@dp.message_handler(lambda message: message.text and not message.text.startswith("/"))
async def echo(message: types.Message):
    user_message = message.text
    bot_response = await get_gemini_ai_response(user_message)
    await message.reply(bot_response)


# Обработка неизвестных команд
@dp.message_handler()
async def unknown(message: types.Message):
    await message.reply("Извините, я не понимаю эту команду.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
