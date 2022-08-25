import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.commands import register_commands
from handlers.callbacks import register_callbacks
from handlers.register import register_state_callbacks
from handlers.inline import register_inline

import config


async def main():
    bot = Bot(config.bot_token)
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    register_commands(dp)
    register_callbacks(dp)
    register_state_callbacks(dp)
    register_inline(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
