"""
Это будет просто копипаста с сайта, https://mastergroosha.github.io/aiogram-3-guide/quickstart/
Постарайся давать комментарии, что бы выбрать отсюда лучшее и уже потом добавить в основу
Все команды добавь в /help
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# 2 декабря добавил первые импорты
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


# Хэндлер на команду /start
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Привет!')


# хэндлер на команду Хелп
@dp.message(Command('help'))
async def hlp_command(message: types.Message):
    answer = ("Приветствую! \n"
              "Список все команд:\n"
              "/start - запуск бота \n"  # может сделать перезапуск?
              "/help - помощь \n")
    await message.answer(answer)


"""
Команды можно регистрировать как сразу через декоратор, так и позже
"""


@dp.message(Command('test1'))
async def test1_command(message: types.Message):
    await message.answer('test1')

async def test2_command(message: types.Message):
    await message.answer('test2')

dp.message.register(test2_command, Command('test2'))





# Запуск процесса поллинга (ожидания апдейтов???)
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
