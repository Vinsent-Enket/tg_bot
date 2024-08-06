import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Bold, Text
from aiogram.types import LinkPreviewOptions


BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

hello_text = ('Здравствуйте, я бот <strong>автосервиса</strong>,'
              ' с моей помощью вы можете оставить заявку на звонок мастера')

about_text = 'Мы находимся по адресу - Москва, наш сайт - https://www.test.ru'

# TODO: Сделать команду для таймера и будильника, крч периодические задачи

# TODO: По запросу Алексея, добавить отправку анекдотов по номерам (еще и случайного)
#  и по расписанию вычислять пидора (вот тебе и периодические задачи).

"""
топ html разметок

1. <p> — параграф.
2. <h1> — заголовок первого уровня.
3. <h2> — заголовок второго уровня.
4. <h3> — заголовок третьего уровня.
5. <h4> — заголовок четвертого уровня.
6. <h5> — заголовок пятого уровня.
7. <h6> — заголовок шестого уровня.
8. <br> — перенос строки.
9. <strong> — выделение жирным шрифтом.
10. <em> — выделение курсивом.
11. <img> — изображение.
12. <a> — гиперссылка.
13. <ul> — маркированный список.
14. <ol> — нумерованный список.
15. <li> — элемент списка.
16. <div> — контейнер для группировки других элементов.
17. <span> — контейнер для форматирования текста.
18. <table> — таблица.
19. <tr> — строка таблицы.
20. <td> — ячейка таблицы.
"""

"""

Свои пояснения:

У нас есть бот, который будет обрабатывать команды

У него есть диспетчер который реагирует на сообщения


Разберем примером

@dp.message(Command(commands=["start"]))  - регистрируем команду "/start
async def process_start_command(message: Message):
    await message.answer(  - указываем что будет в ответе
        f'Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь\n\n\n{message.model_dump_json(indent=4, 
        exclude_none=True)}')
        
        
    есть answer - это просто текст
    а есть reply - это уже *ответ*

"""

# Создаем объекты бота и диспетчера
# bot = Bot(token=BOT_TOKEN)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
# @dp.message(Command(commands=['start']))
# async def process_start_command(message: Message):
#     await message.answer(hello_text)


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['about']))
async def process_about_command(message: Message):
    await message.answer(about_text)


@dp.message(Command("start"))
@dp.message(CommandStart(
    deep_link=True
))
async def cmd_start_help(message: Message):
    await message.answer("Это старт с кнопкой старт")
# кастомные команды

@dp.message(Command(commands='get_id'))
async def process_get_id_command(message: Message):
    await message.answer(f'ID: {message.chat.id}')


@dp.message(Command(commands="hello"))
async def process_hello_command(message: Message):
    await message.reply(f'Привет, {message.from_user.first_name}!')


@dp.message(Command(commands='format'))
async def process_f_answer_command(message: Message,
                                   command: CommandObject):
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    text = command.args
    content = Text(
        "Ваш текст - \n, ",
        Bold(text)
    )
    await message.reply(
        **content.as_kwargs()
    )


@dp.message(Command('dice'))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message(Command('stats'))
async def cmd_stats(message: types.Message):
    await message.answer(f'Статистика: {message.chat.id}\n'
                         f'{message.chat.username}\n'
                         f'{message.chat.first_name}\n'
                         f'{message.chat.last_name}\n'
                         f'Премиум {message.from_user.is_premium}')




# Новый импорт

@dp.message(Command("links"))
async def cmd_links(message: Message):
    links_text = (
        "https://nplus1.ru/news/2024/05/23/voyager-1-science-data"
        "\n"
        "https://t.me/telegram"
    )
    # Ссылка отключена
    options_1 = LinkPreviewOptions(is_disabled=True)
    await message.answer(
        f"Нет превью ссылок\n{links_text}",
        link_preview_options=options_1
    )

    # -------------------- #

    # Маленькое превью
    # Для использования prefer_small_media обязательно указывать ещё и url
    options_2 = LinkPreviewOptions(
        url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data",
        prefer_small_media=True
    )
    await message.answer(
        f"Маленькое превью\n{links_text}",
        link_preview_options=options_2
    )

    # -------------------- #

    # Большое превью
    # Для использования prefer_large_media обязательно указывать ещё и url
    options_3 = LinkPreviewOptions(
        url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data",
        prefer_large_media=True
    )
    await message.answer(
        f"Большое превью\n{links_text}",
        link_preview_options=options_3
    )

    # -------------------- #

    # Можно сочетать: маленькое превью и расположение над текстом
    options_4 = LinkPreviewOptions(
        url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data",
        prefer_small_media=True,
        show_above_text=True
    )
    await message.answer(
        f"Маленькое превью над текстом\n{links_text}",
        link_preview_options=options_4
    )

    # -------------------- #

    # Можно выбрать, какая ссылка будет использоваться для предпосмотра,
    options_5 = LinkPreviewOptions(
        url="https://t.me/telegram"
    )
    await message.answer(
        f"Предпросмотр не первой ссылки\n{links_text}",
        link_preview_options=options_5
    )

"""
----------------------------------------------------------------------------------------------
"""


@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)
