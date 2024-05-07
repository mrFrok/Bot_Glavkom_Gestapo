import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
import config
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import handlers
from handlers import commands
from aiogram.fsm.storage.memory import MemoryStorage
from db import get_reminders, update_send_remind
import datetime


# Инициализация
bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


# Главная функция
async def main():
    # Регистрация роутеров
    dp.include_routers(handlers.admin_actions.router, handlers.database_actions.router,
                       handlers.personal_actions.router)
    await commands.set_command(bot)

    await on_startup_launch()

    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def send_reminders():
    while True:
        subscribers = get_reminders()
        for subscriber in subscribers:
            if datetime.datetime.now() - datetime.datetime.strptime(subscriber[1],
                                                                    '%Y-%m-%d %H:%M') > datetime.timedelta(
                    hours=24):
                if subscriber[2] == 0:
                    await bot.send_message(subscriber[0], f'Ежедневная рассылка! Не забудьте прописать !работать в чате(Вы это уже можете!)')
                    update_send_remind(subscriber[0])
        await asyncio.sleep(60)


async def on_startup_launch():
    asyncio.create_task(send_reminders())


# Запуск бота
if __name__ == "__main__":
    # Включение логов
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Асинхронный запуск бота
    asyncio.run(main())
