from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllChatAdministrators
from aiogram import Bot

async def set_command(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы, внесение в базу данных, изменение никнейма в базе данных'
        ),
        BotCommand(
            command='help',
            description='Список всех команд бота'
        )
    ]
    admin_commands = [
        BotCommand(
            command='ban',
            description='Забанить пользователя'
        ),
        BotCommand(
            command='mute',
            description='Замутить пользователя'
        ),
        BotCommand(
            command='auid',
            description='Добавить пользователей в БД'
        ),
        BotCommand(
            command='start',
            description='Начало работы, внесение в базу данных, изменение никнейма в базе данных'
        ),
        BotCommand(
            command='help',
            description='Список всех команд бота'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
    await bot.set_my_commands(admin_commands, BotCommandScopeAllChatAdministrators())
