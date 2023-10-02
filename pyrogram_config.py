from pyrogram import Client
from config import TOKEN

api_id = 22369506
api_hash = "a8e4988c2e822f0395f807534d825bba"
bot_token = f"{TOKEN}"

async def get_chat_members_id(chat_id):
    app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    chat_members_id = []  # Используем список для сохранения id пользователей
    await app.start()
    async for member in app.get_chat_members(chat_id):
        chat_members_id.append(member.user.id)  # Используем .append() для добавления id в список
    await app.stop()
    return chat_members_id

async def get_chat_members_name(chat_id):
    app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    chat_members_name = []  # Используем список для сохранения имен пользователей
    await app.start()
    async for member in app.get_chat_members(chat_id):
        chat_members_name.append(member.user.first_name)  # Используем .append() для добавления имени в список
    await app.stop()
    return chat_members_name

async def get_chat_members_username(chat_id):
    app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    chat_members_name = []  # Используем список для сохранения имен пользователей
    await app.start()
    async for member in app.get_chat_members(chat_id):
        chat_members_name.append(member.user.username)  # Используем .append() для добавления имени в список
    await app.stop()
    return chat_members_name


