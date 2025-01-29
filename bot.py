"""
Это будет просто копипаста с сайта, https://mastergroosha.github.io/aiogram-3-guide/quickstart/
Постарайся давать комментарии, что бы выбрать отсюда лучшее и уже потом добавить в основу
Все команды добавь в /help
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from datetime import datetime

"""
Апдейт — любое событие из этого списка: сообщение, редактирование сообщения, колбэк, инлайн-запрос, платёж, добавление бота в группу и т.д.
Хэндлер — асинхронная функция, которая получает от диспетчера/роутера очередной апдейт и обрабатывает его.
Диспетчер — объект, занимающийся получением апдейтов от Telegram с последующим выбором хэндлера для обработки принятого апдейта.
Роутер — аналогично диспетчеру, но отвечает за подмножество множества хэндлеров. Можно сказать, что диспетчер — это корневой роутер.
Фильтр — выражение, которое обычно возвращает True или False и влияет на то, будет вызван хэндлер или нет.
Мидлварь — прослойка, которая вклинивается в обработку апдейтов.
"""

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем самого бота
BOT_TOKEN = "6908027614:AAHCULVVrZBd7zKKK_2A9_weqXgY7rcR8to"  # TODO: заменить на переменную окружения

bot = Bot(token=BOT_TOKEN)

# Диспетчер
dp = Dispatcher()
dp['started_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')


# Хэндлер на команду /start
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Привет!\n'
                         'Для вызова всех команд вызови /help')


# хэндлер на команду Хелп
@dp.message(Command('help'))
async def hlp_command(message: types.Message):
    answer = ("Приветствую! \n"
              "Список все команд:\n"
              "/start - запуск бота \n"  # может сделать перезапуск?
              "/help - помощь \n"
              "/test1 - просто ответ \n"
              "/test2 - ответ на сообщение \n"
              "/add_to_list - добавить число в список \n"
              "/show_list - показать список \n"
              "/info - информация о боте"
              "/dice - кинуть кубик")
    await message.answer(answer)


"""
Команды можно регистрировать как сразу через декоратор, так и позже
"""


@dp.message(Command('test1'))
# простой ответ на сообщение
async def test1_command(message: types.Message):
    await message.answer('просто ответ')


# ответ как будто через контекстное меню
async def test2_command(message: types.Message):
    await message.reply('ответ на сообщение')


@dp.message(Command('dice'))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


dp.message.register(test2_command, Command('test2'))


@dp.message(Command('add_to_list'))
async def cmd_add_to_list(message: types.Message, my_list: list[int]):
    my_list.append(7)
    print(my_list)
    await message.answer(f"Добавлено число 7")


@dp.message(Command('show_list'))
async def cmd_show_list(message: types.Message, my_list: list[int]):
    print(my_list)
    await message.answer(f"Список: {my_list}")


@dp.message(Command('info'))
async def cmd_info(message: types.Message):
    await message.answer(f"Бот запущен: {dp['started_at']}")


# Запуск процесса поллинга (ожидания апдейтов???)
async def main():
    # await dp.start_polling(bot)
    await dp.start_polling(bot, my_list=[1, 2, 3])


if __name__ == '__main__':
    asyncio.run(main())
