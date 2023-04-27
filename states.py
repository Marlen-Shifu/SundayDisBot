from aiogram.dispatcher.filters.state import State, StatesGroup


class Menu(StatesGroup):
    place = State()


class MakeClaim(StatesGroup):
    type = State()
    place = State()
    sub_type = State()
    name = State()
    phone = State()
    text = State()
    photo = State()
    confirm = State()


class MakeRequest(StatesGroup):
    type = State()
    sub_type = State()
    place = State()
    text = State()
    confirm = State()
