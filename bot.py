from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor

from aiogram import types

import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

import phonenumbers

from states import MakeClaim, MakeRequest, Menu

from config import TOKEN, ADMIN_ID

from utils import types_menu, places_menu, get_type_name, get_place_name, places_list

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

main_menu = types.InlineKeyboardMarkup(resize_keyboard=True)
main_menu.add(types.InlineKeyboardButton("Информация о точках(адреса, время работы)", callback_data="info"))
main_menu.add(types.InlineKeyboardButton("Написать жалобу", callback_data="make_claim"))
main_menu.add(types.InlineKeyboardButton("Написать предложение или вопрос", callback_data="make_request"))
main_menu.add(types.InlineKeyboardButton("Хочу стать партнером", callback_data="partnership"))


@dp.message_handler(commands=['start'], state='*')
async def start(mes: Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass

    if mes.from_user.first_name is not None:
        await mes.answer(f"""Здравствуйте, {mes.from_user.first_name}!
Вас приветствует чат-бот Sunday Coffee.
    
Выберите заведение.""", reply_markup=places_menu)

    else:
        await mes.answer(f"""Здравствуйте!
Вас приветствует чат-бот Sunday Coffee.

Выберите заведение.""", reply_markup=places_menu)

    # await mes.bot.send_message(ADMIN_ID, f"{mes.from_user.id}: {mes.from_user.username}/{mes.chat.id} - {mes.from_user.first_name}")


@dp.callback_query_handler(lambda call: call.data == "info", state='*')
async def info(call: CallbackQuery, state: FSMContext):

    try:
        await state.finish()
    except:
        pass

    await call.bot.send_message(call.from_user.id, """Ждем Вас в наших филиалах в городе Алматы:
    
    - Абая 17
    - Орбита 3, 5Е
    - Тимирязева 38Б
    - Жибек жолы 106
    - Желтоксан 59/3
    - Тимирязева 42/6
    - Медео
    
    Время работы на всех точках с 8:00 до 00:00,
    Кроме Медео где Мы угостим Вас чашкой ароматного кофе с 8:00 до 02:00.""", reply_markup=places_menu)


@dp.callback_query_handler(lambda call: call.data == "partnership", state='*')
async def info(call: CallbackQuery, state: FSMContext):

    try:
        await state.finish()
    except:
        pass

    await call.bot.send_message(call.from_user.id, """Партнерство""", reply_markup=places_menu)


@dp.callback_query_handler(lambda call: call.data in [place.get('callback_data') for place in places_list], state='*')
async def info(call: CallbackQuery, state: FSMContext):

    await Menu.place.set()

    state = Dispatcher.get_current().current_state()
    await state.update_data(place=call.data)

    await call.bot.send_message(call.from_user.id, f"Что Вы хотите?", reply_markup=main_menu)


if __name__ == "__main__":
    from write_report_handlers import *
    from write_request_handlers import *

    executor.start_polling(dp)
