from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMenuState(StatesGroup):
    get_menu = State()


class UserStartState(StatesGroup):
    get_lang = State()
    get_name = State()
    get_contact = State()
    get_code = State()
    get_role = State()


class UserSettings(StatesGroup):
    choose = State()
    get_lang = State()
    get_contact = State()
    get_code = State()


class UserFeedback(StatesGroup):
    get_feedback = State()


class UserBuyState(StatesGroup):
    get_cat = State()
    get_prod = State()
    get_conf = State()


class UserSearch(StatesGroup):
    get_name = State()
