import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

TOKEN = os.getenv('MAHTAL_BOT_APITOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("✅ Бот успешно запущен!")

@dp.message(Command("menu"))
async def show_menu(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="yes")
    builder.button(text="Нет", callback_data="no")
    await message.answer("Выберите вариант:", reply_markup=builder.as_markup())

@dp.message()
async def handle_unknown(message: Message):
    await message.answer("Неизвестная команда. Попробуйте /start")
        
async def main():
    # Удаляем вебхук перед стартом
    await bot.delete_webhook(drop_pending_updates=True)
    print("🔄 Вебхук удалён, запускаем поллинг...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("🔄 Инициализация бота...")
    asyncio.run(main())