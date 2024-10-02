import os
import random

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.markdown import hide_link
from aiogram.utils.media_group import MediaGroupBuilder

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


# Меню с кнопками
@dp.message(Command("menu"))
async def process_random_meme_1(message: Message):
    kb = [
        [
            types.KeyboardButton(text="Рандом"),
            types.KeyboardButton(text="Альбом")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите кнопку"
    )
    await message.answer("Какую отправить мем?", reply_markup=keyboard)


@dp.message(Command('work_menu'))
async def work_menu_builder(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Запросить геолокацию", request_location=True),
        types.KeyboardButton(text="Запросить контакт", request_contact=True)
    )
    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(Command('test_menu'))
async def menu_builder(message: Message, mod=None):
    if mod == 'main':
        kb = [[
            types.KeyboardButton(text='Ссылочные мемы'),
            types.KeyboardButton(text="Скачанные мемы"),
            types.KeyboardButton(text="Картинки из символов"),
            types.KeyboardButton(text="Анекдоты"),
        ], ]
    elif mod == 'meme':
        kb = [
            [
                types.KeyboardButton(text="Рандом"),
                types.KeyboardButton(text="Альбом"),
                types.KeyboardButton(text="Назад в мейн меню"),
            ], ]
    else:
        kb = [[
            types.KeyboardButton(text='Ссылочные мемы'),
            types.KeyboardButton(text="Скачанные мемы"),
            types.KeyboardButton(text="Картинки из символов"),
            types.KeyboardButton(text="Анекдоты"),
        ], ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите кнопку"
    )
    await message.answer("Какую отправить мем?", reply_markup=keyboard)


@dp.message(F.text.lower() == "ссылочные мемы")
async def link_meme_menu(message: Message):
    await menu_builder(message, 'meme')


@dp.message(F.text.lower() == "назад в мейн меню")
async def back_to_main_menu(message: Message):
    await menu_builder(message, 'main')


@dp.message(F.text.lower() == "рандом")
async def with_puree(message: types.Message):
    await message.answer(f"{hide_link(random.choice(memes))}"
                         f"твой мем")


@dp.message(F.text.lower() == "альбом")
async def cmd_album(message: Message):
    album_builder = MediaGroupBuilder(  # создаем альбом и задаем ему описание
        caption="Подпись для альбома"
    )
    album_builder.add(
        type="photo",
        media="https://minecraft-inside.ru/forum/uploads/monthly_2024_05/skeleton-funny.gif.d543de0ca22d3e1605b1003477ee4ddc.gif"
        # caption="Подпись к конкретному медиа"

    )
    # Если мы сразу знаем тип, то вместо общего add
    # можно сразу вызывать add_<тип>
    album_builder.add_photo(
        # Для ссылок или file_id достаточно сразу указать значение
        media="https://cdn1.flamp.ru/a3a68875a3f3168937422b1ff97c007b.jpeg",
        caption="Подпись к мему"
    )
    album_builder.add_photo(
        media="https://avatars.mds.yandex.net/i?id=644791b5c94139006f78598f566904252799a80f13ffccf2-12653362-images-thumbs&n=13"
    )
    await message.answer_media_group(
        # Не забудьте вызвать build()
        media=album_builder.build()
    )


if __name__ == '__main__':
    dp.run_polling(bot)
