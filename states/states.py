from aiogram.dispatcher.filters.state import State, StatesGroup

class ADD_CHANEL(StatesGroup):
    link = State()
    price = State()
    category = State()

class DEL_CHANEL(StatesGroup):
    chanel_id = State()

class EDIT_PRICE(StatesGroup):
    chanel_id = State()
    price = State()

class FSM_ADMIN_SPAM(StatesGroup):
    text = State()
    btns = State()
