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


class UserBonus(StatesGroup):
    get_brock = State()
    get_region = State()


class UserFeedback(StatesGroup):
    get_feedback = State()


class UserCatalogState(StatesGroup):
    get_glob_cat = State()
    get_cat = State()
    get_sub_cat = State()
    get_prod = State()
    get_analog = State()


class UserSearch(StatesGroup):
    get_name = State()
