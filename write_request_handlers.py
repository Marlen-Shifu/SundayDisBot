import phonenumbers
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import dp, main_menu
from config import ADMIN_ID
from states import MakeRequest
from utils import get_type_name, get_place_name, places_menu, types_menu, types_menu_no_photo, get_type_name_no_photo


@dp.callback_query_handler(lambda call: call.data == "make_request")
async def request(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, """Какое предложение Вы хотите сделать?""", reply_markup=types_menu_no_photo)
    await MakeRequest.type.set()


@dp.callback_query_handler(state=MakeRequest.type)
async def request(call: CallbackQuery, state: FSMContext):
    await call.bot.send_message(call.from_user.id, f"Выберите заведение", reply_markup=places_menu)
    await state.update_data(type=call.data)
    await MakeRequest.place.set()


@dp.callback_query_handler(state=MakeRequest.place)
async def request(call: CallbackQuery, state: FSMContext):
    await call.bot.send_message(call.from_user.id, f"Опишите Ваше предложение")
    await state.update_data(place=call.data)
    await MakeRequest.text.set()


@dp.message_handler(state=MakeRequest.text)
async def request(mes: Message, state: FSMContext):
    await state.update_data(text=mes.text)

    data = await state.get_data()

    k = types.InlineKeyboardMarkup()

    k.add(types.InlineKeyboardButton("Нет", callback_data='no'))
    k.add(types.InlineKeyboardButton("Да", callback_data='yes'))

    await mes.answer(
            f"""Подтвердите ваши данные:
            Тип: {get_type_name_no_photo(data.get('type'))}
            Заведение: {get_place_name(data.get('place'))}
            Текст: {data.get('text')}""", reply_markup=k)

    await MakeRequest.confirm.set()


@dp.callback_query_handler(state=MakeRequest.confirm)
async def request(call: CallbackQuery, state: FSMContext):
    if call.data == 'no':
        await call.bot.send_message(call.from_user.id, "Главное меню", reply_markup=main_menu)

    elif call.data == 'yes':

        data = await state.get_data()

        await call.bot.send_message(ADMIN_ID,
            f"""Новое предложение:
            Тип: {get_type_name_no_photo(data.get('type'))}
            Заведение: {get_place_name(data.get('place'))}
            Текст: {data.get('text')}""")\


        await call.bot.send_message(call.from_user.id, "Спасибо за Ваше предложение, оно очень важно нам, что-то еще?", reply_markup=main_menu)

    await state.finish()
