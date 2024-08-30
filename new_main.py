import os

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import ssl

#session = AiohttpSession(proxy="http://proxy.server:3128", )

BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

bot = Bot(
    token=BOT_TOKEN,

    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,

    )

)
dp = Dispatcher()

help_text = ("Список команд бота:\n"
             "start - запуск бота\n")


@dp.message(Command("start"))
@dp.message(CommandStart(
    deep_link=True
))
async def cmd_start_help(message: Message):
    await message.answer("Это старт с кнопкой старт")


@dp.message(Command("help"))
async def process_about_command(message: Message):
    await message.answer(help_text)
    


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_about_command(message: Message):
    await message.answer(help_text)


if __name__ == '__main__':
    dp.run_polling(bot)
