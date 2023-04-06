import logging
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

MONEY_INPUT_BOOL: dict = {}
MONEY_INPUT_INT: dict = {}

TRANSACTION_INPUT_PLUS_BOOL: dict = {}
TRANSACTION_INPUT_MINUS_BOOL: dict = {}

TRANSACTION_INPUT_MINUS_INT: dict = {}
TRANSACTION_INPUT_MINUS_CATEGORY: dict = {}
TRANSACTION_INPUT_MINUS_SUB_CATEGORY: dict = {}

COMMITMENT_SUM: dict = {}
COMMITMENT_NAME: dict = {}
COMMITMENT_DATE: dict = {}

COMMITMENT_SUM_BOOL: dict = {}
COMMITMENT_NAME_BOOL: dict = {}
COMMITMENT_DATE_BOOL: dict = {}



########################################################################
##                    Основная часть бота                             ##
########################################################################
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    last_message = await bot.send_message(message.chat.id,
                                          text='Добро пожаловать!',
                                          reply_markup=inline_keyboard.START)
    service_data_manager.add_record(message.chat.id, message.message_id)


# ГЛАВНОЕ МЕНЮ
@dp.callback_query_handler(text='menu')
async def menu(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    caption = get_rules_and_cost_string(callback_query.from_user.id)
    last_message = await bot.send_photo(chat_id=callback_query.from_user.id,
                                        photo=chart_manager.get_pie_chart(callback_query.from_user.id),
                                        reply_markup=inline_keyboard.MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


########################################################################################################################
#                                       Меню "Календарь обязательств"                                                  #
########################################################################################################################
@dp.callback_query_handler(text='calendar_of_commitments')
async def calendar_of_commitments_menu(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
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
                                        caption=f'БАЛАНС: {balance} (₽)\n'
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
    data_manager.add_record(callback_query.from_user.id,
                            cost=COMMITMENT_SUM[callback_query.from_user.id],
                            rule=COMMITMENT_NAME[callback_query.from_user.id],
                            date=COMMITMENT_DATE[callback_query.from_user.id])
    chart_manager.set_calendar_table(callback_query.from_user.id)
    chart_manager.set_pie_chart(callback_query.from_user.id)
    await calendar_of_commitments_menu(callback_query)


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
    reset_inputs(callback_query.from_user.id)
    reset_minus_menu_data(callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    last_message = await bot.send_photo(chat_id=callback_query.from_user.id,
                                        photo=chart_manager.get_my_rules_table(callback_query.from_user.id),
                                        reply_markup=inline_keyboard.MY_RULE_MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='create_rule')
async def create_menu(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    global TRANSACTION_INPUT_MINUS_CATEGORY
    global RULE_INPUT_INT
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Создание правила:',
                                          reply_markup=inline_keyboard.create_rule_menu(
                                              category=TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id],
                                              limitation=f'{RULE_INPUT_INT[callback_query.from_user.id]} (₽)')
                                          )
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='choose_category_rule')
async def choose_category_rule(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Выберите Категорию:',
                                reply_markup=inline_keyboard.RULE_CATEGORIES_MENU
                                )


@dp.callback_query_handler(text=inline_keyboard.get_rule_category_list())
async def choose_category_rule(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_CATEGORY
    TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id] = inline_keyboard.rule_translate_key(callback_query.data)
    await create_menu(callback_query)


@dp.callback_query_handler(text='enter_limitation_rule')
async def choose_category_rule(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    global RULE_INPUT_BOOL
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите ограничение (₽):',
                                reply_markup=inline_keyboard.BACK_TO_RULE_MENU
                                )
    RULE_INPUT_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text='save_rule')
async def save_rule(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    global RULE_INPUT_INT
    global TRANSACTION_INPUT_MINUS_CATEGORY
    if RULE_INPUT_INT[callback_query.from_user.id] != "Ввести сумму" and\
            TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id] != "Выберите Категорию":
        my_rules_manager.add_record(tg_id=callback_query.from_user.id,
                                    category=TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id],
                                    cost=RULE_INPUT_INT[callback_query.from_user.id])
        chart_manager.set_my_rules_table(telegram_id=callback_query.from_user.id)
        await my_rule_menu(callback_query)
    else:
        await create_menu(callback_query)


@dp.callback_query_handler(text='delete_rule')
async def delete_rule(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))
    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Какое правило удалить?',
                                          reply_markup=inline_keyboard.ger_list_of_btn_rule(callback_query.from_user.id))
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text=inline_keyboard.get_index_list_delete())
async def delete_list(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
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
    text = f'Пополнения: {sum_of_plus}\n' \
           f'Затраты: {sum_of_minus}\n' \
           f'БАЛАНС: {sum_of_plus-sum_of_minus}'
    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text=text,
                                          reply_markup=inline_keyboard.TRANSACTION_CHANGE_MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='add_transaction')
async def transaction_change_add_transaction(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    reset_minus_menu_data(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Выберите "Доход" или "Расход":',
                                reply_markup=inline_keyboard.TURN_CATEGORY_FOR_ADD)


@dp.callback_query_handler(text='plus_transaction_change')
async def plus_transaction_change(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_PLUS_BOOL
    reset_inputs(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите название транзакции (НАЗВАНИЕ:СУММА)\nНапример: Подработка:2599',
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)
    TRANSACTION_INPUT_PLUS_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text='minus_transaction_change')
async def minus_transaction_change(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_INT
    global TRANSACTION_INPUT_MINUS_CATEGORY
    global TRANSACTION_INPUT_MINUS_SUB_CATEGORY
    await bot.delete_message(callback_query.from_user.id,
                             service_data_manager.get_last_message_id(callback_query.from_user.id))
    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Внести "Расход":',
                                          reply_markup=inline_keyboard.enter_minus_menu(f'{TRANSACTION_INPUT_MINUS_INT[callback_query.from_user.id]} (₽)',
                                                                                        TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id],
                                                                                        TRANSACTION_INPUT_MINUS_SUB_CATEGORY[callback_query.from_user.id])
                                          )
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='enter_minus')
async def enter_minus(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_BOOL
    reset_inputs(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите число:',
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)
    TRANSACTION_INPUT_MINUS_BOOL[callback_query.from_user.id] = True


@dp.callback_query_handler(text='choose_category')
async def choose_category(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_SUB_CATEGORY
    TRANSACTION_INPUT_MINUS_SUB_CATEGORY[callback_query.from_user.id] = 'Выберите ПодКатегорию'
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Выберите Категорию:',
                                reply_markup=inline_keyboard.CATEGORIES_MENU)


@dp.callback_query_handler(text=inline_keyboard.get_category_list())
async def category_list(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_CATEGORY
    TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id] = inline_keyboard.translate_key(callback_query.data)
    await minus_transaction_change(callback_query)


@dp.callback_query_handler(text='choose_sub_category')
async def choose_sub_category(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_CATEGORY
    if TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id] == 'Выберите Категорию':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Сначала выберите Категорию')
    else:
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                    text='Выберите ПодКатегорию:',
                                    reply_markup=inline_keyboard.get_sub_category_BTNS(TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id]))


@dp.callback_query_handler(text=inline_keyboard.get_sub_category_list())
async def sub_category_list(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_SUB_CATEGORY
    TRANSACTION_INPUT_MINUS_SUB_CATEGORY[callback_query.from_user.id] = inline_keyboard.translate_sub_key(callback_query.data)
    await minus_transaction_change(callback_query)


@dp.callback_query_handler(text='save_minus_choose')
async def save_minus_choose(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_INT
    global TRANSACTION_INPUT_MINUS_CATEGORY
    global TRANSACTION_INPUT_MINUS_SUB_CATEGORY

    if TRANSACTION_INPUT_MINUS_INT[callback_query.from_user.id] == 'Ввести сумму'\
        or TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id] == 'Выберите Категорию'\
        or TRANSACTION_INPUT_MINUS_SUB_CATEGORY[callback_query.from_user.id] == 'Выберите ПодКатегорию':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Заполните пожалуйста все поля')
    else:
        transaction_change_data_manager.add_record(tg_id=callback_query.from_user.id,
                                                   name=f'{TRANSACTION_INPUT_MINUS_CATEGORY[callback_query.from_user.id]}({TRANSACTION_INPUT_MINUS_SUB_CATEGORY[callback_query.from_user.id]})',
                                                   cost=TRANSACTION_INPUT_MINUS_INT[callback_query.from_user.id],
                                                   operation='Расход')
        chart_manager.set_my_rules_table(telegram_id=callback_query.from_user.id)
        await transaction_change_menu(callback_query)


@dp.callback_query_handler(text='transaction_history_plus')
async def transaction_history_plus(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    text = transaction_change_data_manager.get_transactions(tg_id=callback_query.from_user.id,
                                                            operation="Доход")
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=text,
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)


@dp.callback_query_handler(text='transaction_history_minus')
async def transaction_history_plus(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    text = transaction_change_data_manager.get_transactions(tg_id=callback_query.from_user.id,
                                                            operation="Расход")
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=text,
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)


@dp.callback_query_handler(text='transaction_history_all')
async def transaction_history_all(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    text = transaction_change_data_manager.get_transactions_all(tg_id=callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=text,
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)


@dp.callback_query_handler(text='delete_transaction')
async def delete_transaction(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Какие транзакции удалить?',
                                reply_markup=inline_keyboard.get_transaction_list(callback_query.from_user.id))


@dp.callback_query_handler(text=inline_keyboard.get_index_transaction_delete())
async def delete_transaction(callback_query: types.CallbackQuery):
    reset_inputs(callback_query.from_user.id)
    transaction_change_data_manager.delete_record(tg_id=callback_query.from_user.id,
                                                  index=int(callback_query.data.replace('_transaction', '')))
    chart_manager.set_my_rules_table(callback_query.from_user.id)
    await transaction_change_menu(callback_query)
########################################################################################################################
#                                       Конец Меню "Транзакционные изменения"                                          #
########################################################################################################################


@dp.message_handler(content_types='text')
async def input_data(message: types.Message):
    global RULE_INPUT_STR
    global RULE_INPUT_BOOL
    global RULE_INPUT_INT
    global MONEY_INPUT_INT
    global MONEY_INPUT_BOOL
    global TRANSACTION_INPUT_PLUS_BOOL
    global TRANSACTION_INPUT_MINUS_BOOL
    global TRANSACTION_INPUT_MINUS_INT

    global COMMITMENT_SUM
    global COMMITMENT_NAME
    global COMMITMENT_DATE

    if RULE_INPUT_BOOL[message.chat.id]:
        RULE_INPUT_INT[message.chat.id] = message.text
        MONEY_INPUT_BOOL[message.chat.id] = False
        await create_menu(message)

    elif MONEY_INPUT_BOOL[message.chat.id]:
        MONEY_INPUT_BOOL[message.chat.id] = False
        try:
            MONEY_INPUT_INT = float(message.text)
            await message.answer(text='Перейдем к следующему шагу? Или добавим еще правило?',
                                 reply_markup=inline_keyboard.END_TRAINING)
        except:
            MONEY_INPUT_BOOL = True
            await message.answer(text='Введите пожалуйста число')

    elif TRANSACTION_INPUT_PLUS_BOOL[message.chat.id]:
        try:
            data = message.text
            data = data.split(':')
            name = data[0].strip()
            cost = data[1].strip()
            cost = int(cost)
            operation = 'Доход'
            transaction_change_data_manager.add_record(tg_id=message.chat.id,
                                                       name=name,
                                                       cost=cost,
                                                       operation=operation)
            TRANSACTION_INPUT_PLUS_BOOL[message.chat.id] = False
            await transaction_change_menu(message)

        except:
            await message.answer(text='Введите пожалуйста так, как указано в примере.')

    elif TRANSACTION_INPUT_MINUS_BOOL[message.chat.id]:
        try:
            data = message.text
            TRANSACTION_INPUT_MINUS_INT[message.chat.id] = int(data)
            await minus_transaction_change(message)
        except:
            await message.answer(text='Введите пожалуйста так, как указано в примере.')

    elif COMMITMENT_SUM_BOOL[message.chat.id]:
        try:
            data = message.text
            COMMITMENT_SUM[message.chat.id] = int(data)
            await create_commitment(message)
        except:
            await message.answer(text='Введите пожалуйсто число')

    elif COMMITMENT_NAME_BOOL[message.chat.id]:
        data = message.text
        COMMITMENT_NAME[message.chat.id] = data
        await create_commitment(message)

    elif COMMITMENT_DATE_BOOL[message.chat.id]:
            try:
                data = message.text
                date = data.split('-')
                if (0 < int(date[0]) <= 31) and (0 < int(date[1]) <= 12) and (2023 <= int(date[2]) <= 2300):
                    COMMITMENT_DATE[message.chat.id] = data
                    await create_commitment(message)
            except:
                await message.answer(text='Введите пожалуйста так, как указано в примере')

    else:
        await message.answer(text='Я не понимаю.')


########################################################################
##                   Вспомогательные функции                          ##
########################################################################
def reset_inputs(user_id):
    global RULE_INPUT_STR
    global RULE_INPUT_BOOL
    global MONEY_INPUT_INT
    global MONEY_INPUT_BOOL
    global TRANSACTION_INPUT_PLUS_BOOL
    global TRANSACTION_INPUT_MINUS_BOOL
    RULE_INPUT_BOOL[user_id] = False
    RULE_INPUT_STR[user_id] = ''
    MONEY_INPUT_BOOL[user_id] = False
    MONEY_INPUT_INT[user_id] = 0
    TRANSACTION_INPUT_PLUS_BOOL[user_id] = False
    TRANSACTION_INPUT_MINUS_BOOL[user_id] = False


def reset_minus_menu_data(user_id):
    global TRANSACTION_INPUT_MINUS_INT
    global TRANSACTION_INPUT_MINUS_CATEGORY
    global TRANSACTION_INPUT_MINUS_SUB_CATEGORY
    global RULE_INPUT_INT
    RULE_INPUT_INT[user_id] = 'Ввести сумму'
    TRANSACTION_INPUT_MINUS_INT[user_id] = 'Ввести сумму'
    TRANSACTION_INPUT_MINUS_CATEGORY[user_id] = 'Выберите Категорию'
    TRANSACTION_INPUT_MINUS_SUB_CATEGORY[user_id] = 'Выберите ПодКатегорию'


def get_rules_and_cost_string(tg_id) -> str:
    emoji_number_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
    rules_list = data_manager.get_rule(tg_id)
    cost_list = data_manager.get_cost(tg_id)
    unifier: str = ''
    for i in range(len(rules_list)):
        unifier += f'{emoji_number_list[i]} {rules_list[i]} - {cost_list[i]} руб.\n'
    return unifier


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
