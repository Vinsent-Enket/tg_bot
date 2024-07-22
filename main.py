import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

hello_text = ('Здравствуйте, я бот <strong>автосервиса</strong>,'
              ' с моей помощью вы можете оставить заявку на звонок мастера')

about_text = 'Мы находимся по адресу - Москва, наш сайт - https://www.test.ru'

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
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(hello_text)


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['about']))
async def process_about_command(message: Message):
    await message.answer(about_text)


# кастомные команды

@dp.message(Command(commands='get_id'))
async def process_get_id_command(message: Message):
    await message.answer(f'ID: {message.chat.id}')


@dp.message(Command('dice'))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message(Command('stats'))
async def cmd_stats(message: types.Message):
    await message.answer(f'Статистика: {message.chat.id}\n'
                         f'{message.chat.username}\n'
                         f'{message.chat.first_name}\n'
                         f'{message.chat.last_name}\n'
                         f'{message.from_user.is_premium}')


@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)
