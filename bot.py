import logging
import time

import data_manager
import my_rules_manager
import service_data_manager
import transaction_change_data_manager
from aiogram import Bot, Dispatcher, executor, types


import inline_keyboard
from config import BOT_TOKEN
import bot_messages
import chart_manager


logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Переменные для понимания какие данные вводит пользователь
RULE_INPUT_BOOL: dict = {}
RULE_INPUT_STR: dict = {}
RULE_INPUT_INT: dict = {}
RULE_INPUT_STR_BOOL: dict = {}


TRANSACTION_INPUT_MINUS_BOOL: dict = {}
TRANSACTION_INPUT_CATEGORY_BOOL: dict = {}
TRANSACTION_INPUT_OPERATION_BOOL: dict = {}

TRANSACTION_INPUT_MINUS_INT: dict = {}
TRANSACTION_INPUT_MINUS_CATEGORY: dict = {}
TRANSACTION_INPUT_OPERATION: dict = {}


COMMITMENT_SUM: dict = {}
COMMITMENT_NAME: dict = {}
COMMITMENT_DATE: dict = {}

COMMITMENT_SUM_BOOL: dict = {}
COMMITMENT_NAME_BOOL: dict = {}
COMMITMENT_DATE_BOOL: dict = {}

TRAINIG_DICT_BOOL: dict = {}
########################################################################
##                    Основная часть бота                             ##
########################################################################


######################################## Ветка обучения ################################################################
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    reset_minus_menu_data(message.chat.id)
    last_message = await bot.send_message(message.chat.id,
                                          text=bot_messages.start(),
                                          reply_markup=inline_keyboard.START)
    service_data_manager.add_record(message.chat.id, last_message.message_id)


@dp.callback_query_handler(text='training_create_rule')
async def training_create_rule(callback_query: types.CallbackQuery):
    global TRAINIG_DICT_BOOL
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=bot_messages.create_rule(),
                                reply_markup=inline_keyboard.TRAINING_CREATE_RULE)
    TRAINIG_DICT_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text='training_calendar')
async def training_calendar(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=bot_messages.calendar(),
                                reply_markup=inline_keyboard.TRAINING_CALENDAR)


@dp.callback_query_handler(text='create_training_calendar')
async def training_create_calendar(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=bot_messages.create_calendar(),
                                reply_markup=inline_keyboard.TRAINING_CREATE_CALENDAR)


@dp.callback_query_handler(text='training_transaction')
async def training_create_transaction(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=bot_messages.transaction(),
                                reply_markup=inline_keyboard.TRAINING_TRANSACTION)


@dp.callback_query_handler(text='create_training_transaction')
async def training_transaction(callback_query: types.CallbackQuery):
    reset_minus_menu_data(callback_query.from_user.id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=bot_messages.create_transaction())
    time.sleep(5)
    await menu(callback_query)
########################################################################################################################


# ГЛАВНОЕ МЕНЮ
@dp.callback_query_handler(text='menu')
async def menu(callback_query: types.CallbackQuery):
    reset_minus_menu_data(callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    sum_of_plus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                          operation="Доход")
    sum_of_minus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                           operation="Расход")
    balance = sum_of_plus - sum_of_minus
    sum_of_pay = sum(data_manager.get_cost(callback_query.from_user.id))

    last_message = await bot.send_photo(chat_id=callback_query.from_user.id,
                                        photo=chart_manager.get_pie_chart(callback_query.from_user.id),
                                        caption=f'💵БАЛАНС: {balance} (₽)\n'
                                                f'Общая сумма затрат: {sum_of_pay} (₽)\n'
                                                f'Рекомендуемая сумма затрат: {int((balance - sum_of_pay) / 30)} (₽) в день'
                                                f' / {balance - sum_of_pay} (₽) в месяц ',
                                        reply_markup=inline_keyboard.MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


########################################################################################################################
#                                       Меню "Календарь обязательств"                                                  #
########################################################################################################################
@dp.callback_query_handler(text='calendar_of_commitments')
async def calendar_of_commitments_menu(callback_query: types.CallbackQuery):
    global COMMITMENT_SUM
    global COMMITMENT_NAME
    global COMMITMENT_DATE
    COMMITMENT_SUM[callback_query.from_user.id] = 'Ввести сумму'
    COMMITMENT_NAME[callback_query.from_user.id] = 'Ввести название'
    COMMITMENT_DATE[callback_query.from_user.id] = 'Ввести дату'
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    sum_of_plus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                          operation="Доход")
    sum_of_minus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                           operation="Расход")
    balance = sum_of_plus - sum_of_minus
    sum_of_pay = sum(data_manager.get_cost(callback_query.from_user.id))

    last_message = await bot.send_photo(chat_id=callback_query.from_user.id,
                                        photo=chart_manager.get_calendar_table(callback_query.from_user.id),
                                        caption=f'💵БАЛАНС: {balance} (₽)\n'
                                                f'Общая сумма затрат: {sum_of_pay} (₽)\n'
                                                f'Рекомендуемая сумма затрат: {int((balance-sum_of_pay)/30)} (₽) в день'
                                                f' / {balance-sum_of_pay} (₽) в месяц ',
                                        reply_markup=inline_keyboard.CALENDAR_MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='create_commitment')
async def create_commitment(callback_query: types.CallbackQuery):
    global COMMITMENT_SUM
    global COMMITMENT_NAME
    global COMMITMENT_DATE
    global COMMITMENT_SUM_BOOL
    global COMMITMENT_NAME_BOOL
    global COMMITMENT_DATE_BOOL
    COMMITMENT_SUM_BOOL[callback_query.from_user.id] = False
    COMMITMENT_NAME_BOOL[callback_query.from_user.id] = False
    COMMITMENT_DATE_BOOL[callback_query.from_user.id] = False
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Создание обязательства:',
                                          reply_markup=inline_keyboard.create_commitment_menu(f'{COMMITMENT_SUM[callback_query.from_user.id]} (₽)',
                                                                                              COMMITMENT_NAME[callback_query.from_user.id],
                                                                                              COMMITMENT_DATE[callback_query.from_user.id]))
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='enter_sum_commitment')
async def enter_sum_commitment(callback_query: types.CallbackQuery):
    global COMMITMENT_SUM_BOOL
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите cумму (₽):',
                                reply_markup=inline_keyboard.BTN_BACK_TO_CREATE_COMMITMENT_MENU)
    COMMITMENT_SUM_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text='enter_name_of_commitment')
async def enter_name_commitment(callback_query: types.CallbackQuery):
    global COMMITMENT_NAME_BOOL
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите название:',
                                reply_markup=inline_keyboard.BTN_BACK_TO_CREATE_COMMITMENT_MENU)
    COMMITMENT_NAME_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text='enter_date_of_commitment')
async def enter_date_commitment(callback_query: types.CallbackQuery):
    global COMMITMENT_DATE_BOOL
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите дату, формата "дд-мм-гггг":',
                                reply_markup=inline_keyboard.BTN_BACK_TO_CREATE_COMMITMENT_MENU)
    COMMITMENT_DATE_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text='save_commitment')
async def enter_date_commitment(callback_query: types.CallbackQuery):
    global COMMITMENT_SUM
    global COMMITMENT_NAME
    global COMMITMENT_DATE
    global TRAINIG_DICT_BOOL

    if COMMITMENT_SUM[callback_query.from_user.id] != 'Ввести сумму' and \
        COMMITMENT_NAME[callback_query.from_user.id] != 'Ввести название' and \
        COMMITMENT_DATE[callback_query.from_user.id] != 'Ввести дату':
        data_manager.add_record(callback_query.from_user.id,
                                cost=COMMITMENT_SUM[callback_query.from_user.id],
                                rule=COMMITMENT_NAME[callback_query.from_user.id],
                                date=COMMITMENT_DATE[callback_query.from_user.id])
        chart_manager.set_calendar_table(callback_query.from_user.id)
        chart_manager.set_pie_chart(callback_query.from_user.id)
        if TRAINIG_DICT_BOOL[callback_query.from_user.id]:
            await training_create_transaction(callback_query)
        else:
            await calendar_of_commitments_menu(callback_query)
    else:
        await bot.send_message(callback_query.from_user.id, text='Заполните пожалуйста все поля')
        await create_commitment(callback_query.from_user.id)

@dp.callback_query_handler(text='delete_commitment')
async def delete_commitment(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Удаление обязательства:',
                                          reply_markup=inline_keyboard.get_commitment(callback_query.from_user.id))
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text=inline_keyboard.get_index_delete_commitment())
async def delete_commitment(callback_query: types.CallbackQuery):
    data_manager.delete_record(callback_query.from_user.id, int(callback_query.data.replace('_commitment', '')))
    chart_manager.set_calendar_table(callback_query.from_user.id)
    chart_manager.set_pie_chart(callback_query.from_user.id)
    await calendar_of_commitments_menu(callback_query)
########################################################################################################################
#                                        Конец "Календарь обязательств"                                                #
########################################################################################################################


########################################################################################################################
#                                        Меню "Мои Правила"                                                            #
########################################################################################################################
@dp.callback_query_handler(text='my_rules')
async def my_rule_menu(callback_query: types.CallbackQuery):
    reset_minus_menu_data(callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    last_message = await bot.send_photo(chat_id=callback_query.from_user.id,
                                        photo=chart_manager.get_my_rules_table(callback_query.from_user.id),
                                        reply_markup=inline_keyboard.MY_RULE_MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='create_rule')
async def create_menu(callback_query: types.CallbackQuery):
    global RULE_INPUT_INT
    global RULE_INPUT_STR
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Создание правила:',
                                          reply_markup=inline_keyboard.create_rule_menu(
                                              category=RULE_INPUT_STR[callback_query.from_user.id],
                                              limitation=f'{RULE_INPUT_INT[callback_query.from_user.id]} (₽)')
                                          )
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='choose_category_rule')
async def choose_category_rule(callback_query: types.CallbackQuery):
    global RULE_INPUT_STR_BOOL
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите название:',
                                reply_markup=inline_keyboard.BACK_TO_RULE_MENU
                                )
    RULE_INPUT_STR_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text=inline_keyboard.get_rule_category_list())
async def choose_category_rule(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_CATEGORY
    TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id] = inline_keyboard.rule_translate_key(callback_query.data)
    await create_menu(callback_query)


@dp.callback_query_handler(text='enter_limitation_rule')
async def choose_category_rule(callback_query: types.CallbackQuery):
    global RULE_INPUT_BOOL
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите ограничение (₽):',
                                reply_markup=inline_keyboard.BACK_TO_RULE_MENU
                                )
    RULE_INPUT_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text='save_rule')
async def save_rule(callback_query: types.CallbackQuery):
    global RULE_INPUT_INT
    global RULE_INPUT_STR
    if RULE_INPUT_INT[callback_query.from_user.id] != "Ввести сумму" and\
            RULE_INPUT_STR[callback_query.from_user.id] != "Ввести название":
        my_rules_manager.add_record(tg_id=callback_query.from_user.id,
                                    category=RULE_INPUT_STR[callback_query.from_user.id],
                                    cost=RULE_INPUT_INT[callback_query.from_user.id])
        chart_manager.set_my_rules_table(telegram_id=callback_query.from_user.id)
        if TRAINIG_DICT_BOOL[callback_query.from_user.id]:
            await training_calendar(callback_query)
        else:
            await my_rule_menu(callback_query)
    else:
        bot.send_message(callback_query.from_user.id, text='Заполните пожалуйста все поля')
        await create_menu(callback_query)


@dp.callback_query_handler(text='delete_rule')
async def delete_rule(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))
    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Какое правило удалить?',
                                          reply_markup=inline_keyboard.ger_list_of_btn_rule(callback_query.from_user.id))
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text=inline_keyboard.get_index_list_delete())
async def delete_list(callback_query: types.CallbackQuery):
    my_rules_manager.delete_record(tg_id=callback_query.from_user.id,
                                   index=int(callback_query.data.replace('_rule', '')))
    chart_manager.set_my_rules_table(callback_query.from_user.id)
    await my_rule_menu(callback_query)
########################################################################################################################
#                                       Конец Меню "Мои Правила"                                                       #
########################################################################################################################


########################################################################################################################
#                                        Меню "Транзакционные изменения"                                               #
########################################################################################################################
@dp.callback_query_handler(text='transaction_change')
async def transaction_change_menu(callback_query: types.CallbackQuery):
    reset_minus_menu_data(callback_query.from_user.id)

    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))
    sum_of_plus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                          operation="Доход")
    sum_of_minus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                          operation="Расход")
    text = f'📥Пополнения: {sum_of_plus}\n' \
           f'📤Затраты: {sum_of_minus}\n' \
           f'💵БАЛАНС: {sum_of_plus-sum_of_minus}'
    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text=text,
                                          reply_markup=inline_keyboard.TRANSACTION_CHANGE_MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='add_transaction')
async def transaction_change_add_transaction(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_INT
    global TRANSACTION_INPUT_MINUS_CATEGORY
    global TRANSACTION_INPUT_OPERATION
    await bot.delete_message(callback_query.from_user.id,
                             service_data_manager.get_last_message_id(callback_query.from_user.id))
    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Заполните поля:',
                                          reply_markup=inline_keyboard.enter_minus_menu(
                                              f'{TRANSACTION_INPUT_MINUS_INT[callback_query.from_user.id]} (₽)',
                                              TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id],
                                              TRANSACTION_INPUT_OPERATION[callback_query.from_user.id])
                                          )
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='enter_minus')
async def enter_minus(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_BOOL
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите число:',
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)
    TRANSACTION_INPUT_MINUS_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text='choose_category')
async def choose_category(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_CATEGORY_BOOL
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите название:',
                                reply_markup=inline_keyboard.CATEGORIES_MENU)
    TRANSACTION_INPUT_CATEGORY_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text='choose_operation')
async def choose_category(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Выберите операцию:',
                                reply_markup=inline_keyboard.CHOOSE_OPERATION)


@dp.callback_query_handler(text=inline_keyboard.get_list_callback_operations())
async def choose_category(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_OPERATION
    operation = inline_keyboard.get_translate_list_callback_operation(callback_query.data)
    TRANSACTION_INPUT_OPERATION[callback_query.from_user.id] = operation
    await transaction_change_add_transaction(callback_query)


@dp.callback_query_handler(text='save_minus_choose')
async def save_minus_choose(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_INT
    global TRANSACTION_INPUT_MINUS_CATEGORY
    global TRANSACTION_INPUT_OPERATION
    global TRAINIG_DICT_BOOL

    if TRANSACTION_INPUT_MINUS_INT[callback_query.from_user.id] == 'Ввести сумму'\
        or TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id] == 'Ввести название'\
        or TRANSACTION_INPUT_OPERATION[callback_query.from_user.id] == 'Выберите операцию':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Заполните пожалуйста все поля')
    else:
        transaction_change_data_manager.add_record(tg_id=callback_query.from_user.id,
                                                   name=TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id],
                                                   cost=TRANSACTION_INPUT_MINUS_INT[callback_query.from_user.id],
                                                   operation=TRANSACTION_INPUT_OPERATION[callback_query.from_user.id])
        chart_manager.set_my_rules_table(telegram_id=callback_query.from_user.id)
        chart_manager.set_calendar_table(telegram_id=callback_query.from_user.id)
        chart_manager.set_pie_chart(telegram_id=callback_query.from_user.id)
        if TRAINIG_DICT_BOOL[callback_query.from_user.id]:
            await training_transaction(callback_query)
        else:
            await transaction_change_menu(callback_query)


@dp.callback_query_handler(text='transaction_history_all')
async def transaction_history_all(callback_query: types.CallbackQuery):
    text = transaction_change_data_manager.get_transactions_all(tg_id=callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=text,
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)


@dp.callback_query_handler(text='delete_transaction')
async def delete_transaction(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Какие транзакции удалить?',
                                reply_markup=inline_keyboard.get_transaction_list(callback_query.from_user.id))


@dp.callback_query_handler(text=inline_keyboard.get_index_transaction_delete())
async def delete_transaction(callback_query: types.CallbackQuery):
    transaction_change_data_manager.delete_record(tg_id=callback_query.from_user.id,
                                                  index=int(callback_query.data.replace('_transaction', '')))
    chart_manager.set_my_rules_table(callback_query.from_user.id)
    await transaction_change_menu(callback_query)
########################################################################################################################
#                                       Конец Меню "Транзакционные изменения"                                          #
########################################################################################################################


@dp.message_handler(content_types='text')
async def input_data(message: types.Message):
    global RULE_INPUT_STR_BOOL
    global RULE_INPUT_STR
    global RULE_INPUT_BOOL
    global RULE_INPUT_INT

    global TRANSACTION_INPUT_MINUS_BOOL
    global TRANSACTION_INPUT_MINUS_INT
    global TRANSACTION_INPUT_CATEGORY_BOOL
    global TRANSACTION_INPUT_MINUS_CATEGORY

    global COMMITMENT_SUM
    global COMMITMENT_NAME
    global COMMITMENT_DATE

    if RULE_INPUT_BOOL[message.chat.id]:
        RULE_INPUT_INT[message.chat.id] = message.text
        RULE_INPUT_BOOL[message.chat.id] = False
        await create_menu(message)

    elif RULE_INPUT_STR_BOOL[message.chat.id]:
        RULE_INPUT_STR[message.chat.id] = message.text
        RULE_INPUT_STR_BOOL[message.chat.id] = False
        await create_menu(message)

    elif TRANSACTION_INPUT_MINUS_BOOL[message.chat.id]:
        try:
            data = message.text
            TRANSACTION_INPUT_MINUS_INT[message.chat.id] = int(data)
            TRANSACTION_INPUT_MINUS_BOOL[message.chat.id] = False
            await transaction_change_add_transaction(message)
        except:
            await message.answer(text='Введите пожалуйста так, как указано в примере.')

    elif TRANSACTION_INPUT_CATEGORY_BOOL[message.chat.id]:
        data = message.text
        TRANSACTION_INPUT_MINUS_CATEGORY[message.chat.id] = data
        TRANSACTION_INPUT_CATEGORY_BOOL[message.chat.id] = False
        await transaction_change_add_transaction(message)

    elif COMMITMENT_SUM_BOOL[message.chat.id]:
        try:
            data = message.text
            COMMITMENT_SUM[message.chat.id] = int(data)
            COMMITMENT_SUM_BOOL[message.chat.id] = False
            await create_commitment(message)
        except:
            await message.answer(text='Введите пожалуйсто число')

    elif COMMITMENT_NAME_BOOL[message.chat.id]:
        data = message.text
        COMMITMENT_NAME[message.chat.id] = data
        COMMITMENT_NAME_BOOL[message.chat.id] = False
        await create_commitment(message)

    elif COMMITMENT_DATE_BOOL[message.chat.id]:
            try:
                data = message.text
                date = data.split('-')
                if (0 < int(date[0]) <= 31) and (0 < int(date[1]) <= 12) and (2023 <= int(date[2]) <= 2300):
                    COMMITMENT_DATE[message.chat.id] = data
                    COMMITMENT_DATE_BOOL[message.chat.id] = False
                    await create_commitment(message)
            except:
                await message.answer(text='Введите пожалуйста так, как указано в примере')

    else:
        await message.answer(text='Я не понимаю.')


########################################################################
##                   Вспомогательные функции                          ##
########################################################################
def reset_minus_menu_data(user_id):
    global TRANSACTION_INPUT_MINUS_INT
    global TRANSACTION_INPUT_MINUS_CATEGORY
    global TRANSACTION_INPUT_OPERATION
    global RULE_INPUT_INT
    global RULE_INPUT_STR
    global TRAINIG_DICT_BOOL
    global COMMITMENT_SUM
    global COMMITMENT_NAME
    global COMMITMENT_DATE
    global COMMITMENT_SUM_BOOL
    global COMMITMENT_NAME_BOOL
    global COMMITMENT_DATE_BOOL
    COMMITMENT_SUM[user_id] = 'Ввести сумму'
    COMMITMENT_NAME[user_id] = 'Ввести название'
    COMMITMENT_DATE[user_id] = 'Ввести дату'
    RULE_INPUT_INT[user_id] = 'Ввести сумму'
    RULE_INPUT_STR[user_id] = 'Ввести название'
    TRANSACTION_INPUT_MINUS_INT[user_id] = 'Ввести сумму'
    TRANSACTION_INPUT_MINUS_CATEGORY[user_id] = 'Ввести название'
    TRANSACTION_INPUT_OPERATION[user_id] = 'Выберите операцию'
    RULE_INPUT_BOOL[user_id] = False
    RULE_INPUT_STR_BOOL[user_id] = False
    TRANSACTION_INPUT_MINUS_BOOL[user_id] = False
    TRANSACTION_INPUT_CATEGORY_BOOL[user_id] = False
    TRANSACTION_INPUT_OPERATION_BOOL[user_id] = False
    COMMITMENT_SUM_BOOL[user_id] = False
    COMMITMENT_NAME_BOOL[user_id] = False
    COMMITMENT_DATE_BOOL[user_id] = False
    TRAINIG_DICT_BOOL[user_id] = False


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
