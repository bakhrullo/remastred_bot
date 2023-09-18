from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.db.db_api import get_user, create_user


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: types.User):
        redis = data['redis']
        user_cache = await redis.get(user.id)
        if user_cache:
            return data.update({'status': "cached", 'lang': user_cache['lang']})
        user_loc = await get_user(user.id, data['config'])
        if 'detail' in user_loc:
            await create_user(user.id, user.language_code, data['config'])
            data.update({'status': "created", 'lang': user.language_code})
        else:
            data['user'] = user_loc
            data.update({'status': "found", 'lang': user_loc['lang']})

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.from_user)
