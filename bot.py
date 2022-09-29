import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tg_bot.config import load_config
from tg_bot.filters.admin import AdminFilter

from tg_bot.models.db_model import DBModel

from tg_bot.handlers.admin.register_handlers import register_handlers_admin
from tg_bot.handlers.user.register_handlers import register_handlers_user


logger = logging.getLogger(__name__)


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher):
    register_handlers_admin(dp)
    register_handlers_user(dp)


async def telegram_bot():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config("bot.ini")
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config
    bot['db'] = DBModel(config.db.path)

    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(telegram_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
