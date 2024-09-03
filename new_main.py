import os
import random

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hide_link

memes = ["https://pic.rutubelist.ru/video/e1/b0/e1b07858d5c76253cc0b2fcedaa470f0.jpg",
         "https://i.pinimg.com/736x/2b/3f/c2/2b3fc23563175d97f9a0f6f10405fb25.jpg",
         "https://avatars.mds.yandex.net/i?id=48845ca40b1d9cb90f92c1cdcd9d2fc0_l-5682441-images-thumbs&ref=rim&n=13&w=1080&h=1080",

         ]

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


@dp.message(Command("random_meme_1"))
async def process_random_meme_1(message: Message):
    kb = [
        [
            types.KeyboardButton(text="Рандом"),
            types.KeyboardButton(text="Все сразу")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите кнопку"
    )
    await message.answer("Какую отправить мем?", reply_markup=keyboard)

@dp.message(F.text.lower() == "рандом")
async def with_puree(message: types.Message):
    await message.answer(f"{hide_link(random.choice(memes))}"
                         f"твой мем")


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_about_command(message: Message):
    await message.answer(help_text)


@dp.message(F.photo)
async def echo_photo(message: Message):
    await message.reply_photo(message.photo[0].file_id)


# функция отправки рандомного мема
@dp.message(Command(commands=['meme']))
async def process_meme_command(message: Message):
    await message.answer(f"{hide_link(random.choice(memes))}"
                         f"твой мем")


if __name__ == '__main__':
    dp.run_polling(bot)
