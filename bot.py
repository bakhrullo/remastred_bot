import asyncio
import logging

import aioredis
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.filters.back import BackFilter
from tgbot.filters.state_filter import StateFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.acl import ACLMiddleware
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.misc.bot_set_cmds import set_default_commands
from tgbot.misc.i18n import i18ns

logger = logging.getLogger(__name__)
DEBUG = True


def register_all_middlewares(dp, config, redis):
    dp.setup_middleware(EnvironmentMiddleware(config=config, redis=redis))
    dp.setup_middleware(ACLMiddleware())
    dp.setup_middleware(i18ns)


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(BackFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    if DEBUG:
        register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO if DEBUG else logging.WARNING,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    redis = aioredis.from_url("redis://localhost", decode_responses=True)
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    bot['redis'] = redis

    register_all_middlewares(dp, config, redis)
    register_all_filters(dp)
    register_all_handlers(dp)

#    await set_default_commands(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
