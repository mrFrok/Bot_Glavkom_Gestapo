import datetime
from aiogram import types, Router
from aiogram.types import chat_permissions
from aiogram.filters import Command
import time
from filters import IsAdminFilter
from db import new_varn_user, get_varn_users, update_varn_user, get_top_varn_users, delete_varn_user, add_user, \
    get_user_from_name, add_user_if_not_exists, get_user_from_username, get_user, add_restricts, delete_restricts_user
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
                        name = get_user(muteid)[3]
                        add_restricts(muteid, mention.group(1), name, comment, 'ban', datetime.datetime.now())
                    else:
                        await message.reply(
                            'Не правильно написано!\nНапример:\n`/мут 1 ч причина \n /мут 1 м причина \n /мут 1 д причина \n /мут 1 г причина \n /мут навсегда причина`')
                        return

                if mutetype == "ч" or mutetype == "часов" or mutetype == "h":
                    await bot.ban_chat_member(message.chat.id, muteid,
                                              until_date=int(time.time()) + muteint * 3600)
                    name = get_user(muteid)[3]
                    add_restricts(muteid, mention.group(1), name, comment, 'ban', datetime.datetime.now())
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
                    name = get_user(muteid)[3]
                    add_restricts(muteid, mention.group(1), name, comment, 'ban', datetime.datetime.now())
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
                    name = get_user(muteid)[3]
                    add_restricts(muteid, mention.group(1), name, comment, 'ban', datetime.datetime.now())
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
            name = get_user(message.reply_to_message.from_user.id)[3]
            add_restricts(message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, name,
                          comment, 'ban', datetime.datetime.now())
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
        name = get_user(message.reply_to_message.from_user.id)[3]
        add_restricts(message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, name, comment, 'ban', datetime.datetime.now())
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
        name = get_user(message.reply_to_message.from_user.id)[3]
        add_restricts(message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, name, comment, 'ban', datetime.datetime.now())
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
        name = get_user(message.reply_to_message.from_user.id)[3]
        add_restricts(message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, name, comment, 'ban', datetime.datetime.now())
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
        name = get_user(message.reply_to_message.from_user.id)[3]
        add_restricts(message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, name, comment, 'ban', datetime.datetime.now())
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
                delete_restricts_user(muteid1[0])
                await message.answer(
                    f'Пользователь <a href="tg://user?id={muteid1}">{mutename[2]}</a> разбанен админом {banner}',
                    parse_mode='html')

    await message.delete()
    await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    delete_restricts_user(message.reply_to_message.from_user.id)

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
                        name = get_user(muteid)[3]
                        add_restricts(muteid, mention.group(1), name, comment, 'mute', datetime.datetime.now())
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
                    name = get_user(muteid)[3]
                    add_restricts(muteid, mention.group(1), name, comment, 'mute', datetime.datetime.now())
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
                    name = get_user(muteid)[3]
                    add_restricts(muteid, mention.group(1), name, comment, 'mute', datetime.datetime.now())
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
                    name = get_user(muteid)[3]
                    add_restricts(muteid, mention.group(1), name, comment, 'mute', datetime.datetime.now())
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
                    name = get_user(muteid)[3]
                    add_restricts(muteid, mention.group(1), name, comment, 'mute', datetime.datetime.now())
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
                name = get_user(message.reply_to_message.from_user.id)[3]
                add_restricts(message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, name, comment, 'mute', datetime.datetime.now())
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
            name = get_user(message.reply_to_message.from_user.id)[3]
            add_restricts(message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, name,
                          comment, 'mute', datetime.datetime.now())
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
            name = get_user(message.reply_to_message.from_user.id)[3]
            add_restricts(message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, name,
                          comment, 'mute', datetime.datetime.now())

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
            name = get_user(message.reply_to_message.from_user.id)[3]
            add_restricts(message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, name,
                          comment, 'mute', datetime.datetime.now())
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
            name = get_user(message.reply_to_message.from_user.id)[3]
            add_restricts(message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, name,
                          comment, 'mute', datetime.datetime.now())
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
                    return
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
                delete_restricts_user(muteid)
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
        delete_restricts_user(message.reply_to_message.from_user.id)

        await message.answer(
            f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был снят мут админом {mutitel}',
            parse_mode='html')


@router.message(IsAdminFilter(is_admin=True), Command('варн', 'Варн', 'Varn', 'varn', prefix="!/"))
async def varn(message: types.Message):
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
                admin = message.from_user.mention_html()
                a = get_varn_users(muteid)
                if a is None:
                    try:
                        reason_a = message.text.split()[2]
                        reason_a = message.text.split()[2:]
                        reason = " ".join(reason_a)
                        new_varn_user(muteid, mention.group(1), 1, reason, datetime.datetime.now())
                        await message.answer(
                            f'Пользователю <a href="tg://user?id={muteid}">{mention.group(1)}</a> был выдан варн админом {admin} по причине {reason}. \nСейчас количество варнов у пользователя составляет {1}')
                        return
                    except:
                        new_varn_user(muteid, mention.group(1), 1, 'Без причины', datetime.datetime.now())
                        await message.answer(
                            f'Пользователю <a href="tg://user?id={muteid}">{mention.group(1)}</a> был выдан варн админом {admin}. \nСейчас количество варнов у пользователя составляет {1}')
                        return
                else:
                    if a[0] == 1:
                        try:
                            reason_a = message.text.split()[2:]
                            reason = " ".join(reason_a)
                            update_varn_user(muteid, 2, reason, datetime.datetime.now())
                            await message.answer(
                                f'Пользователю <a href="tg://user?id={muteid}">{mention.group(1)}</a> был выдан варн админом {admin} по причине {reason}. \nСейчас количество варнов у пользователя составляет {2}')
                        except:
                            update_varn_user(muteid, 2, 'Без причины', datetime.datetime.now())
                            await message.answer(
                                f'Пользователю <a href="tg://user?id={muteid}">{mention.group(1)}</a> был выдан варн админом {admin}. \nСейчас количество варнов у пользователя составляет {2}')
                            return
                    elif a[0] >= 2:
                        await bot.ban_chat_member(message.chat.id, muteid,
                                                  until_date=int(time.time()) + 7 * 86400)
                        await message.answer(
                            f' | <b>Решение выдать бан было принято:</b> {admin}\n | <b>Нарушитель:</b> <a href="tg://user?id={muteid}">{mention.group(1)}</a>\n⏰ | <b>Срок наказания:</b> 1 неделя\n | <b>Причина:</b> Нарушитель получил 3 варна',
                            parse_mode='html')
                        return
        else:
            await message.reply('Вы не указали пользователя!')
    else:
        member_id = message.reply_to_message.from_user.id
        member_name = message.reply_to_message.from_user.username
        admin = message.from_user.mention_html()
        a = get_varn_users(member_id)
        if a is None:
            try:
                reason_a = message.text.split()[1]
                reason_a = message.text.split()[1:]
                reason = " ".join(reason_a)
                new_varn_user(member_id, member_name, 1, reason, datetime.datetime.now())
                await message.answer(
                    f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был выдан варн админом {admin} по причине {reason}. \nСейчас количество варнов у пользователя составляет {1}')
            except:
                new_varn_user(member_id, member_name, 1, 'Без причины', datetime.datetime.now())
                await message.answer(
                    f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был выдан варн админом {admin}. \nСейчас количество варнов у пользователя составляет {1}')
        else:
            if a[0] == 1:
                try:
                    reason_a = message.text.split()[1:]
                    reason = " ".join(reason_a)
                    update_varn_user(member_id, 2, reason, datetime.datetime.now())
                    await message.answer(
                        f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был выдан варн админом {admin} по причине {reason}. \nСейчас количество варнов у пользователя составляет {2}')
                except:
                    update_varn_user(member_id, 2, 'Без причины', datetime.datetime.now())
                    await message.answer(
                        f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был выдан варн админом {admin}. \nСейчас количество варнов у пользователя составляет {2}')

            elif a[0] >= 2:
                await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                          until_date=int(time.time()) + 7 * 86400)
                await message.answer(
                    f' | <b>Решение выдать бан было принято:</b> {admin}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>\n⏰ | <b>Срок наказания:</b> 1 неделя\n | <b>Причина:</b> Нарушитель получил 3 варна',
                    parse_mode='html')


@router.message(IsAdminFilter(is_admin=True), Command('Снять_варн', 'снять_варн', 'варн-', '-варн', prefix="!/"))
async def varn_minus(message: types.Message):
    if not message.reply_to_message:
        mention = re.search(r'@(\w+)', message.text)
        if mention:
            muteid1 = get_user_from_username(mention.group(1))
            if muteid1 != None:
                try:
                    muteid = get_user_from_username(mention.group(1))[0]
                except:
                    await message.reply(f'Вы не указали пользователя')
                    return
                await message.bot.delete_message(message.chat.id, message.message_id)
                admin = message.from_user.mention_html()
                a = get_varn_users(muteid)
                if a is None:
                    await message.reply(f"У пользователя нет варнов")
                else:
                    try:
                        b = message.text.split()[2]
                        if str(b) == 'все':
                            delete_varn_user(muteid)
                            await message.answer(
                                f'Пользователю <a href="tg://user?id={muteid}">{mention.group(1)}</a> были сняты все варны админом {admin}.')
                        else:
                            await message.answer(f'Нет такого аргумента как "{b}"')
                    except IndexError:
                        if a[0] == 1:
                            delete_varn_user(muteid)
                            await message.answer(
                                f'Пользователю <a href="tg://user?id={muteid}">{mention.group(1)}</a> был снят один варн админом {admin}. \nСейчас количество варнов у пользователя составляет {0}')
                        elif a[0] == 2:
                            update_varn_user(muteid, 1, None, datetime.datetime.now())
                            await message.answer(
                                f'Пользователю <a href="tg://user?id={muteid}">{mention.group(1)}</a> был снят один варн админом {admin}. \nСейчас количество варнов у пользователя составляет {1}')

        else:
            await message.reply('Вы не указали пользователя!')
    else:
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
                    update_varn_user(member_id, 1, None, datetime.datetime.now())
                    await message.answer(
                        f'Пользователю <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> был снят один варн админом {admin}. Сейчас количество варнов у пользователя составляет {1}')


@router.message(IsAdminFilter(is_admin=True), Command('варнинфо', 'Варнинфо', 'Ви', 'ви', prefix="!/"))
async def varn_info(message: types.Message):
    varns_info = get_top_varn_users()
    response = 'Варны у участников:\n'
    for i, (userid, username, value_varns, reason, date_last_varn) in enumerate(varns_info, start=1):
        response += f'{i}. <a href="tg://user?id={userid}">{username}</a> количество варнов -  {value_varns}, причина - {reason}, дата - {date_last_varn}\n'
    await message.answer(response)
