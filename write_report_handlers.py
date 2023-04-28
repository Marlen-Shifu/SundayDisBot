import phonenumbers
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import dp, main_menu
from config import ADMIN_ID
from states import MakeClaim
from utils import get_type_name, get_place_name, places_menu, types_menu, sub_types_menu, get_sub_type_name


@dp.callback_query_handler(lambda call: call.data == "make_claim", state='*')
async def report(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    place = data.get('place')

    await call.bot.send_message(call.from_user.id, """Какое замечание Вы хотите сделать?""", reply_markup=types_menu)

    await MakeClaim.type.set()

    await Dispatcher.get_current().current_state().update_data(place=place)


# @dp.callback_query_handler(state=MakeClaim.type)
# async def report(call: CallbackQuery, state: FSMContext):
#     await call.bot.send_message(call.from_user.id, f"Выберите заведение", reply_markup=places_menu)
#     await state.update_data(type=call.data)
#     await MakeClaim.place.set()

# @dp.callback_query_handler(state=MakeClaim.type)
# async def report(call: CallbackQuery, state: FSMContext):
#     await state.update_data(type=call.data)
#
#     await call.bot.send_message(call.from_user.id, """Что именно вы хотите?""", reply_markup=sub_types_menu)
#
#     await MakeClaim.sub_type.set()


@dp.callback_query_handler(state=MakeClaim.type)
async def report(call: CallbackQuery, state: FSMContext):
    await call.bot.send_message(call.from_user.id, f"Можно узнать Ваше имя?")
    await state.update_data(type=call.data)
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

    data = await state.get_data()
    type = data.get('type')

    if type == 'bar_kitchen':

        k = types.InlineKeyboardMarkup()
        k.add(types.InlineKeyboardButton("Нет", callback_data='no'))
        k.add(types.InlineKeyboardButton("Да", callback_data='yes'))

        await mes.answer("Хотите оставить фото?", reply_markup=k)

        await MakeClaim.photo.set()

    else:
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
                                Текст: {data.get('text')}""", reply_markup=k)

        await MakeClaim.confirm.set()


@dp.callback_query_handler(state=MakeClaim.photo)
async def report(call: CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        await call.bot.send_message(call.from_user.id, "Отправьте фото")
    else:
        data = await state.get_data()

        k = types.InlineKeyboardMarkup()

        k.add(types.InlineKeyboardButton("Нет", callback_data='no'))
        k.add(types.InlineKeyboardButton("Да", callback_data='yes'))

        await call.bot.send_message(call.from_user.id,
                                    f"""Подтвердите ваши данные:
                                Тип: {get_type_name(data.get('type'))}
                                Заведение: {get_place_name(data.get('place'))}
                                Имя: {data.get('name')},
                                Телефон: {data.get('phone')},
                                Текст: {data.get('text')}""", reply_markup=k)

        await MakeClaim.confirm.set()


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
                                Текст: {data.get('text')}""", reply_markup=k)

        await MakeClaim.confirm.set()

    else:
        await mes.answer("Отправьте фото")
        return


@dp.callback_query_handler(state=MakeClaim.confirm)
async def report(call: CallbackQuery, state: FSMContext):
    if call.data == 'no':
        await call.bot.send_message(call.from_user.id, "Главное меню", reply_markup=places_menu)

    elif call.data == 'yes':

        data = await state.get_data()

        user_telegram = f"@{call.from_user.username}" if call.from_user.username is not None else "Недоступен"


        await call.bot.send_message(ADMIN_ID,
            f"""Поступила новая жалоба:
                                Тип: {get_type_name(data.get('type'))}
                                Заведение: {get_place_name(data.get('place'))}
                                Имя: {data.get('name')},
                                Телефон: {data.get('phone')},
                                Текст: {data.get('text')},
                                Телеграм: {user_telegram}""")


        try:
            await call.bot.send_photo(ADMIN_ID, data.get('photo'))
        except:
            await call.bot.send_message(ADMIN_ID, "Нету фото")

        await call.bot.send_message(call.from_user.id, "Спасибо за Вашу реакцию, с Вами свяжутся, что-то еще?", reply_markup=places_menu)

    await state.finish()
