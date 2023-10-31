from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "start"),
            types.BotCommand("settings", "settings"),
            types.BotCommand("bonus", "bonus"),
            types.BotCommand("search", "search"),
            types.BotCommand("catalog", "catalog"),
        ]
    )
