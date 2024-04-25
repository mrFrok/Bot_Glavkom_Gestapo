import db
from aiogram import Bot

async def send_remind(bot: Bot):
    users = db.get_reminders()
    for userid in users:
        await bot.send_message(userid, f'Ежедневная рассылка.\nНе забудьте прописать команду !хуй')
