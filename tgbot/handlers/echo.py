from aiogram import types, Dispatchercd

from tgbot.misc.i18n import i18ns

_ = i18ns.gettext
__ = i18ns.lazy_gettext


async def bot_echo(message: types.Message):
    await message.answer(_("/start tugmasini bosing!"))


async def bot_echo_all(message: types.Message):
    await message.answer(_("/start tugmasini bosing!"))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
