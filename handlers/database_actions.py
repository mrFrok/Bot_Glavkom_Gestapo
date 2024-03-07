import random
from aiogram import types, Router, F
from aiogram.filters import Command
from bot import dp, bot
from aiogram.types import Message
from random import randint, choice
import config
from db import add_user, update_user, update_dick, get_user, get_top_dicks, get_users, delete_user, \
    add_user_if_not_exists, add_dick, get_user_dick, full_update, add_user_nedr, update_user_nedr, get_status_nedr, \
    get_users_nedr, \
    get_user_nedr, check_reminder, new_reminder, update_reminder, delete_reminder
import datetime
from pyrogram_config import get_chat_members_id, get_chat_members_name, get_chat_members_username
from filters import IsAdminFilter

router = Router()


@router.message(Command('старт', 'start', prefix='!/'))
async def start(message: types.Message):
    userid = message.from_user.id
    a = get_user(userid)
    if int(message.chat.id) - int(config.GROUP_ID) != 0:
        await message.reply('Вы не состоите в группе!')
    elif a is None:
        date_add = str(datetime.datetime.now())
        username = message.from_user.username
        name = message.from_user.full_name
        add_user(userid, username, name, date_add)
        await message.reply('Вы успешно добавленны в базу данных')
    elif a[3] != message.from_user.full_name or a[2] != message.from_user.username:
        full_update(userid, message.from_user.username, message.from_user.full_name)
        await message.reply('Ваше имя успешно изменено')
    else:
        await message.reply('Вы уже есть в базе данных!')


@router.message(Command('писька', 'хуй', prefix='!'))
async def dick(message: types.Message):
    last_used = datetime.datetime.now()
    userid = message.from_user.id
    a = get_user_dick(userid)
    if int(message.chat.id) - int(config.GROUP_ID) != 0:
        await message.reply('Вы не состоите в группе!')
    elif a is None:
        size = randint(-3, 10)
        name = message.from_user.full_name
        add_dick(userid, name, size, last_used)
        await message.reply(f'Ваш размер хуя теперь равен {size} см')
    else:
        size = randint(-10, 20)
        if last_used - datetime.datetime.strptime(a[4], '%Y-%m-%d %H:%M:%S.%f') > datetime.timedelta(hours=24):
            if a[3] > a[3] + size:
                update_dick(a[3] + size, last_used, userid)
                await message.reply(
                    f'Ваш хуй уменьшился на {size} см, теперь он равен {a[3] + size} см')
            elif a[3] < a[3] + size:
                update_dick(a[3] + size, last_used, userid)
                await message.reply(
                    f'Ваш хуй увеличился на {size} см, теперь он равен {a[3] + size} см')
            else:
                update_dick(a[3] + size, last_used, userid)
                await message.reply(f'Ваш хуй не изменился, сейчас он равен {a[3]} см')
        else:
            time_since_last_use = last_used - datetime.datetime.strptime(a[4], '%Y-%m-%d %H:%M:%S.%f')
            time_since_last_use = time_since_last_use - datetime.timedelta(
                microseconds=time_since_last_use.microseconds)
            time_until_next_use = datetime.timedelta(hours=24) - time_since_last_use
            await message.reply(
                f'Вы уже пытались вырастить хуй сегодня, возвращайтесь через {time_until_next_use}! Сейчас ваш хуй равен {a[3]} см')


@router.message(Command('топ_хуев', 'тх', prefix='!'))
async def top_hui(message: types.Message):
    top_hui = get_top_dicks()
    response = 'Топ-10 хуёв:\n'
    for i, (userid, name, size) in enumerate(top_hui, start=1):
        response += f'{i}. <a href="tg://user?id={userid}">{name}</a> ({size} см)\n'
    await message.answer(response)


@router.message(Command('кто', 'Кто', 'who', 'Who', prefix='!'))
async def who(message: types.Message):
    users = get_users()
    rand = choice(users)
    messages1 = message.text.split()[1:]
    messages = ' '.join(messages1)
    answer_id = get_user(int(rand[0]))[1]
    answer_name = get_user(int(rand[0]))[3]
    await message.answer(f'Мне кажется, что <a href="tg://user?id={answer_id}">{answer_name}</a> {messages}')


@router.message(F.new_chat_member)
async def new_members_handler(message: Message):
    new_member = message.new_chat_members[0]
    add_user(new_member.id, new_member.username, new_member.full_name, datetime.datetime.now())
    await bot.send_message(message.chat.id,
                           f'Добро пожаловать, <a href="tg://user?id={new_member.id}">{new_member.full_name}</a>! Ты попал в лучшую группу, здесь рады всем! \n'
                           f"В этой группе ты можешь найти новых друзей, общаться с самыми лучшими, дружными и адекватными людьми со всего света \n"
                           f"С правилами ты можешь ознакомиться <a href = 'https://t.me/pmcfemboy228/3836/3837'>здесь</a> \n"
                           f"Так же у нас есть <a href = 'https://discord.gg/wWFxVGJsmQ'>Discord</a>\n"
                           f"Больше не буду задерживать, удачи!")


@router.message(F.left_chat_member)
async def on_chat_member_left(message: types.Message):
    user = message.left_chat_member
    delete_user(user.id)
    await message.answer(
        f'Прощай, <a href="tg://user?id={user.id}">{user.full_name}</a>. Мы будем тебя помнить(Или нет)')


@router.message(Command('созвать всех', 'св', 'созвать_всех', 'Созвать_всех', 'Св', 'созыв', 'Созыв', prefix='!'))
async def calling(message: types.Message):
    users = get_users()
    await message.answer(
        f'Пользователь <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a> запустил призыв')
    emoji_list = [
        '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯',
        '🦁', '🐮', '🐷', '🐸', '🐵', '🐔', '🐧', '🐦', '🐤', '🐣',
        '🐥', '🦆', '🦢', '🦉', '🦚', '🦜', '🦩', '🦔', '🐺', '🦝',
        '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦗',
        '🕷️', '🦂', '🦀', '🦞', '🦐', '🦑', '🐙', '🦈', '🐬', '🐳',
        '🐋', '🦭', '🐢', '🐍', '🦎', '🐊', '🐸', '🦢', '🦆', '🦉',
        '🦚', '🦜', '🦩', '🦔', '🐇', '🦝', '🦨', '🦡', '🐾', '🦛',
        '🦘', '🦡', '🐧', '🐦', '🦆', '🦢', '🦜', '🦩', '🦔', '🐇',
        '🦝', '🦨', '🦡', '🐾', '🦛', '🦘', '🐆', '🦓', '🦌', '🦬',
        '🐃', '🐄', '🐖', '🐏', '🐑', '🐐', '🦙', '🦚', '🦜', '🦢',
        '🦩', '🦔', '👨‍❤️‍👨'
    ]

    chunk_size = 8
    chunks = [users[i:i + chunk_size] for i in range(0, len(users), chunk_size)]

    for chunk in chunks:
        random.shuffle(emoji_list)
        mention_text = ''.join(
            [f'<a href="tg://user?id={user[0]}">{emoji}</a>' for user, emoji in zip(chunk, emoji_list[:len(chunk)])])
        await message.answer(f'{mention_text}')

    await message.answer(f'Созыв окончен')


@router.message(Command('доббд', 'дпбд', 'auid', prefix='!/'), IsAdminFilter(is_admin=True))
async def dobbd(message: types.Message):
    chat_members_id = await get_chat_members_id(message.chat.id)
    chat_members_name = await get_chat_members_name(message.chat.id)
    chat_members_username = await get_chat_members_username(message.chat.id)

    async def is_bot(user_id, message: types.Message):
        user = await message.bot.get_chat_member(message.chat.id, user_id)
        return user.user.is_bot

    added_users_count = 0

    for i, x, y in zip(chat_members_id, chat_members_name, chat_members_username):
        if not await is_bot(i, message):  # Проверяем, не является ли пользователь ботом
            add_user_if_not_exists(i, y, x, datetime.datetime.now())
            added_users_count += 1

    await message.reply(f'Добавлено {added_users_count} пользователей')


'''
@router.message(Command('рассылка', 'Рассылка', prefix='!'))
async def reminder(message: types.Message, state: FSMContext):
    check = check_reminder(message.from_user.id)
    if check == None:
        await state.set_state(Form.question1)
        await message.reply(
            f'Сейчас вы не подписаны на рассылку. Вы хотите подписаться на рассылку?(Напишите Да/Нет)\nВНИМАНИЕ! Чтобы бот мог прислать вам напоминание, вы должны начать с ним чат!')
    else:
        await state.set_state(Form.question1)
        await message.reply(
            f'Прямо сейчас вы подписаны на рассылку. Желаете ли вы отписаться от рассылки или изменить время получения рассылки?\nВведите "Отписаться", чтобы отписаться от рассылки или "изменить", чтобы изменить время.')


@router.message(Form.question1)
async def form_question1(message: Message, state: FSMContext):
    await state.update_data(question1=message.text)
    que = await state.get_data()
    await state.clear()
    question = que['question1']
    if question.lower() == 'да':
        new_reminder(message.from_user.id, message.from_user.full_name)
        await message.reply(
            f'Вы успешно подписались на рассылку. Теперь, каждый день в 6:00 по МСК вы будете получать рассылку.\nУбедитесь, что вы начали чат с ботом, иначе он не сможет присылать сообщения')
    else:
        await message.reply(f'Как хотите.')
'''
"""
@router.message(Form.question2)
async def form_question2(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(question2=message.text)
        que = await state.get_data()
        time = int(que['question2'])
        if time >= 0 and time <= 24:
            new_reminder(message.from_user.id, message.from_user.full_name, time)
            await message.reply(
                f'Вы успешно подписались на рассылку. Теперь, каждый день в {time} час(-ов, -а).\nУбедитесь, что вы начали чат с ботом, иначе он не сможет присылать сообщения')
            await state.clear()
        else:
            await message.reply(f'Неправильное время! Должно быть от 0 до 24, попробуйте снова!')
    else:
        await message.reply(f'Вы ввели часы неправильно! Попробуйте заново')
"""

"""
@router.message(Command('учавствовать_в_недрочабре', 'увн', prefix='!'))
async def nedr(message: types.Message):
    member_id = message.from_user.id
    member_name = message.from_user.full_name
    a = get_status_nedr(member_id)
    now_day = datetime.datetime.now()
    is_admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if a != None:
        await message.answer(f'Вы уже участвуете в недрочабре! Сейчас вы {a[0]}')
    elif now_day.day != 1 or now_day.month != 11:
        await message.answer(f"Сейчас не первое ноября, регистрация закрыта!")
    elif CREATOR.check(member=is_admin) == True:
        add_user_nedr(member_id, member_name, "Гранд магистр🟪")
        await message.answer(f'Поздравляем, теперь вы участвуете в недрочабре! Теперь вы {"Гранд Магистр🟪"}')
    elif IS_ADMIN.check(member=is_admin) == True:
        add_user_nedr(member_id, member_name, "Магистр🟩")
        await message.answer(f'Поздравляем, теперь вы участвуете в недрочабре! Теперь вы {"Мастер🟩"}')
    else:
        add_user_nedr(member_id, member_name, "Джедай🟦")
        await message.answer(f'Поздравляем, теперь вы участвуете в недрочабре! Теперь вы {"Джедай🟦"}')

@router.message(Command('перейти_на_темную_сторону', 'пнтс', 'пасть', prefix='!'))
async def pnts(message: types.Message):
    member_id = message.from_user.id
    member_name = message.from_user.full_name
    a = get_user_nedr(member_id)
    is_admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if a == None:
        await message.answer(f'Вы не участвуете в недрочабре! Пропишите команду !увн для участия(Если сегодня 1 ноября)')
    elif a[2] == 1:
        await message.answer(f'Вы уже перешли на тёмную сторону! Сейчас вы {a[1]}')
    elif CREATOR.check(member=is_admin) == True:
        update_user_nedr(member_id, member_name, "Владыка ситхов⬛")
        await message.answer(f'Вы перешли на тёмную сторону! Теперь вы {"Владыка ситхов⬛"}')
    elif IS_ADMIN.check(member=is_admin) == True:
        update_user_nedr(member_id, member_name, "Дарт🟧")
        await message.answer(f"Вы перешли на тёмную сторону! Теперь вы {'Дарт🟧'}")
    else:
        update_user_nedr(member_id, member_name, 'Ситх 🟥')
        await message.answer(f'Вы перешли на тёмную сторону! Теперь вы {"Cитх🟥"}')


@router.message(Command('участники_недрочабря', 'ун', prefix='!'))
async def top_nedr(message: types.Message):
    users = get_users_nedr()
    response = 'Участники недрочабря:\n'
    for i, (userid, username, status) in enumerate(users, start=1):
        response += f'{i}. <a href="tg://user?id={userid}">{username}</a> - {status}\n'
    await message.answer(response)
"""
