import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Настройки бота
TOKEN = os.environ['TOKEN']  # Замените на токен от @BotFather
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Вопросы теста
questions = [{
    "text":
    "Чем занимается ваш бизнес?",
    "options": [["Услуги", "services"], ["Товары", "goods"],
                ["Информация", "info"]]
}, {
    "text":
    "Где ищут вас клиенты?",
    "options": [["Соцсети",
                 "social"], ["Поисковики (Google/Yandex)", "search"],
                ["Офлайн", "offline"]]
}]

# Хранение ответов
user_data = {}


# Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    user_data[chat_id] = {"step": 0, "answers": {}}
    await send_question(chat_id)


# Отправка вопроса
async def send_question(chat_id):
    step = user_data[chat_id]["step"]
    if step >= len(questions):
        await show_result(chat_id)
        return

    keyboard = InlineKeyboardMarkup()
    for option in questions[step]["options"]:
        keyboard.add(InlineKeyboardButton(option[0], callback_data=option[1]))

    await bot.send_message(chat_id,
                           questions[step]["text"],
                           reply_markup=keyboard)


# Обработка ответа
@dp.callback_query_handler()
async def handle_answer(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    user_data[chat_id]["answers"][user_data[chat_id]["step"]] = callback.data
    user_data[chat_id]["step"] += 1
    await send_question(chat_id)


# Результат
async def show_result(chat_id):
    answers = user_data[chat_id]["answers"]
    result = "📌 Ваш результат:\n\n"

    if answers.get(0) == "services":
        result += "Вам подойдёт сайт-визитка или лендинг!"
    elif answers.get(0) == "goods":
        result += "Нужен интернет-магазин (например, на Shopify)."
    else:
        result += "Попробуйте блог + SEO."

    await bot.send_message(chat_id, result)
    del user_data[chat_id]  # Очистка данных


executor.start_polling(dp)
