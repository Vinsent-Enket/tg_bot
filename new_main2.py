import os
import random

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.markdown import hide_link
from aiogram.utils.media_group import MediaGroupBuilder

# ссылки на мемы
memes = ["https://pic.rutubelist.ru/video/e1/b0/e1b07858d5c76253cc0b2fcedaa470f0.jpg",
         "https://i.pinimg.com/736x/2b/3f/c2/2b3fc23563175d97f9a0f6f10405fb25.jpg",
         "https://avatars.mds.yandex.net/i?id=48845ca40b1d9cb90f92c1cdcd9d2fc0_l-5682441-images-thumbs&ref=rim&n=13&w=1080&h=1080",

         ]

# BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
BOT_TOKEN = "6908027614:AAHCULVVrZBd7zKKK_2A9_weqXgY7rcR8to"
bot = Bot(
    token=BOT_TOKEN,

    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,

    )

)
dp = Dispatcher()

help_text = ("Список команд бота:\n"
             "start - запуск бота\n"
             "help - помощь\n"
             )


@dp.message(Command("start"))
@dp.message(CommandStart(
    deep_link=True
))
async def cmd_start_help(message: Message):
    await message.answer("Это старт с кнопкой старт")


# Меню бота

@dp.message(Command('menu'))
async def menu_builder(message: Message, kb_mod=None):
    # получаем на вход мод и клавиатуру этого мода, возможно получится убрать ифы

    if kb_mod:
        # kb = [kb_mod.append(types.KeyboardButton(text="Назад в мейн меню"))]
        print(kb_mod.append(types.KeyboardButton(text="Назад в мейн меню")))
        kb = [kb_mod.append(types.KeyboardButton(text="Назад в мейн меню"))]

        print("попал")
    else:
        kb = [
            [
                types.KeyboardButton(text='Мемы'),
                types.KeyboardButton(text="+2 или -2?"),
                types.KeyboardButton(text="Картинки из символов*"),
                types.KeyboardButton(text="Анекдоты*"),

            ], ]  # TODO- Сделалать инлайн кнопки, а то в одну линию не удобно

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите кнопку"
    )
    await message.answer("Выберете кнопку", reply_markup=keyboard)


@dp.message(F.text.lower() == "назад в мейн меню")
async def back_to_main_menu(message: Message):
    await menu_builder(message)


# блок кнопок мемов

@dp.message(F.text.lower() == "мемы")
async def link_meme_menu(message: Message):
    # Первая собранная клавиатура с подменю
    kb_mod = [
        types.KeyboardButton(text="Рандомный мем"),
        types.KeyboardButton(text="Альбомом"),
        types.KeyboardButton(text="По порядку"),
        types.KeyboardButton(text="Скачанные мемы"),
    ]
    print("отработка мемов")
    print(type(kb_mod))

    await menu_builder(message, kb_mod)


@dp.message(F.text.lower() == "рандомный мем")
async def with_puree(message: types.Message):
    await message.answer(f"{hide_link(random.choice(memes))}"
                         f"твой мем")


@dp.message(F.text.lower() == "альбомом")
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


@dp.message(F.text.lower() == "по порядку")
async def cmd_poryadok(message: Message):
    await message.answer("в разработке")


@dp.message(F.text.lower() == "скачанные мемы")
async def cmd_downloaded_memes(message: Message):
    await message.answer("В разработке")


# блок кнопок арифметических операций
@dp.message(F.text.lower() == "+2 или -2?")
async def arifm_operand(message: Message):
    kb_mod = [
        types.KeyboardButton(text="+-1"),
    ]
    await menu_builder(message, kb_mod)


if __name__ == '__main__':
    dp.run_polling(bot)
