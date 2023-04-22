from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor

from aiogram import types

import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

import phonenumbers

from config import TOKEN

from utils import types_menu, places_menu, get_type_name, get_place_name

# from operations import *
#
from states import MakeClaim


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

main_menu = types.InlineKeyboardMarkup(resize_keyboard=True)
main_menu.add(types.InlineKeyboardButton("Информация о точках(адреса, время работы)", callback_data="info"))
main_menu.add(types.InlineKeyboardButton("Написать жалобу", callback_data="make_claim"))
main_menu.add(types.InlineKeyboardButton("Написать предложение или вопрос", callback_data="make_request"))


@dp.message_handler(commands=['start'], state='*')
async def start(mes: Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass

    if mes.from_user.first_name is not None:
        await mes.answer(f"""Здравствуйте, {mes.from_user.first_name}!
Вас приветствует чат-бот Sunday Coffee.
    
Выберите то что Вас интересует.""", reply_markup=main_menu)

    else:
        await mes.answer(f"""Здравствуйте!
Вас приветствует чат-бот Sunday Coffee.

Выберите то что Вас интересует.""", reply_markup=main_menu)


@dp.callback_query_handler(lambda call: call.data == "info")
async def info(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, """Ждем Вас в наших филиалах в городе Алматы:
    
    - Абая 17
    - Орбита 3, 5Е
    - Тимирязева 38Б
    - Жибек жолы 106
    - Желтоксан 59/3
    - Тимирязева 42/6
    - Медео
    
    Время работы на всех точках с 8:00 до 00:00,
    Кроме Медео где Мы угостим Вас чашкой ароматного кофе с 8:00 до 02:00.""")


@dp.callback_query_handler(lambda call: call.data == "make_claim")
async def report(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, """Какое замечание Вы хотите сделать?""", reply_markup=types_menu)
    await MakeClaim.type.set()


@dp.callback_query_handler(state=MakeClaim.type)
async def report(call: CallbackQuery, state: FSMContext):
    await call.bot.send_message(call.from_user.id, f"Выберите заведение", reply_markup=places_menu)
    await state.update_data(type=call.data)
    await MakeClaim.place.set()


@dp.callback_query_handler(state=MakeClaim.place)
async def report(call: CallbackQuery, state: FSMContext):
    await call.bot.send_message(call.from_user.id, f"Можно узнать Ваше имя?")
    await state.update_data(place=call.data)
    await MakeClaim.name.set()


@dp.message_handler(state=MakeClaim.name)
async def report(mes: Message, state: FSMContext):
    k = types.ReplyKeyboardMarkup(resize_keyboard=True)
    k.add(types.KeyboardButton("Отправить контакт", request_contact=True))

    await mes.answer("Напишите Ваш номер телефона или нажмите \"Отправить контакт\"", reply_markup=k)

    await state.update_data(name=mes.text)

    await MakeClaim.phone.set()


@dp.message_handler(state=MakeClaim.phone, content_types=['text', 'contact'])
async def report(mes: Message, state: FSMContext):
    if mes.contact is not None:
        try:
            num = phonenumbers.parse(mes.contact.phone_number, "KZ")
        except:
            await mes.answer('Неверный номер или формат')
            return

        if (phonenumbers.is_valid_number(num)):

            await state.update_data(phone=mes.contact.phone_number)
        else:
            await mes.answer('Неверный номер или формат')
            return

    else:
        try:
            num = phonenumbers.parse(mes.text, "KZ")
        except:
            await mes.answer('Неверный номер или формат')
            return

        if (phonenumbers.is_valid_number(num)):

            await state.update_data(phone=mes.text)

        else:
            await mes.answer('Неверный номер или формат')
            return

    await mes.answer("Опишите свою претензию и ситуацию", reply_markup=types.ReplyKeyboardRemove())
    await MakeClaim.text.set()


@dp.message_handler(state=MakeClaim.text)
async def report(mes: Message, state: FSMContext):
    await state.update_data(text=mes.text)

    k = types.InlineKeyboardMarkup()
    k.add(types.InlineKeyboardButton("Нет", callback_data='no'))
    k.add(types.InlineKeyboardButton("Да", callback_data='yes'))

    await mes.answer("Хотите оставить фото?", reply_markup=k)

    await MakeClaim.photo.set()


@dp.callback_query_handler(state=MakeClaim.photo)
async def report(call: CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        await call.bot.send_message(call.from_user.id, "Отправьте фото")
    else:
        pass


@dp.message_handler(content_types=['photo'], state=MakeClaim.photo)
async def report(mes: Message, state: FSMContext):
    if len(mes.photo) != 0:

        print(mes.photo[-1].file_id)
        await state.update_data(photo=mes.photo[-1].file_id)

        data = await state.get_data()

        k = types.InlineKeyboardMarkup()

        k.add(types.InlineKeyboardButton("Нет", callback_data='no'))
        k.add(types.InlineKeyboardButton("Да", callback_data='yes'))

        await mes.answer(
            f"""Подтвердите ваши данные:
    Тип: {get_type_name(data.get('type'))}
    Заведение: {get_place_name(data.get('place'))}
    Имя: {data.get('name')},
    Телефон: {data.get('phone')},
    Текст: {data.get('text')}""",
reply_markup=k)

    else:
        await mes.answer("Отправьте фото")
        return






@dp.callback_query_handler(lambda call: call.data == "make_request")
async def request(call: CallbackQuery):
    pass


if __name__ == "__main__":
    executor.start_polling(dp)
