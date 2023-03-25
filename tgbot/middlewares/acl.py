from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.db.db_api import get_user


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: types.User):
        user_loc = await get_user(user.id, data['config'])
        data['status'] = False if 'detail' in user_loc else True
        data['lang'] = 'uz' if 'detail' in user_loc else user_loc['lang']

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.from_user)
