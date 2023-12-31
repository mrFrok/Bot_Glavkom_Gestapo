import asyncio
import logging
import config
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import handlers
from handlers import commands
import datetime
import apsched

bot = Bot(token=config.TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

"""
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(apsched.send_remind, 'interval', seconds=10, kwargs={'bot': bot})

scheduler.start()
asyncio.get_event_loop().run_forever()
"""

#Главная функция
async def main():
    # Регистрация роутеров
    dp.include_routers(handlers.admin_actions.router, handlers.database_actions.router,
                       handlers.personal_actions.router)
    await commands.set_command(bot)

    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Запуск бота
if __name__ == "__main__":
    # Включение логов
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Асинхронный запуск бота
    asyncio.run(main())

