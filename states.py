from aiogram.dispatcher.filters.state import State, StatesGroup


class MakeClaim(StatesGroup):
    type = State()
    place = State()
    name = State()
    phone = State()
    text = State()
    photo = State()
    confirm = State()


class MakeRequest(StatesGroup):
    type = State()
    place = State()
    text = State()
    confirm = State()