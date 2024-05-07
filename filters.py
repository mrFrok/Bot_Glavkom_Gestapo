from aiogram import types
from aiogram.filters import BaseFilter, IS_ADMIN


class IsAdminFilter(BaseFilter):
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def __call__(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return IS_ADMIN.check(member=member)
