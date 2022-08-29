import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from handlers.commands import register_commands
from handlers.callbacks import register_callbacks
from handlers.register import register_state_callbacks
from handlers.inline import register_inline
from apps.database import create_tables
import config


async def set_commands(dp: Dispatcher):
    """ set up commands for menu"""
    bot_commands = [
        BotCommand(command="add", description="add a wallet"),
        BotCommand(command="list", description="list of all addresses"),
        BotCommand(command="wallets", description="edit my wallets"),
        BotCommand(command="clear", description="delete all data"),
        BotCommand(command="help", description="help")
    ]
    await dp.bot.set_my_commands(bot_commands)


async def main():
    bot = Bot(config.bot_token)
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    await create_tables()
    await set_commands(dp)
    register_commands(dp)
    register_callbacks(dp)
    register_state_callbacks(dp)
    register_inline(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
