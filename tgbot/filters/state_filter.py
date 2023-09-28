from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Filter


class StateFilter(Filter):
    key = "search"

    async def check(self, message: types.Message, state: FSMContext):
        print(await state.get_state())
