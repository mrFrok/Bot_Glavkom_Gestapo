from pyrogram import Client
from config import TOKEN

api_id = 22369506
api_hash = "a8e4988c2e822f0395f807534d825bba"
bot_token = f"{TOKEN}"

async def get_chat_members(chat_id):
    app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    chat_members = []
    await app.start()
    async for member in app.get_chat_members(chat_id):
        chat_members.append((member.user.id, member.user.first_name, member.user.username))
    await app.stop()
    return chat_members
