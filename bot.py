from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor

from aiogram import types

import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from config import TOKEN

# from operations import *
#
# from states import *


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(types.KeyboardButton("Информация о точках(адреса, время работы)"))
main_menu.add(types.KeyboardButton("Написать жалобу"))
main_menu.add(types.KeyboardButton("Написать предложение или вопрос"))


@dp.message_handler(commands=['start'])
async def start(mes: Message):
    await mes.answer("""Здравствуйте!
Вас приветствует чат-бот Sunday Coffee.

Выберите то что Вас интересует.""")


@dp.message_handler(lambda mes: mes.text == "Информация о точках(адреса, время работы)")
async def info(mes: Message):
    await mes.answer("""Ждем Вас в наших филиалах в городе Алматы:
    
    - Абая 17
    - Орбита 3, 5Е
    - Тимирязева 38Б
    - Жибек жолы 106
    - Желтоксан 59/3
    - Тимирязева 42/6
    - Медео
    
    Время работы на всех точках с 8:00 до 00:00,
    Кроме Медео где Мы угостим Вас чашкой ароматного кофе с 8:00 до 02:00.""")


@dp.message_handler(lambda mes: mes.text == "Написать жалобу")
async def report(mes: Message):
    pass


@dp.message_handler(lambda mes: mes.text == "Написать предложение или вопрос")
async def request(mes: Message):
    pass


if __name__ == "__main__":
    executor.start_polling(dp)
