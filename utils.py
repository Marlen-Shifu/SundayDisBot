from aiogram import types

types_list = [
    {"text": "По бару и кухне(Можете приложить фото)", "callback_data": "bar_kitchen"},
    {"text": "Сервис", "callback_data": "service"},
    {"text": "Другое", "callback_data": "other"},
]

types_menu = types.InlineKeyboardMarkup()

for type in types_list:
    types_menu.add(types.InlineKeyboardButton(**type))

types_list_no_photo = [
    {"text": "По бару и кухне", "callback_data": "bar_kitchen"},
    {"text": "Сервис", "callback_data": "service"},
    {"text": "Другое", "callback_data": "other"},
]

types_menu_no_photo = types.InlineKeyboardMarkup()

for type in types_list_no_photo:
    types_menu_no_photo.add(types.InlineKeyboardButton(**type))

places_list = [
    {"text": "Абая 17", "callback_data": "abay_17"},
    {"text": "Орбита 3, 5Е", "callback_data": "orbita_3"},
    {"text": "Тимирязева 38Б", "callback_data": "timiryazeva_38"},
    {"text": "Жибек жолы 106", "callback_data": "zhibek_106"},
    {"text": "Желтоксан 59 / 3", "callback_data": "zheltoksan_59"},
    {"text": "Тимирязева 42 / 6", "callback_data": "timiryazeva_42"},
    {"text": "Медео", "callback_data": "medeo"},
]

places_menu = types.InlineKeyboardMarkup()

for place in places_list:
    places_menu.add(types.InlineKeyboardButton(**place))


sub_types_list = [
    {"text": "Изменить состав", "callback_data": "compound"},
    {"text": "Изменить подачу", "callback_data": "feeding"},
    {"text": "Добавить пункт в меню", "callback_data": "menu"},
    {"text": "Другое", "callback_data": "other"},
]

sub_types_menu = types.InlineKeyboardMarkup()

for sub_type in sub_types_list:
    sub_types_menu.add(types.InlineKeyboardButton(**sub_type))


def get_type_name(data):
    return get_name(types_list, data)


def get_type_name_no_photo(data):
    return get_name(types_list_no_photo, data)


def get_place_name(data):
    return get_name(places_list, data)


def get_sub_type_name(data):
    return get_name(sub_types_list, data)


def get_name(list, data):
    for i in list:
        if i.get("callback_data") == data:
            return i.get("text")
    return None
