from aiogram import types, Router, F
from aiogram.types import chat_permissions, Message
from aiogram.filters import Command, IS_ADMIN, ChatMemberUpdatedFilter
import time
import config
from filters import IsAdminFilter
from db import new_varn_user, get_varn_users, update_varn_user, get_top_varn_users, delete_varn_user, add_user, \
    get_user_from_name, add_user_if_not_exists, get_user_from_username, get_user
import re
from bot import bot, dp

router = Router()


@router.message(IsAdminFilter(is_admin=True),
                Command("ban", "бан", prefix="!/"))
async def ban(message: types.Message):
    name1 = message.from_user.mention_html()
    if not message.reply_to_message:
        mention = re.search(r'@(\w+)', message.text)
        if mention:
            muteid1 = get_user_from_username(mention.group(1))
            if muteid1 != None:
                try:
                    muteid = get_user_from_username(mention.group(1))[0]
                    muteint = int(message.text.split()[2])
                    mutetype = message.text.split()[3]
                    comment = " ".join(message.text.split()[4:])
                except:
                    try:
                        mutetype = message.text.split()[1]
                        comment = " ".join(message.text.split()[2:])
                    except:
                        await message.reply(
                            '   Не правильно написано!\nНапример:\n`/мут 1 ч причина \n /мут 1 м причина \n /мут 1 д причина \n /мут 1 г причина \n /мут навсегда причина`')
                        return
                    if mutetype == "infinity" or mutetype == "навсегда":
                        await bot.ban_chat_member(message.chat.id, muteid)
                        try:
                            await message.delete()
                        except:
                            pass
                        await bot.send_message(message.chat.id,
                                               f' | <b>Решение выдать бан было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> {mutetype}\n | <b>Причина:</b> {comment}',
                                               parse_mode='html')
                    else:
                        await message.reply(
                            'Не правильно написано!\nНапример:\n`/мут 1 ч причина \n /мут 1 м причина \n /мут 1 д причина \n /мут 1 г причина \n /мут навсегда причина`')
                        return

                if mutetype == "ч" or mutetype == "часов" or mutetype == "h":
                    await bot.ban_chat_member(message.chat.id, muteid,
                                              until_date=int(time.time()) + muteint * 3600)
                    try:
                        await message.delete()
                    except:
                        pass
                    await message.answer(
                        f' | <b>Решение выдать бан было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                        parse_mode='html')
                elif mutetype == "м" or mutetype == "минут" or mutetype == "m":
                    await bot.ban_chat_member(message.chat.id, muteid,
                                              until_date=int(time.time()) + muteint * 60)
                    try:
                        await message.delete()
                    except:
                        pass
                    await message.answer(
                        f' | <b>Решение выдать бан было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                        parse_mode='html')
                elif mutetype == "д" or mutetype == "дней" or mutetype == "d":
                    await bot.ban_chat_member(message.chat.id, muteid,
                                              until_date=int(time.time()) + muteint * 86400)
                    try:
                        await message.delete()
                    except:
                        pass
                    await message.answer(
                        f' | <b>Решение выдать бан было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                        parse_mode='html')
                elif mutetype == "г" or mutetype == "год" or mutetype == "y" or mutetype == "л" or mutetype == "лет":
                    await bot.ban_chat_member(message.chat.id, muteid,
                                              until_date=int(time.time()) + muteint * 31536000)
                    try:
                        await message.delete()
                    except:
                        pass
                    await message.answer(
                        f' | <b>Решение выдать бан было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                        parse_mode='html')
    try:
        user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        if user.status.ADMINISTRATOR():
            await message.reply('Нельзя заблокировать админа')
            return
    except:
        pass
    try:
        muteint = int(message.text.split()[1])
        mutetype = message.text.split()[2]
        comment = " ".join(message.text.split()[3:])
    except:
        try:
            mutetype = message.text.split()[1]
            comment = " ".join(message.text.split()[2:])
        except:
            await message.reply(
                'Не правильно написано!\nНапример:\n`/бан 1 м причина \n /бан 1 ч причина \n /бан 1 д причина \n /бан 1 г причина \n /бан навсегда причина `')
        if mutetype == "infinity" or mutetype == "навсегда":
            await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            try:
                await message.delete()
            except:
                pass
            await message.answer(
                f' | <b>Решение выдать бан было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> {mutetype}\n | <b>Причина:</b> {comment}',
                parse_mode='html')
        else:
            await message.reply(
                'Не правильно написано!\nНапример:\n`/бан 1 м причина \n /бан 1 ч причина \n /бан 1 д причина \n /бан 1 г причина \n /бан навсегда причина `')
            return
    if mutetype == "ч" or mutetype == "часов" or mutetype == "h":
        await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                  until_date=int(time.time()) + muteint * 3600)
        try:
            await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            await message.delete()
        except:
            pass
        await message.answer(
            f' | <b>Решение выдать бан было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
            parse_mode='html')
    elif mutetype == "м" or mutetype == "минут" or mutetype == "m":
        await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                  until_date=int(time.time()) + muteint * 60)
        try:
            await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            await message.delete()
        except:
            pass
        await message.answer(
            f' | <b>Решение выдать бан было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
            parse_mode='html')
    elif mutetype == "д" or mutetype == "дней" or mutetype == "d":
        await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                  until_date=int(time.time()) + muteint * 86400)
        try:
            await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            await message.delete()
        except:
            pass
        await message.answer(
            f' | <b>Решение выдать бан было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
            parse_mode='html')
    elif mutetype == "г" or mutetype == "год" or mutetype == "y" or mutetype == "л" or mutetype == "лет":
        await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                  until_date=int(time.time()) + muteint * 31536000)
        try:
            await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            await message.delete()
        except:
            pass
        await message.answer(
            f' | <b>Решение выдать бан было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
            parse_mode='html')


@router.message(IsAdminFilter(is_admin=True), Command("unban", "разбан", 'Unban', 'Разбан', prefix="!/"))
async def unban(message: types.Message):
    banner = message.from_user.mention_html()
    if not message.reply_to_message:
        mention = re.search(r'@(\w+)', message.text)
        if mention:
            muteid1 = get_user_from_username(mention.group(1))
            if muteid1 == None:
                await message.answer('Этого пользователя нет в базе данных!')
            else:
                mutename = get_user(muteid1[0])
                await message.delete()
                await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=muteid1[0])
                await message.answer(
                    f'Пользователь <a href="tg://user?id={muteid1}">{mutename[2]}</a> разбанен админом {banner}',
                    parse_mode='html')

    await message.delete()
    await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)

    await message.answer(
        f'Пользователь <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> разбанен админом {banner}',
        parse_mode='html')


@router.message(IsAdminFilter(is_admin=True), Command("mute", "мут", "Мут", "Mute", prefix="!/"))
async def mute(message: types.Message):
    name1 = message.from_user.mention_html()
    if not message.reply_to_message:
        mention = re.search(r'@(\w+)', message.text)
        if mention:
            muteid1 = get_user_from_username(mention.group(1))
            if muteid1 != None:
                try:
                    muteid = get_user_from_username(mention.group(1))[0]
                    muteint = int(message.text.split()[2])
                    mutetype = message.text.split()[3]
                    comment = " ".join(message.text.split()[4:])
                except:
                    try:
                        mutetype = message.text.split()[1]
                        comment = " ".join(message.text.split()[2:])
                    except:
                        await message.reply(
                            '   Не правильно написано!\nНапример:\n`/мут 1 ч причина \n /мут 1 м причина \n /мут 1 д причина \n /мут 1 г причина \n /мут навсегда причина`')
                        return
                    if mutetype == "infinity" or mutetype == "навсегда":
                        await bot.restrict_chat_member(message.chat.id, muteid,
                                                       can_send_messages=False,
                                                       can_send_media_messages=False, can_send_other_messages=False,
                                                       can_add_web_page_previews=False)
                        try:
                            await message.delete()
                        except:
                            pass
                        await bot.send_message(message.chat.id,
                                               f' | <b>Решение выдать мут было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> {mutetype}\n | <b>Причина:</b> {comment}',
                                               parse_mode='html')
                    else:
                        await message.reply(
                            'Не правильно написано!\nНапример:\n`/мут 1 ч причина \n /мут 1 м причина \n /мут 1 д причина \n /мут 1 г причина \n /мут навсегда причина`')
                        return
                if mutetype == "ч" or mutetype == "часов" or mutetype == "h":
                    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=muteid,
                                                   until_date=int(time.time()) + muteint * 3600,
                                                   permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                                can_send_polls=False,
                                                                                                can_send_other_messages=False,
                                                                                                can_send_media_messages=False))
                    await message.bot.send_message(message.chat.id,
                                                   f' | <b>Решение выдать мут было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                                                   parse_mode='html')
                    await message.delete()

                elif mutetype == "м" or mutetype == "минут" or mutetype == "m":
                    await bot.restrict_chat_member(message.chat.id, muteid,
                                                   until_date=int(time.time()) + muteint * 60,
                                                   permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                                can_send_polls=False,
                                                                                                can_send_other_messages=False,
                                                                                                can_send_media_messages=False))
                    await message.delete()
                    await message.answer(
                        f' | <b>Решение выдать мут было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                        parse_mode='html')

                elif mutetype == "д" or mutetype == "дней" or mutetype == "d":
                    await bot.restrict_chat_member(message.chat.id, muteid,
                                                   until_date=int(time.time()) + muteint * 86400,
                                                   permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                                can_send_polls=False,
                                                                                                can_send_other_messages=False,
                                                                                                can_send_media_messages=False))
                    await message.delete()
                    await message.answer(
                        f' | <b>Решение выдать мут было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                        parse_mode='html')

                elif mutetype == "г" or mutetype == "год" or mutetype == "y" or mutetype == "л" or mutetype == "лет":
                    await bot.restrict_chat_member(message.chat.id, muteid,
                                                   until_date=int(time.time()) + muteint * 31536000,
                                                   permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                                can_send_polls=False,
                                                                                                can_send_other_messages=False,
                                                                                                can_send_media_messages=False))
                    await message.delete()
                    await message.answer(
                        f' | <b>Решение выдать мут было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                        parse_mode='html')
            else:
                await message.reply('Пользователя нет в базе данных, используйте ответ на сообщение пользователя')
        else:
            await message.reply(
                'Не правильно написано!\nНапример:\n`/мут 1 ч причина \n /мут 1 м причина \n /мут 1 д причина \n /мут 1 г причина \n /мут навсегда причина`')
            return
    try:
        user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        if user.status == 'ADMINISTRATOR':
            await message.reply('Нельзя заблокировать админа')
            return
    except:
        pass
    else:
        try:
            muteint = int(message.text.split()[1])
            mutetype = message.text.split()[2]
            comment = " ".join(message.text.split()[3:])
        except:
            try:
                mutetype = message.text.split()[1]
                comment = " ".join(message.text.split()[2:])
            except:
                await message.reply(
                    '   Не правильно написано!\nНапример:\n`/мут 1 ч причина \n /мут 1 м причина \n /мут 1 д причина \n /мут 1 г причина \n /мут навсегда причина`')
                return
            if mutetype == "infinity" or mutetype == "навсегда":
                await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                               permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                            can_send_polls=False,
                                                                                            can_send_other_messages=False,
                                                                                            can_send_media_messages=False))
                try:
                    await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                    await message.delete()
                except:
                    pass
                await message.answer(
                    f' | <b>Решение выдать мут было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> {mutetype}\n | <b>Причина:</b> {comment}',
                    parse_mode='html')
            else:
                await message.reply(
                    '   Не правильно написано!\nНапример:\n`/мут 1 ч причина \n /мут 1 м причина \n /мут 1 д причина \n /мут 1 г причина \n /мут навсегда причина`')
                return
        if mutetype == "ч" or mutetype == "часов" or mutetype == "h":
            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                           until_date=int(time.time()) + muteint * 3600,
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                        can_send_polls=False,
                                                                                        can_send_other_messages=False,
                                                                                        can_send_media_messages=False))
            try:
                await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                await message.delete()
            except:
                pass
            await message.answer(
                f' | <b>Решение выдать мут было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                parse_mode='html')

        elif mutetype == "м" or mutetype == "минут" or mutetype == "m":
            await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                           until_date=int(time.time()) + muteint * 60,
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                        can_send_polls=False,
                                                                                        can_send_other_messages=False,
                                                                                        can_send_media_messages=False))

            await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            await message.delete()

            await message.answer(
                f' | <b>Решение выдать мут было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                parse_mode='html')

        elif mutetype == "д" or mutetype == "дней" or mutetype == "d":
            await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                           until_date=int(time.time()) + muteint * 86400,
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                        can_send_polls=False,
                                                                                        can_send_other_messages=False,
                                                                                        can_send_media_messages=False))
            try:
                await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                await message.delete()
            except:
                pass
            await message.answer(
                f' | <b>Решение выдать мут было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                parse_mode='html')

        elif mutetype == "г" or mutetype == "год" or mutetype == "y" or mutetype == "л" or mutetype == "лет":
            await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                           until_date=int(time.time()) + muteint * 31536000,
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                        can_send_polls=False,
                                                                                        can_send_other_messages=False,
                                                                                        can_send_media_messages=False))
            try:
                await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                await message.delete()
            except:
                pass
            await message.answer(
                f' | <b>Решение выдать мут было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
                parse_mode='html')


@router.message(IsAdminFilter(is_admin=True), Command("unmute", "размут", 'Unmute', 'Размут', prefix="!/"))
async def unmute(message):
    mutitel = message.from_user.mention_html()
    if not message.reply_to_message:
        mention = re.search(r'@(\w+)', message.text)
        if mention:
            muteid1 = get_user_from_username(mention.group(1))
            if muteid1 != None:
                try:
                    muteid = get_user_from_username(mention.group(1))[0]
                except:
                    await message.reply(f'Вы не указали пользователя')
                await message.bot.delete_message(message.chat.id, message.message_id)
                await message.bot.restrict_chat_member(chat_id=message.chat.id,
                                                       user_id=muteid,
                                                       permissions=chat_permissions.ChatPermissions(
                                                           can_send_messages=True,
                                                           can_send_polls=True,
                                                           can_send_other_messages=True,
                                                           can_send_media_messages=True,
                                                           can_invite_users=True,
                                                           can_add_web_page_previews=True))
                await message.answer(
                    f'Пользователю <a href="tg://user?id={muteid}">{mention.group(1)}</a> был снят мут админом {mutitel}',
                    parse_mode='html')
        else:
            await message.reply('Вы не указали пользователя!')
    else:
        await message.bot.delete_message(message.chat.id, message.message_id)
        await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                               permissions=chat_permissions.ChatPermissions(can_send_messages=True,
                                                                                            can_send_polls=True,
                                                                                            can_send_other_messages=True,
                                                                                            can_send_media_messages=True,
                                                                                            can_invite_users=True,
                                                                                            can_add_web_page_previews=True))

        await message.answer(
            f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был снят мут админом {mutitel}',
            parse_mode='html')


@router.message(F.new_chat_member)
async def new_members_handler(message: Message):
    new_member = message.new_chat_members[0]
    add_user_if_not_exists(new_member.id, new_member.full_name, new_member.username)
    await bot.send_message(message.chat.id,
                           f'Добро пожаловать, <a href="tg://user?id={new_member.id}">{new_member.full_name}</a>! Ты попал в лучшую группу, здесь рады всем! \n'
                           f"В этой группе ты можешь найти новых друзей, общаться с самыми лучшими, дружными и адекватными людьми со всего света \n"
                           f"С правилами ты можешь ознакомиться <a href = 'https://t.me/c/1817240369/239383/239387'>здесь</a> \n"
                           f"Так же у нас есть <a href = 'https://discord.gg/wWFxVGJsmQ'>Discord</a>\n"
                           f"Больше не буду задерживать, удачи!")


@router.message(IsAdminFilter(is_admin=True), Command('варн', 'Варн', 'Varn', 'varn', prefix="!/"))
async def varn(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    member_id = message.reply_to_message.from_user.id
    member_name = message.reply_to_message.from_user.full_name
    admin = message.from_user.mention_html()
    a = get_varn_users(member_id)
    if a is None:
        try:
            reason_a = message.text.split()[1]
            reason_a = message.text.split()[1:]
            reason = " ".join(reason_a)
            new_varn_user(member_id, member_name, 1, reason)
            await message.answer(
                f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был выдан варн админом {admin} по причине {reason}. Сейчас количество варнов у пользователя составляет {1}')
        except:
            new_varn_user(member_id, member_name, 1, 'Без причины')
            await message.answer(
                f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был выдан варн админом {admin}. Сейчас количество варнов у пользователя составляет {1}')
    else:
        if a[0] == 1:
            try:
                reason_a = message.text.split()[1:]
                reason = " ".join(reason_a)
                update_varn_user(member_id, 2, reason)
                await message.answer(
                    f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был выдан варн админом {admin} по причине {reason}. Сейчас количество варнов у пользователя составляет {2}')
            except:
                update_varn_user(member_id, 2, 'Без причины')
                await message.answer(
                    f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был выдан варн админом {admin}. Сейчас количество варнов у пользователя составляет {2}')

        elif a[0] >= 2:
            await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                      until_date=int(time.time()) + 7 * 86400)
            await message.answer(
                f' | <b>Решение выдать бан было принято:</b> {admin}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> 1 неделя\n | <b>Причина:</b> Нарушитель получил 3 варна',
                parse_mode='html')


@router.message(IsAdminFilter(is_admin=True), Command('Снять_варн', 'снять_варн', 'варн-', '-варн', prefix="!/"))
async def varn_minus(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    member_id = int(message.reply_to_message.from_user.id)
    member_name = message.reply_to_message.from_user.full_name
    admin = message.from_user.mention_html()
    a = get_varn_users(member_id)
    if a is None:
        await message.reply(f"У пользователя нет варнов")
    else:
        try:
            b = message.text.split()[1]
            if str(b) == 'все':
                delete_varn_user(member_id)
                await message.answer(
                    f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> были сняты все варны админом {admin}.')
            else:
                await message.answer(f'Нет такого аргумента как "{b}"')
        except IndexError:
            if a[0] == 1:
                delete_varn_user(member_id)
                await message.answer(
                    f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был снят один варн админом {admin}. Сейчас количество варнов у пользователя составляет {0}')
            elif a[0] == 2:
                update_varn_user(member_id, 1, None)
                await message.answer(
                    f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был снят один варн админом {admin}. Сейчас количество варнов у пользователя составляет {1}')


@router.message(IsAdminFilter(is_admin=True), Command('варнинфо', 'Варнинфо', 'Ви', 'ви', prefix="!/"))
async def varn_info(message: types.Message):
    varns_info = get_top_varn_users()
    response = 'Варны у участников:\n'
    for i, (userid, username, value_varns, reason) in enumerate(varns_info, start=1):
        response += f'{i}. <a href="tg://user?id={userid}">{username}</a> количество варнов -  {value_varns}, причина - {reason}\n'
    await message.answer(response)
