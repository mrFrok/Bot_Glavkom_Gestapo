import asyncio
import random
from aiogram import types, Router, F
import re
from aiogram.filters import Command
from aiogram.types import Message
from random import randint, choice
from bot import bot, dp
import config
from db import add_user, update_user, update_dick1, update_dick2, update_dick3, get_user, get_top_dicks, get_users, \
    delete_user, \
    add_user_if_not_exists, add_dick, get_user_dick, full_update, add_user_nedr, update_user_nedr, get_status_nedr, \
    get_users_nedr, \
    get_user_nedr, check_reminder, new_reminder, update_reminder, delete_reminder, get_user_restricts, \
    get_user_from_username, get_user_restricts_for_two_weeks, add_reputation_if_not_exists, get_user_reputation, \
    get_top_reputation, \
    update_reputation, get_last_use_reputation, update_last_use_reputation, get_work_level, get_work_use, \
    update_work_use, update_work_level, update_sick, heal_sick, get_objects, update_object1, update_object2, \
    update_object3, update_medicine, get_last_worked, update_money, update_last_worked, get_money, get_inventory, \
    get_medicine, get_sick, decrease_dick, update_about, get_about, add_loan, get_loan, update_loan_balance, \
    repay_the_loan, check_marriage, add_marriage, get_marriages, delete_marriage, get_user2_from_username, add_temp, \
    get_temp, delete_temp
import datetime
from pyrogram_config import get_chat_members
from filters import IsAdminFilter
import re
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

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


class Remind(StatesGroup):
    YesOrNo = State()


@router.message(Command('работать', 'Работать', prefix='!'), StateFilter(None))
async def work(message: types.Message, state: FSMContext):
    add_dick(message.from_user.id, message.from_user.full_name)
    date_worked = get_last_worked(message.from_user.id)[0]
    if datetime.datetime.now() - datetime.datetime.strptime(date_worked, '%Y-%m-%d %H:%M:%S.%f') > datetime.timedelta(
            hours=24):
        if datetime.datetime.now() - datetime.datetime.strptime(date_worked,
                                                                '%Y-%m-%d %H:%M:%S.%f') > datetime.timedelta(days=7):
            update_work_use(message.from_user.id, 0)
            await message.reply(
                'Начальник удалил вам все отработанные дни, так как вас не было на работе уже больше недели! В следующий раз старайтесь меньше прогуливать работу!')
        is_sick = get_sick(message.from_user.id)[0]
        if is_sick == 1:
            prime_chance = random.random()
            if prime_chance < 0.2:
                money_old = get_money(message.from_user.id)[0]
                money = randint(10, 20)
                update_money(message.from_user.id, money_old + money)
                await message.reply(f'За ваше усердие на работе начальник выписал вам премию в {money} монет')
            days = (datetime.datetime.now() - datetime.datetime.strptime(date_worked, '%Y-%m-%d %H:%M:%S.%f')).days
            minus = days * 2
            decrease_dick(message.from_user.id, get_user_dick(message.from_user.id)[3] - minus)
            await message.reply(
                f'Ваш хуй уменьшился на {minus} см из-за того, что вы больны! Вылечитесь как можно быстрее! Сейчас ваш хуй равен {get_user_dick(message.from_user.id)[3]} см')
            level = get_work_level(message.from_user.id)[0]
            if level == 1:
                money_old = get_money(message.from_user.id)[0]
                money = randint(10, 20)
                update_work_use(message.from_user.id, get_work_use(message.from_user.id)[0] + 1)
                update_last_worked(message.from_user.id, datetime.datetime.now())
                update_money(message.from_user.id, money_old + money)
                try:
                    update_reminder(message.from_user.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                except:
                    pass
                builder = InlineKeyboardBuilder()
                builder.add(types.InlineKeyboardButton(
                    text="В магазин",
                    callback_data="магазин")
                )
                await message.reply(
                    f'Вы заработали {money} монет. Сейчас вы отработали {get_work_use(message.from_user.id)[0]} раз',
                    reply_markup=builder.as_markup())
                if check_reminder(message.from_user.id) is None:
                    builder = InlineKeyboardBuilder()
                    builder.add(types.InlineKeyboardButton(
                        text="Да",
                        callback_data="дар")
                    )
                    builder.add(types.InlineKeyboardButton(
                        text="Нет",
                        callback_data="нетр")
                    )
                    await message.reply('Хотите ли вы подписаться на рассылку?', reply_markup=builder.as_markup())
                    await state.set_state(Remind.YesOrNo)
                    await asyncio.sleep(600)
                    await state.clear()
            elif level == 2:
                money_old = get_money(message.from_user.id)[0]
                money = randint(20, 40)
                update_work_use(message.from_user.id, get_work_use(message.from_user.id)[0] + 1)
                update_last_worked(message.from_user.id, datetime.datetime.now())
                update_money(message.from_user.id, money_old + money)
                try:
                    update_reminder(message.from_user.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                except:
                    pass
                builder = InlineKeyboardBuilder()
                builder.add(types.InlineKeyboardButton(
                    text="В магазин",
                    callback_data="магазин")
                )
                await message.reply(
                    f'Вы заработали {money} монет. Сейчас вы отработали {get_work_use(message.from_user.id)[0]} раз',
                    reply_markup=builder.as_markup())
                if check_reminder(message.from_user.id) is None:
                    builder = InlineKeyboardBuilder()
                    builder.add(types.InlineKeyboardButton(
                        text="Да",
                        callback_data="дар")
                    )
                    builder.add(types.InlineKeyboardButton(
                        text="Нет",
                        callback_data="нетр")
                    )
                    await message.reply('Хотите ли вы подписаться на рассылку?', reply_markup=builder.as_markup())
                    await state.set_state(Remind.YesOrNo)
                    await asyncio.sleep(600)
                    await state.clear()
            elif level == 3:
                money_old = get_money(message.from_user.id)[0]
                money = randint(40, 80)
                update_work_use(message.from_user.id, get_work_use(message.from_user.id)[0] + 1)
                update_last_worked(message.from_user.id, datetime.datetime.now())
                update_money(message.from_user.id, money_old + money)
                try:
                    update_reminder(message.from_user.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                except:
                    pass
                builder = InlineKeyboardBuilder()
                builder.add(types.InlineKeyboardButton(
                    text="В магазин",
                    callback_data="магазин")
                )
                await message.reply(
                    f'Вы заработали {money} монет. Сейчас вы отработали {get_work_use(message.from_user.id)[0]} раз',
                    reply_markup=builder.as_markup())
                if check_reminder(message.from_user.id) is None:
                    builder = InlineKeyboardBuilder()
                    builder.add(types.InlineKeyboardButton(
                        text="Да",
                        callback_data="дар")
                    )
                    builder.add(types.InlineKeyboardButton(
                        text="Нет",
                        callback_data="нетр")
                    )
                    await message.reply('Хотите ли вы подписаться на рассылку?', reply_markup=builder.as_markup())
                    await state.set_state(Remind.YesOrNo)
                    await asyncio.sleep(600)
                    await state.clear()
            else:
                await message.reply('Ошибка какая то :)')
        else:
            prime_chance = random.random()
            if prime_chance < 0.2:
                money_old = get_money(message.from_user.id)[0]
                money = randint(10, 20)
                update_money(message.from_user.id, money_old + money)
                await message.reply(f'За ваше усердие на работе начальник выписал вам премию в {money} монет')
            randoms = random.random()
            if randoms < 0.05:
                update_sick(message.from_user.id, 1)
                await message.reply(
                    'Вы работали слишком усердно, и подхватили болезнь! Теперь ваш хуй будет уменьшаться каждый день на 2 см, и вы не сможете увеличивать хуй! Вылечитесь как можно быстрее!')
            level = get_work_level(message.from_user.id)[0]
            if level == 1:
                money_old = get_money(message.from_user.id)[0]
                money = randint(10, 20)
                update_work_use(message.from_user.id, get_work_use(message.from_user.id)[0] + 1)
                update_last_worked(message.from_user.id, datetime.datetime.now())
                update_money(message.from_user.id, money_old + money)
                try:
                    update_reminder(message.from_user.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                except:
                    pass
                builder = InlineKeyboardBuilder()
                builder.add(types.InlineKeyboardButton(
                    text="В магазин",
                    callback_data="магазин")
                )
                await message.reply(
                    f'Вы заработали {money} монет. Сейчас вы отработали {get_work_use(message.from_user.id)[0]} раз',
                    reply_markup=builder.as_markup())
                if check_reminder(message.from_user.id) is None:
                    builder = InlineKeyboardBuilder()
                    builder.add(types.InlineKeyboardButton(
                        text="Да",
                        callback_data="дар")
                    )
                    builder.add(types.InlineKeyboardButton(
                        text="Нет",
                        callback_data="нетр")
                    )
                    await message.reply('Хотите ли вы подписаться на рассылку?', reply_markup=builder.as_markup())
                    await state.set_state(Remind.YesOrNo)
                    await asyncio.sleep(600)
                    await state.clear()
            elif level == 2:
                money_old = get_money(message.from_user.id)[0]
                money = randint(20, 40)
                update_work_use(message.from_user.id, get_work_use(message.from_user.id)[0] + 1)
                update_last_worked(message.from_user.id, datetime.datetime.now())
                update_money(message.from_user.id, money_old + money)
                try:
                    update_reminder(message.from_user.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                except:
                    pass
                builder = InlineKeyboardBuilder()
                builder.add(types.InlineKeyboardButton(
                    text="В магазин",
                    callback_data="магазин")
                )
                await message.reply(
                    f'Вы заработали {money} монет. Сейчас вы отработали {get_work_use(message.from_user.id)[0]} раз',
                    reply_markup=builder.as_markup())
                if check_reminder(message.from_user.id) is None:
                    builder = InlineKeyboardBuilder()
                    builder.add(types.InlineKeyboardButton(
                        text="Да",
                        callback_data="дар")
                    )
                    builder.add(types.InlineKeyboardButton(
                        text="Нет",
                        callback_data="нетр")
                    )
                    await message.reply('Хотите ли вы подписаться на рассылку?', reply_markup=builder.as_markup())
                    await state.set_state(Remind.YesOrNo)
                    await asyncio.sleep(600)
                    await state.clear()
            elif level == 3:
                money_old = get_money(message.from_user.id)[0]
                money = randint(40, 80)
                update_work_use(message.from_user.id, get_work_use(message.from_user.id)[0] + 1)
                update_last_worked(message.from_user.id, datetime.datetime.now())
                update_money(message.from_user.id, money_old + money)
                try:
                    update_reminder(message.from_user.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                except:
                    pass
                builder = InlineKeyboardBuilder()
                builder.add(types.InlineKeyboardButton(
                    text="В магазин",
                    callback_data="магазин")
                )
                await message.reply(
                    f'Вы заработали {money} монет. Сейчас вы отработали {get_work_use(message.from_user.id)[0]} раз',
                    reply_markup=builder.as_markup())
                if check_reminder(message.from_user.id) is None:
                    builder = InlineKeyboardBuilder()
                    builder.add(types.InlineKeyboardButton(
                        text="Да",
                        callback_data="дар")
                    )
                    builder.add(types.InlineKeyboardButton(
                        text="Нет",
                        callback_data="нетр")
                    )
                    await message.reply('Хотите ли вы подписаться на рассылку?', reply_markup=builder.as_markup())
                    await state.set_state(Remind.YesOrNo)
                    await asyncio.sleep(600)
                    await state.clear()
            else:
                await message.reply('Ошибка какая то :)')
    else:
        time_since_last_use = datetime.datetime.now() - datetime.datetime.strptime(date_worked, '%Y-%m-%d %H:%M:%S.%f')
        time_since_last_use = time_since_last_use - datetime.timedelta(
            microseconds=time_since_last_use.microseconds)
        time_until_next_use = datetime.timedelta(hours=24) - time_since_last_use
        await message.reply(
            f'Вы уже работали сегодня, возвращайтесь через {time_until_next_use}!')


@router.callback_query(F.data == 'магазин')
async def shop1(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
             text="Купить соду",
             callback_data="сода"
        ),
        types.InlineKeyboardButton(
            text="Купить настойку",
            callback_data="настойка"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Купить европейский препарат",
            callback_data="европейский препарат"
        ),
        types.InlineKeyboardButton(
            text="Купить лекарство от болезни",
            callback_data="лекарство от болезни"
        )
    )
    await callback.message.reply(f'Здравствуйте, {callback.from_user.full_name}!\n'
                        f'Ваш баланс: {get_money(callback.from_user.id)[0]} монет\n'
                        'Доступные товары:\n'
                        'Сода(1 уровень) - 10 монет\n'
                        'Настойка(2 уровень) - 40 монет\n'
                        'Европейский препарат(3 уровень) - 80 монет(Чтобы купить, пишите просто препарат))\n'
                        'Лекарство от болезни - 300 монет\n'
                        'Чтобы купить товар напишите "!купить название_товара количество_товара"(без надписей в скобках)',
                        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'дар', Remind.YesOrNo)
async def yes(callback: types.CallbackQuery, state: FSMContext):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    new_reminder(callback.from_user.id, callback.from_user.full_name, now)
    await callback.message.answer(
        'Вы подписались на рассылку! Не забудьте начать диалог с ботом, если вы его ещё не начали')
    await bot.send_message(callback.from_user.id, 'Проверка. Вы подписались на напоминание')
    await state.clear()


@router.callback_query(F.data == 'нетр', Remind.YesOrNo)
async def no(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Как хотите!')
    await state.clear()


@router.message(Command('Отписаться', 'отписаться', prefix='!'))
async def unsubscribe(message: types.Message):
    delete_reminder(message.from_user.id)
    await message.reply('Вы отписались от рассылки!')


@router.message(Command('повышение', 'Повышение', prefix='!'))
async def upgrade(message: types.Message):
    level = get_work_level(message.from_user.id)[0]
    work_hours = get_work_use(message.from_user.id)[0]
    if level == 1:
        if work_hours >= 14:
            update_work_level(message.from_user.id, 2)
            update_work_use(message.from_user.id, 0)
            await message.reply(
                'Вы получили повышение! Теперь вы на 2 уровне! Чтобы получить повышение, вам нужно проработать 30 дней')
        else:
            await message.reply(f'Чтобы получить повышение, вам нужно проработать ещё {14 - work_hours} дней!')
    elif level == 2:
        if work_hours >= 30:
            update_work_level(message.from_user.id, 3)
            update_work_use(message.from_user.id, 0)
            await message.reply(
                'Вы получили повышение! Теперь вы на 3 уровне! Больше повысить уровень нельзя!')
        else:
            await message.reply(f'Чтобы получить повышение, вам нужно проработать ещё {30 - work_hours} дней!')
    else:
        await message.reply('Вы уже на 3 уровне!')


@router.message(Command('лечиться', 'Лечиться', prefix='!'))
async def heal(message: types.Message):
    medicine = get_medicine(message.from_user.id)[0]
    is_sick = get_sick(message.from_user.id)[0]
    if is_sick == 1:
        if medicine > 0:
            heal_sick(message.from_user.id, 0, medicine - 1)
            await message.reply('Вы вылечились!')
        else:
            await message.reply('У вас нет лекарств!')
    else:
        await message.reply('Вы здоровы!')


@router.message(Command('магазин', 'Магазин', prefix='!'))
async def shop(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Купить соду",
            callback_data="сода"
        ),
        types.InlineKeyboardButton(
            text="Купить настойку",
            callback_data="настойка"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Купить европейский препарат",
            callback_data="европейский препарат"
        ),
        types.InlineKeyboardButton(
            text="Купить лекарство от болезни",
            callback_data="лекарство от болезни"
        )
    )
    await message.reply(f'Здравствуйте, {message.from_user.full_name}!\n'
                        f'Ваш баланс: {get_money(message.from_user.id)[0]} монет\n'
                        'Доступные товары:\n'
                        'Сода(1 уровень) - 10 монет\n'
                        'Настойка(2 уровень) - 40 монет\n'
                        'Европейский препарат(3 уровень) - 80 монет(Чтобы купить, пишите просто препарат))\n'
                        'Лекарство от болезни - 300 монет\n'
                        'Чтобы купить товар напишите "!купить название_товара количество_товара"(без надписей в скобках)',
                        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'сода')
async def buy_soda(callback: types.CallbackQuery):
    money = get_money(callback.from_user.id)[0]
    if money >= 10:
        update_object1(callback.from_user.id, get_objects(callback.from_user.id)[0] + 1, money - 10)
        await callback.message.reply(f'Вы купили соду')
    else:
        await callback.message.reply('Недостаточно монет!')


@router.callback_query(F.data == 'настойка')
async def buy_nastoyka(callback: types.CallbackQuery):
    money = get_money(callback.from_user.id)[0]
    if money >= 40:
        update_object2(callback.from_user.id, get_objects(callback.from_user.id)[1] + 1, money - 40)
        await callback.message.reply(f'Вы купили настойку')
    else:
        await callback.message.reply('Недостаточно монет!')


@router.callback_query(F.data == 'европейский препарат')
async def buy_preparat(callback: types.CallbackQuery):
    money = get_money(callback.from_user.id)[0]
    if money >= 80:
        update_object3(callback.from_user.id, get_objects(callback.from_user.id)[2] + 1, money - 80)
        await callback.message.reply(f'Вы купили европейский препарат')
    else:
        await callback.message.reply('Недостаточно монет!')


@router.callback_query(F.data == 'лекарство от болезни')
async def buy_medicine(callback: types.CallbackQuery):
    money = get_money(callback.from_user.id)[0]
    if money >= 300:
        update_medicine(callback.from_user.id, get_medicine(callback.from_user.id)[0] + 1, money - 300)
        await callback.message.reply(f'Вы купили лекарство от болезни')
    else:
        await callback.message.reply('Недостаточно монет!')


@router.message(Command('монеты', 'Монеты', 'баланс', 'Баланс', prefix='!'))
async def money(message: types.Message):
    await message.reply(f'Ваш баланс составляет {get_money(message.from_user.id)[0]} монет')


@router.message(Command('купить', 'Купить', prefix='!'))
async def buy(message: types.Message):
    try:
        money = get_money(message.from_user.id)[0]
        product = message.text.split()[1]
        count = int(message.text.split()[2])
        if product.lower() == 'сода':
            if money >= 10 * count:
                update_object1(message.from_user.id, get_objects(message.from_user.id)[0] + 1, money - 10 * count)
                await message.reply(f'Вы купили {count} соды')
            else:
                await message.reply('Недостаточно монет!')
        elif product.lower() == 'настойка':
            if money >= 40 * count:
                update_object2(message.from_user.id, get_objects(message.from_user.id)[1] + 1, money - 40 * count)
                await message.reply(f'Вы купили {count} настойки')
            else:
                await message.reply('Недостаточно монет!')
        elif product.lower() == 'препарат':
            if money >= 80 * count:
                update_object3(message.from_user.id, get_objects(message.from_user.id)[2] + 1, money - 80 * count)
                await message.reply(f'Вы купили {count} европейских препаратов')
            else:
                await message.reply('Недостаточно монет!')
        elif product.lower() == 'лекарство':
            if money >= 300 * count:
                update_medicine(message.from_user.id, get_medicine(message.from_user.id)[0] + 1, money - 300 * count)
                await message.reply(f'Вы купили {count} лекарства от болезни')
            else:
                await message.reply('Недостаточно монет!')
        else:
            await message.reply('Такого товара нет!')
    except:
        await message.reply(
            'Неверно введено! Введите "!купить название_товара количество_товара"(без надписей в скобках)')


@router.message(Command('Инвентарь', 'инвентарь', prefix='!'))
async def inventory(message: types.Message):
    inventory = get_inventory(message.from_user.id)
    await message.reply(f'Ваш инвентарь:\n'
                        f'Сода: {inventory[0]} шт\n'
                        f'Настойка: {inventory[1]} шт\n'
                        f'Европейский препарат: {inventory[2]} шт\n'
                        f'Лекарство от болезни: {inventory[3]} шт')


@router.message(Command('писька', 'хуй', prefix='!'))
async def dick(message: types.Message):
    now = datetime.datetime.now()
    userid = message.from_user.id
    a = get_user_dick(userid)
    is_sick = get_sick(userid)[0]
    if a is None:
        await message.reply('Вы не можете увеличить хуй, не имея увеличителя!')
        return
    if int(message.chat.id) - int(config.GROUP_ID) != 0:
        await message.reply('Вы не состоите в группе!')
        return
    if is_sick == 1:
        await message.reply('Вы болеете и не можете увеличивать хуй!')
        return
    else:
        try:
            medication = message.text.split()[1]
            if now - datetime.datetime.strptime(a[5], '%Y-%m-%d %H:%M:%S.%f') < datetime.timedelta(hours=24):
                time_since_last_use = now - datetime.datetime.strptime(a[5], '%Y-%m-%d %H:%M:%S.%f')
                time_since_last_use = time_since_last_use - datetime.timedelta(
                    microseconds=time_since_last_use.microseconds)
                time_until_next_use = datetime.timedelta(hours=24) - time_since_last_use
                await message.reply(
                    f'Вы уже пытались вырастить хуй сегодня, возвращайтесь через {time_until_next_use}! Сейчас ваш хуй равен {a[3]} см')
            else:
                if a is None:
                    add_dick(message.from_user.id, message.from_user.full_name)
                    await message.reply('Вы не можете увеличить хуй, не имея увеличителя!')
                else:
                    if medication.lower() == 'сода':
                        if get_objects(userid)[0] >= 1:
                            size = randint(1, 10)
                            update_dick1(a[3] + size, now, userid, get_objects(userid)[0] - 1)
                            await message.reply(f'Ваш хуй увеличился на {size} см, теперь он равен {a[3] + size} см')
                        else:
                            await message.reply('У вас нет соды!')
                    elif medication.lower() == 'настойка':
                        if get_objects(userid)[1] >= 1:
                            size = randint(10, 20)
                            update_dick2(a[3] + size, now, userid, get_objects(userid)[1] - 1)
                            await message.reply(f'Ваш хуй увеличился на {size} см, теперь он равен {a[3] + size} см')
                        else:
                            await message.reply('У вас нет настойки!')
                    elif medication.lower() == 'препарат':
                        if get_objects(userid)[2] >= 1:
                            size = randint(20, 40)
                            update_dick3(a[3] + size, now, userid, get_objects(userid)[2] - 1)
                            await message.reply(f'Ваш хуй увеличился на {size} см, теперь он равен {a[3] + size} см')
                        else:
                            await message.reply('У вас нет европейского препарата!')
                    else:
                        await message.reply('Такого увеличителя нет!')
        except:
            await message.reply('Неверно введено! Введите "!хуй название_увеличителя"(без надписей в скобках)')


@router.message(Command('взять_кредит', 'Взять_кредит', prefix='!'))
async def take_loan(message: types.Message):
    userid = message.from_user.id
    is_loan = get_loan(userid)[0]
    if is_loan == 1:
        await message.reply(
            f'Вы уже брали кредит! Ваш долг составляет 250 монет! У вас осталось {datetime.datetime.now() - datetime.datetime.strptime(get_loan(userid)[2], '%Y-%m-%d %H:%M:%S.%f')} дней')
    else:
        update_money(userid, get_money(userid)[0] + 200)
        add_loan(userid, 1, 250, datetime.datetime.now())
        await message.reply(
            'Вы взяли кредит на 200 монет! Вы должны будете вернуть 250 монет через 14 дней! Если вы не вернете 250 монет в течение 7 дней, ваш долг будет увеличиваться на 10 монет ежедневно!')


@router.message(Command('кредит', 'Кредит', prefix='!'))
async def credit(message: types.Message):
    userid = message.from_user.id
    is_loan = get_loan(userid)[0]
    if is_loan == 1:
        date_loan = get_loan(userid)[2]
        last_date_loan = get_loan(userid)[3]
        days = datetime.datetime.now() - datetime.datetime.strptime(date_loan, '%Y-%m-%d %H:%M:%S.%f')
        days = (datetime.timedelta(days=14) - days).days
        if datetime.datetime.now() - datetime.datetime.strptime(date_loan, '%Y-%m-%d %H:%M:%S.%f') > datetime.timedelta(
                days=14):
            if last_date_loan is None or datetime.datetime.now() - datetime.datetime.strptime(last_date_loan,
                                                                                              '%Y-%m-%d %H:%M:%S.%f') > datetime.timedelta(
                hours=24):
                try:
                    loan = 10 * (datetime.datetime.now() - datetime.datetime.strptime(get_loan(userid)[4],
                                                                                      '%Y-%m-%d %H:%M:%S.%f')).days
                    update_loan_balance(userid, get_loan(userid)[1] + loan, datetime.datetime.now(),
                                        datetime.datetime.now())
                    await message.reply(f'Ваш долг увеличился на {loan} монет из-за просрочки на {days} дней!')
                    await message.reply(
                        f'Ваш долг составляет {get_loan(userid)[1]} монет! У вас осталось {days} дней')
                    return
                except:
                    loan = 10 * -1 * days
                    update_loan_balance(userid, get_loan(userid)[1] + loan, datetime.datetime.now(),
                                        datetime.datetime.now())
                    await message.reply(f'Ваш долг увеличился на {loan} монет из-за просрочки на {days} дней!')
                    await message.reply(
                        f'Ваш долг составляет {get_loan(userid)[1]} монет! У вас осталось {days} дней')
                    return
            else:
                await message.reply(
                    f'Ваш долг составляет {get_loan(userid)[1]} монет! У вас осталось {days} дней')
                return
        await message.reply(
            f'Ваш долг составляет {get_loan(userid)[1]} монет! У вас осталось {days} дней')
    else:
        await message.reply('У вас нет кредита!')


@router.message(Command('выплатить_кредит', 'Выплатить_кредит', 'погасить_кредит', 'Погасить_кредит', prefix='!'))
async def repay_loan(message: types.Message):
    userid = message.from_user.id
    is_loan = get_loan(userid)[0]
    date_loan = get_loan(userid)[2]
    days = datetime.datetime.now() - datetime.datetime.strptime(date_loan, '%Y-%m-%d %H:%M:%S.%f')
    days = datetime.timedelta(days=14) - days
    last_date_loan = get_loan(userid)[3]
    if is_loan == 1:
        if datetime.datetime.now() - datetime.datetime.strptime(date_loan, '%Y-%m-%d %H:%M:%S.%f') > datetime.timedelta(
                days=14):
            if last_date_loan is None or datetime.datetime.now() - datetime.datetime.strptime(last_date_loan,
                                                                                              '%Y-%m-%d %H:%M:%S.%f') > datetime.timedelta(
                hours=24):
                try:
                    loan = 10 * (datetime.datetime.now() - datetime.datetime.strptime(get_loan(userid)[4],
                                                                                      '%Y-%m-%d %H:%M:%S.%f')).days
                    update_loan_balance(userid, get_loan(userid)[1] + loan, datetime.datetime.now(),
                                        datetime.datetime.now())
                    if get_money(userid)[0] >= get_loan(userid)[1]:
                        update_money(userid, get_money(userid)[0] - get_loan(userid)[1])

                        repay_the_loan(userid, 0)
                        await message.reply('Вы выплатили кредит!')
                        return
                    else:
                        await message.reply(
                            f'У вас недостаточно монет! Вам нужно ещё {get_loan(userid)[1] - get_money(userid)[0]} монет')
                        return
                except:
                    loan = 10 * -1 * days
                    update_loan_balance(userid, get_loan(userid)[1] + loan, datetime.datetime.now(),
                                        datetime.datetime.now())
                    if get_money(userid)[0] >= get_loan(userid)[1]:
                        update_money(userid, get_money(userid)[0] - get_loan(userid)[1])

                        repay_the_loan(userid, 0)
                        await message.reply('Вы выплатили кредит!')
                        return
                    else:
                        await message.reply(
                            f'У вас недостаточно монет! Вам нужно ещё {get_loan(userid)[1] - get_money(userid)[0]} монет')
                        return
        if get_money(userid)[0] >= get_loan(userid)[1]:
            update_money(userid, get_money(userid)[0] - get_loan(userid)[1])
            repay_the_loan(userid, 0)
            await message.reply('Вы выплатили кредит!')
            return
        else:
            await message.reply(
                f'У вас недостаточно монет! Вам нужно ещё {get_loan(userid)[1] - get_money(userid)[0]} монет')
            return
    else:
        await message.reply('У вас нет кредита!')
        return


@router.message(Command('топ_хуев', 'тх', prefix='!'))
async def top_dicks(message: types.Message):
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
    chat_members = await get_chat_members(message.chat.id)

    async def is_bot(user_id, message: types.Message):
        user = await message.bot.get_chat_member(message.chat.id, user_id)
        return user.user.is_bot

    added_users_count = 0

    for user_id, name, username in chat_members:
        if not await is_bot(user_id, message):  # Проверяем, не является ли пользователь ботом
            add_user_if_not_exists(user_id, username, name, datetime.datetime.now())
            added_users_count += 1

    await message.reply(f'Добавлено {added_users_count} пользователей')


@router.message(Command('дело', 'Дело', prefix='!/'), IsAdminFilter(is_admin=True))
async def case(message: types.Message):
    mention = re.search(r'@(\w+)', message.text)
    if mention:
        try:
            mention = mention.group(1)
            personal = get_user_from_username(mention)[0]
            personally_case = get_user_restricts_for_two_weeks(personal)
            response = 'Все нарушения пользователя за 2 недели: \n'
            for i, (x, y, m) in enumerate(personally_case, start=1):
                response += f'{i}. Тип наказания: {x}, Причина наказания: {y}, Дата наказания: {m}\n'
            await message.reply(response)
        except:
            await message.reply('Пользователь чист')


@router.message(Command('реп', prefix='+'))
async def rep(message: types.Message):
    if message.from_user.id != message.reply_to_message.from_user.id:
        add_reputation_if_not_exists(message.from_user.id, message.from_user.username, message.from_user.full_name, 0)
        add_reputation_if_not_exists(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username,
                                     message.reply_to_message.from_user.full_name, 0)
        last_used = get_last_use_reputation(message.from_user.id)[0]
        if (datetime.datetime.now() - datetime.datetime.strptime(last_used,
                                                                 '%Y-%m-%d %H:%M:%S.%f')) >= datetime.timedelta(
            hours=3):
            rep_old = get_user_reputation(message.from_user.id)[0]
            rep = rep_old + 1
            update_reputation(message.reply_to_message.from_user.id, rep)
            update_last_use_reputation(message.from_user.id, datetime.datetime.now())
            await message.answer(
                f'{message.from_user.mention_html()} оказывает уважение <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> (+1)')
        else:
            time_since_last_use = datetime.datetime.now() - datetime.datetime.strptime(last_used,
                                                                                       '%Y-%m-%d %H:%M:%S.%f')
            time_since_last_use = time_since_last_use - datetime.timedelta(
                microseconds=time_since_last_use.microseconds)
            time_until_next_use = datetime.timedelta(hours=3) - time_since_last_use
            await message.answer(f'Вы уже оказывали уважение\неуважение! Возвращайстесь через {time_until_next_use}')
    else:
        await message.answer('Нельзя оказывать уважение самому себе')


@router.message(Command('реп', prefix='-'))
async def rep_min(message: types.Message):
    if message.from_user.id != message.reply_to_message.from_user.id:
        add_reputation_if_not_exists(message.from_user.id, message.from_user.username, message.from_user.full_name, 0)
        add_reputation_if_not_exists(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username,
                                     message.reply_to_message.from_user.full_name, 0)
        last_used = get_last_use_reputation(message.from_user.id)[0]
        if (datetime.datetime.now() - datetime.datetime.strptime(last_used,
                                                                 '%Y-%m-%d %H:%M:%S.%f')) >= datetime.timedelta(
            hours=3):
            rep_old = get_user_reputation(message.from_user.id)[0]
            rep = rep_old - 1
            update_reputation(message.reply_to_message.from_user.id, rep)
            update_last_use_reputation(message.from_user.id, datetime.datetime.now())
            await message.answer(
                f'{message.from_user.mention_html()} неуважает <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> (-1)')
        else:
            time_since_last_use = datetime.datetime.now() - datetime.datetime.strptime(last_used,
                                                                                       '%Y-%m-%d %H:%M:%S.%f')
            time_since_last_use = time_since_last_use - datetime.timedelta(
                microseconds=time_since_last_use.microseconds)
            time_until_next_use = datetime.timedelta(hours=3) - time_since_last_use
            await message.answer(f'Вы уже оказывали уважение\неуважение! Возвращайстесь через {time_until_next_use}')
    else:
        await message.answer('Нельзя оказывать уважение самому себе')


@router.message(Command('топ_реп', 'тр', prefix='!'))
async def top_rep(message: types.Message):
    top_rep = get_top_reputation()
    response = 'Топ-10 репутации:\n'
    for i, (userid, name, reputation) in enumerate(top_rep, start=1):
        response += f'{i}. <a href="tg://user?id={userid}">{name}</a> ({reputation})\n'
    await message.answer(response)


@router.message(Command('биография', 'Биография', prefix='!'))
async def about_user(message: types.Message):
    try:
        messages = message.text.split()[1]
        if messages.lower() == 'заполнить':
            try:
                about = message.text.split()[2:]
                about = ' '.join(about)
                if about == '':
                    await message.answer('Вы не указали биографию! Напишите "!биография заполнить ваша_биография"')
                    return
                update_about(message.from_user.id, about)
                await message.answer('Ваша биография была успешно заполнена!')
            except:
                await message.answer('Вы не указали биографию! Напишите "!биография заполнить ваша_биография"')
        else:
            about = get_about(message.from_user.id)[0]
            if about == None:
                await message.answer(
                    'Вы еще не заполнили свою биографию! Напишите "!биография заполнить ваша_биография"')
            else:
                await message.answer(f'Вот ваша биография:\n{about}')
    except:
        about = get_about(message.from_user.id)[0]
        if about == None:
            await message.answer('Вы еще не заполнили свою биографию! Напишите "!биография заполнить ваша_биография"')
        else:
            await message.answer(f'Вот ваша биография:\n{about}')


class MarriageForm(StatesGroup):
    sogl = State()


@router.message(Command('брак', 'Брак', prefix='!'))
async def marriage(message: types.Message, state: FSMContext):
    mention = re.search(r'@(\w+)', message.text)
    if mention:
        user2 = get_user2_from_username(mention.group(1))
        if user2 is None:
            await message.reply('Пользователь не найден')
            await state.clear()
            return
        elif user2[1] == message.from_user.id:
            await message.reply('Вы не можете оформить брак с самим собой!')
            await state.clear()
            return
        else:
            await state.update_data(userid2=user2[1], username2=user2[2], name2=user2[3])
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(
                    text="Да",
                    callback_data="дам")
            )
            builder.add(types.InlineKeyboardButton(
                    text="Нет",
                    callback_data="нетм")
            )
            await message.answer(
                    f'Внимание, <a href="tg://user?id={user2[1]}">{user2[3]}</a>!\nВы хотите оформить брак с <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>?',
                    reply_markup=builder.as_markup())
            await state.set_state(MarriageForm.sogl)
            add_temp(message.from_user.id, user2[1], message.from_user.username, user2[2],
                         message.from_user.full_name, user2[3])
            await asyncio.sleep(600)
            await state.clear()
    else:
        await message.reply('Вы не указали пользователя! Напишите "!брак @имя_пользователя"')



@router.callback_query(F.data == 'дам')
async def marriage_yes(callback: types.CallbackQuery, state: FSMContext):
    userid = callback.from_user.id
    userid2 = get_temp(userid)[0][2]
    if userid2 == userid:
        users_data = get_temp(callback.from_user.id)[0]
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_marriage(userid1=users_data[1], userid2=users_data[2], username1=users_data[3], username2=users_data[4],
                     name1=users_data[5], name2=users_data[6], date=date)
        await callback.message.answer(
            f'Внимание, чат!\nБрак между <a href="tg://user?id={users_data[1]}">{users_data[5]}</a> и <a href="tg://user?id={users_data[2]}">{users_data[6]}</a> был оформлен!')
        await state.clear()
        delete_temp(users_data[1], users_data[2])
    else:
        pass


@router.callback_query(F.data == 'нетм')
async def marriage_no(callback: types.CallbackQuery, state: FSMContext):
    userid = callback.from_user.id
    userid2 = get_temp(userid)[0]
    if userid2[2] == userid:
        await callback.message.answer('Брак не оформлен!')
        await state.clear()
        delete_temp(userid2[1], userid2[2])
    else:
        pass


@router.message(Command('бракинфо', 'Бракинфо', prefix='!'))
async def marriage_info(message: types.Message):
    marriages = check_marriage(message.from_user.id)
    print(marriages)
    if not marriages:
        await message.reply('Вы еще не состоите в браке!')
    else:
        mari_info = check_marriage(message.from_user.id)[0]
        await message.reply(
            f'Вот ваш брак:\nПервый супруг(Инициатор брака): <a href="tg://user?id={mari_info[1]}">{mari_info[5]}</a>\nВторой супруг: <a href="tg://user?id={mari_info[2]}">{mari_info[6]}</a>\nДата заключения брака: {mari_info[7]}')


@router.message(Command('развод', 'Развод', prefix='!'))
async def marriage_break(message: types.Message, state: FSMContext):
    marriages = check_marriage(message.from_user.id)
    if not marriages:
        await message.reply('Вы еще не состоите в браке!')
        return
    else:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Да",
            callback_data="дараз")
        )
        builder.add(types.InlineKeyboardButton(
            text="Нет",
            callback_data="нетраз")
        )
        await message.reply(f'Вы точно хотите развестись? Это действие необратимо!!!', reply_markup=builder.as_markup())
        await state.set_state(MarriageForm.sogl)


@router.callback_query(F.data == 'дараз', MarriageForm.sogl)
async def marriage_break_yes(callback: types.CallbackQuery, state: FSMContext):
    marriages = check_marriage(callback.from_user.id)[0]
    delete_marriage(marriages[1], marriages[2])
    await callback.message.answer(f'Внимание чат!\n<a href="tg://user?id={marriages[1]}">{marriages[5]}</a> и <a href="tg://user?id={marriages[2]}">{marriages[6]}</a> развелись!')
    await state.clear()


@router.callback_query(F.data == 'нетраз', MarriageForm.sogl)
async def marriage_break_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Ваш брак был сохранен!')
    await state.clear()


@router.message(Command('браки', 'Браки', prefix='!'))
async def marriage_list(message: types.Message):
    marriages = get_marriages()
    response = 'Браки этого чата:\n'
    for i, j in enumerate(marriages, start=1):
        response += f'{i}. <a href="tg://user?id={j[1]}">{j[5]}</a> и <a href="tg://user?id={j[2]}">{j[6]}</a> с {j[7]}\n'
    await message.answer(response)

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
