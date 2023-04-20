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


######################################## Ветка обучения ################################################################
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    service_data_manager.update(message.chat.id)
    service_data_manager.add_new_account(message.chat.id)
    service_data_manager.click_counter_plus_one(message.chat.id)
    last_message = await bot.send_message(message.chat.id,
                                          text=bot_messages.start(),
                                          reply_markup=inline_keyboard.START)
    service_data_manager.add_record(message.chat.id, last_message.message_id)


@dp.callback_query_handler(text='training_create_rule')
async def training_create_rule(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=bot_messages.create_rule(),
                                reply_markup=inline_keyboard.TRAINING_CREATE_RULE)
    service_data_manager.set(tg_id=callback_query.from_user.id,
                             key="TRAINIG_DICT_BOOL",
                             value=True)


@dp.callback_query_handler(text='training_calendar')
async def training_calendar(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=bot_messages.calendar(),
                                reply_markup=inline_keyboard.TRAINING_CALENDAR)


@dp.callback_query_handler(text='create_training_calendar')
async def training_create_calendar(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=bot_messages.create_calendar(),
                                reply_markup=inline_keyboard.TRAINING_CREATE_CALENDAR)


@dp.callback_query_handler(text='training_transaction')
async def training_create_transaction(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=bot_messages.transaction(),
                                reply_markup=inline_keyboard.TRAINING_TRANSACTION)


@dp.callback_query_handler(text='create_training_transaction')
async def training_transaction(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=bot_messages.create_transaction())
    service_data_manager.set(tg_id=callback_query.from_user.id, key='TRAINIG_DICT_BOOL', value=False)
    time.sleep(5)
    await menu(callback_query)
########################################################################################################################


# ГЛАВНОЕ МЕНЮ
@dp.callback_query_handler(text='menu')
async def menu(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))
    service_data_manager.update(callback_query.from_user.id)

    sum_of_plus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                          operation="Доход")
    sum_of_minus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                           operation="Расход")
    balance = sum_of_plus - sum_of_minus
    sum_of_pay = sum(data_manager.get_cost(callback_query.from_user.id))

    name = data_manager.get_rule(tg_id=callback_query.from_user.id)
    sum_ = data_manager.get_cost(tg_id=callback_query.from_user.id)
    remains: list = []
    for i in range(len(name)):
        remains.append(sum_[i] - transaction_change_data_manager.category_sum_of_(tg_id=callback_query.from_user.id,
                                                                                  operation="Расход",
                                                                                  category=name[i]))

    last_message = await bot.send_photo(chat_id=callback_query.from_user.id,
                                        photo=chart_manager.get_pie_chart(callback_query.from_user.id),
                                        caption=f'💵БАЛАНС: {balance} (₽)\n'
                                                f'Общая сумма затрат: {sum_of_pay} (₽)\n'
                                                f'Рекомендуемая сумма затрат: {int((balance - sum(remains)) / 30)} (₽) в день'
                                                f' / {balance - sum(remains)} (₽) в месяц ',
                                        reply_markup=inline_keyboard.MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


########################################################################################################################
#                                       Меню "Календарь обязательств"                                                  #
########################################################################################################################
@dp.callback_query_handler(text='calendar_of_commitments')
async def calendar_of_commitments_menu(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))
    service_data_manager.update(callback_query.from_user.id)

    sum_of_plus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                          operation="Доход")
    sum_of_minus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                           operation="Расход")
    balance = sum_of_plus - sum_of_minus
    sum_of_pay = sum(data_manager.get_cost(callback_query.from_user.id))

    name = data_manager.get_rule(tg_id=callback_query.from_user.id)
    sum_ = data_manager.get_cost(tg_id=callback_query.from_user.id)
    remains: list = []
    for i in range(len(name)):
        remains.append(sum_[i] - transaction_change_data_manager.category_sum_of_(tg_id=callback_query.from_user.id,
                                                                                  operation="Расход",
                                                                                  category=name[i]))

    last_message = await bot.send_photo(chat_id=callback_query.from_user.id,
                                        photo=chart_manager.get_calendar_table(callback_query.from_user.id),
                                        caption=f'💵БАЛАНС: {balance} (₽)\n'
                                                f'Общая сумма затрат: {sum_of_pay} (₽)\n'
                                                f'Рекомендуемая сумма затрат: {int((balance-sum(remains))/30)} (₽) в день'
                                                f' / {balance-sum(remains)} (₽) в месяц ',
                                        reply_markup=inline_keyboard.CALENDAR_MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='create_commitment')
async def create_commitment(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    commitment_sum = service_data_manager.get(tg_id=callback_query.from_user.id, key="COMMITMENT_SUM")
    commitment_name = service_data_manager.get(tg_id=callback_query.from_user.id, key="COMMITMENT_NAME")
    commitment_date = service_data_manager.get(tg_id=callback_query.from_user.id, key="COMMITMENT_DATE")

    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Создание обязательства:',
                                          reply_markup=inline_keyboard.create_commitment_menu(f'{commitment_sum} (₽)',
                                                                                              commitment_name,
                                                                                              commitment_date))
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='enter_sum_commitment')
async def enter_sum_commitment(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите cумму (₽):',
                                reply_markup=inline_keyboard.BTN_BACK_TO_CREATE_COMMITMENT_MENU)
    service_data_manager.set(tg_id=callback_query.from_user.id, key='COMMITMENT_SUM_BOOL', value=True)


@dp.callback_query_handler(text='enter_name_of_commitment')
async def enter_name_commitment(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите название:',
                                reply_markup=inline_keyboard.BTN_BACK_TO_CREATE_COMMITMENT_MENU)
    service_data_manager.set(tg_id=callback_query.from_user.id, key='COMMITMENT_NAME_BOOL', value=True)


@dp.callback_query_handler(text='enter_date_of_commitment')
async def enter_date_commitment(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите дату, формата "дд-мм-гггг":',
                                reply_markup=inline_keyboard.BTN_BACK_TO_CREATE_COMMITMENT_MENU)
    service_data_manager.set(tg_id=callback_query.from_user.id, key='COMMITMENT_DATE_BOOL', value=True)


@dp.callback_query_handler(text='save_commitment')
async def enter_date_commitment(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    commitment_sum = service_data_manager.get(tg_id=callback_query.from_user.id, key="COMMITMENT_SUM")
    commitment_name = service_data_manager.get(tg_id=callback_query.from_user.id, key="COMMITMENT_NAME")
    commitment_date = service_data_manager.get(tg_id=callback_query.from_user.id, key="COMMITMENT_DATE")
    trainig_dict_bool = service_data_manager.get(tg_id=callback_query.from_user.id, key="TRAINIG_DICT_BOOL")

    if commitment_sum != 'Ввести сумму'\
        and commitment_name != 'Ввести название'\
        and commitment_date != 'Ввести дату':
        data_manager.add_record(callback_query.from_user.id,
                                cost=commitment_sum,
                                rule=commitment_name,
                                date=commitment_date)
        chart_manager.set_calendar_table(callback_query.from_user.id)
        chart_manager.set_pie_chart(callback_query.from_user.id)
        if trainig_dict_bool:
            await training_create_transaction(callback_query)
        else:
            await calendar_of_commitments_menu(callback_query)
    else:
        await bot.send_message(callback_query.from_user.id, text='Заполните пожалуйста все поля')
        await create_commitment(callback_query.from_user.id)


@dp.callback_query_handler(text='delete_commitment')
async def delete_commitment(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Удаление обязательства:',
                                          reply_markup=inline_keyboard.get_commitment(callback_query.from_user.id))
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text=inline_keyboard.get_index_delete_commitment())
async def delete_commitment(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
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
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))
    service_data_manager.update(callback_query.from_user.id)

    last_message = await bot.send_photo(chat_id=callback_query.from_user.id,
                                        photo=chart_manager.get_my_rules_table(callback_query.from_user.id),
                                        reply_markup=inline_keyboard.MY_RULE_MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='create_rule')
async def create_menu(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    rule_input_int = service_data_manager.get(tg_id=callback_query.from_user.id, key='RULE_INPUT_INT')
    rule_input_str = service_data_manager.get(tg_id=callback_query.from_user.id, key='RULE_INPUT_STR')

    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Создание правила:',
                                          reply_markup=inline_keyboard.create_rule_menu(
                                              category=rule_input_str,
                                              limitation=f'{rule_input_int} (₽)')
                                          )
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='choose_category_rule')
async def choose_category_rule(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите название:',
                                reply_markup=inline_keyboard.BACK_TO_RULE_MENU
                                )
    service_data_manager.set(tg_id=callback_query.from_user.id, key='RULE_INPUT_STR_BOOL', value=True)


@dp.callback_query_handler(text=inline_keyboard.get_rule_category_list())
async def choose_category_rule(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    service_data_manager.set(tg_id=callback_query.from_user.id,
                             key='TRANSACTION_INPUT_MINUS_CATEGORY',
                             value=inline_keyboard.rule_translate_key(callback_query.data))
    await create_menu(callback_query)


@dp.callback_query_handler(text='enter_limitation_rule')
async def choose_category_rule(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите ограничение (₽):',
                                reply_markup=inline_keyboard.BACK_TO_RULE_MENU
                                )
    service_data_manager.set(tg_id=callback_query.from_user.id, key='RULE_INPUT_BOOL', value=True)


@dp.callback_query_handler(text='save_rule')
async def save_rule(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    rule_input_int = service_data_manager.get(tg_id=callback_query.from_user.id, key='RULE_INPUT_INT')
    rule_input_str = service_data_manager.get(tg_id=callback_query.from_user.id, key='RULE_INPUT_STR')
    training_dict_bool = service_data_manager.get(tg_id=callback_query.from_user.id, key='TRAINIG_DICT_BOOL')

    if rule_input_int != "Ввести сумму" and\
            rule_input_str != "Ввести название":
        my_rules_manager.add_record(tg_id=callback_query.from_user.id,
                                    category=rule_input_str,
                                    cost=rule_input_int)
        chart_manager.set_my_rules_table(telegram_id=callback_query.from_user.id)
        if training_dict_bool:
            await training_calendar(callback_query)
        else:
            await my_rule_menu(callback_query)
    else:
        await bot.send_message(callback_query.from_user.id, text='Заполните пожалуйста все поля')
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
    chart_manager.set_calendar_table(callback_query.from_user.id)
    chart_manager.set_pie_chart(callback_query.from_user.id)
    await my_rule_menu(callback_query)
########################################################################################################################
#                                       Конец Меню "Мои Правила"                                                       #
########################################################################################################################


########################################################################################################################
#                                        Меню "Транзакционные изменения"                                               #
########################################################################################################################
@dp.callback_query_handler(text='transaction_change')
async def transaction_change_menu(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
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
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    transaction_input_minus_int = service_data_manager.get(tg_id=callback_query.from_user.id,
                                                           key='TRANSACTION_INPUT_MINUS_INT')
    transaction_input_minus_category = service_data_manager.get(tg_id=callback_query.from_user.id,
                                                                key='TRANSACTION_INPUT_MINUS_CATEGORY')
    transaction_input_operation = service_data_manager.get(tg_id=callback_query.from_user.id,
                                                           key='TRANSACTION_INPUT_OPERATION')

    await bot.delete_message(callback_query.from_user.id,
                             service_data_manager.get_last_message_id(callback_query.from_user.id))
    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Заполните поля:',
                                          reply_markup=inline_keyboard.enter_minus_menu(
                                              f'{transaction_input_minus_int} (₽)',
                                              transaction_input_minus_category,
                                              transaction_input_operation)
                                          )
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='enter_minus')
async def enter_minus(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите число:',
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)
    service_data_manager.set(tg_id=callback_query.from_user.id, key='TRANSACTION_INPUT_MINUS_BOOL', value=True)


@dp.callback_query_handler(text='choose_category')
async def choose_category(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите название:',
                                reply_markup=inline_keyboard.CATEGORIES_MENU)
    service_data_manager.set(tg_id=callback_query.from_user.id, key='TRANSACTION_INPUT_CATEGORY_BOOL', value=True)


@dp.callback_query_handler(text='choose_operation')
async def choose_category(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Выберите операцию:',
                                reply_markup=inline_keyboard.CHOOSE_OPERATION)


@dp.callback_query_handler(text=inline_keyboard.get_list_callback_operations())
async def choose_category(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    operation = inline_keyboard.get_translate_list_callback_operation(callback_query.data)
    service_data_manager.set(tg_id=callback_query.from_user.id, key='TRANSACTION_INPUT_OPERATION', value=operation)
    await transaction_change_add_transaction(callback_query)


@dp.callback_query_handler(text='save_minus_choose')
async def save_minus_choose(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    transaction_input_minus_int = service_data_manager.get(tg_id=callback_query.from_user.id,
                                                           key='TRANSACTION_INPUT_MINUS_INT')
    transaction_input_minus_category = service_data_manager.get(tg_id=callback_query.from_user.id,
                                                                key='TRANSACTION_INPUT_MINUS_CATEGORY')
    transaction_input_operation = service_data_manager.get(tg_id=callback_query.from_user.id,
                                                           key='TRANSACTION_INPUT_OPERATION')
    training_dict_bool = service_data_manager.get(tg_id=callback_query.from_user.id,
                                                  key='TRAINIG_DICT_BOOL')

    if transaction_input_minus_int == 'Ввести сумму'\
        or transaction_input_minus_category == 'Ввести название'\
        or transaction_input_operation == 'Выберите операцию':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Заполните пожалуйста все поля')
    else:
        transaction_change_data_manager.add_record(tg_id=callback_query.from_user.id,
                                                   name=transaction_input_minus_category,
                                                   cost=transaction_input_minus_int,
                                                   operation=transaction_input_operation)
        chart_manager.set_my_rules_table(telegram_id=callback_query.from_user.id)
        chart_manager.set_calendar_table(telegram_id=callback_query.from_user.id)
        chart_manager.set_pie_chart(telegram_id=callback_query.from_user.id)
        if training_dict_bool:
            await training_transaction(callback_query)
        else:
            await transaction_change_menu(callback_query)


@dp.callback_query_handler(text='transaction_history_all')
async def transaction_history_all(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    text = transaction_change_data_manager.get_transactions_all(tg_id=callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=text,
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)


@dp.callback_query_handler(text='delete_transaction')
async def delete_transaction(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Какие транзакции удалить?',
                                reply_markup=inline_keyboard.get_transaction_list(callback_query.from_user.id))


@dp.callback_query_handler(text=inline_keyboard.get_index_transaction_delete())
async def delete_transaction(callback_query: types.CallbackQuery):
    service_data_manager.click_counter_plus_one(callback_query.from_user.id)
    transaction_change_data_manager.delete_record(tg_id=callback_query.from_user.id,
                                                  index=int(callback_query.data.replace('_transaction', '')))
    chart_manager.set_my_rules_table(callback_query.from_user.id)
    await transaction_change_menu(callback_query)
########################################################################################################################
#                                       Конец Меню "Транзакционные изменения"                                          #
########################################################################################################################


@dp.message_handler(content_types='text')
async def input_data(message: types.Message):
    service_data_manager.click_counter_plus_one(message.chat.id)
    rule_input_str_bool = service_data_manager.get(tg_id=message.chat.id, key='RULE_INPUT_STR_BOOL')
    rule_input_bool = service_data_manager.get(tg_id=message.chat.id, key='RULE_INPUT_BOOL')

    transaction_input_minus_bool = service_data_manager.get(tg_id=message.chat.id, key='TRANSACTION_INPUT_MINUS_BOOL')
    transaction_input_category_bool = service_data_manager.get(tg_id=message.chat.id, key='TRANSACTION_INPUT_CATEGORY_BOOL')

    commitment_sum_bool = service_data_manager.get(tg_id=message.chat.id, key='COMMITMENT_SUM_BOOL')
    commitment_name_bool = service_data_manager.get(tg_id=message.chat.id, key='COMMITMENT_NAME_BOOL')
    commitment_date_bool = service_data_manager.get(tg_id=message.chat.id, key='COMMITMENT_DATE_BOOL')

    if rule_input_bool:
        service_data_manager.set(tg_id=message.chat.id, key='RULE_INPUT_INT', value=message.text)
        service_data_manager.set(tg_id=message.chat.id, key='RULE_INPUT_BOOL', value=False)
        await create_menu(message)

    elif rule_input_str_bool:
        service_data_manager.set(tg_id=message.chat.id, key='RULE_INPUT_STR', value=message.text)
        service_data_manager.set(tg_id=message.chat.id, key='RULE_INPUT_STR_BOOL', value=False)
        await create_menu(message)

    elif transaction_input_minus_bool:
        try:
            data = message.text
            service_data_manager.set(tg_id=message.chat.id, key='TRANSACTION_INPUT_MINUS_INT', value=int(data))
            service_data_manager.set(tg_id=message.chat.id, key='TRANSACTION_INPUT_MINUS_BOOL', value=False)
            await transaction_change_add_transaction(message)
        except:
            await message.answer(text='Введите пожалуйста так, как указано в примере.')

    elif transaction_input_category_bool:
        data = message.text
        service_data_manager.set(tg_id=message.chat.id, key='TRANSACTION_INPUT_MINUS_CATEGORY', value=data)
        service_data_manager.set(tg_id=message.chat.id, key='TRANSACTION_INPUT_CATEGORY_BOOL', value=False)
        await transaction_change_add_transaction(message)

    elif commitment_sum_bool:
        try:
            data = message.text
            service_data_manager.set(tg_id=message.chat.id, key='COMMITMENT_SUM', value=int(data))
            service_data_manager.set(tg_id=message.chat.id, key='COMMITMENT_SUM_BOOL', value=False)
            await create_commitment(message)
        except:
            await message.answer(text='Введите пожалуйсто число')

    elif commitment_name_bool:
        data = message.text
        service_data_manager.set(tg_id=message.chat.id, key='COMMITMENT_NAME', value=data)
        service_data_manager.set(tg_id=message.chat.id, key='COMMITMENT_NAME_BOOL', value=False)
        await create_commitment(message)

    elif commitment_date_bool:
            try:
                data = message.text
                date = data.split('-')
                if (0 < int(date[0]) <= 31) and (0 < int(date[1]) <= 12) and (2023 <= int(date[2]) <= 2300):
                    service_data_manager.set(tg_id=message.chat.id, key='COMMITMENT_DATE', value=data)
                    service_data_manager.set(tg_id=message.chat.id, key='COMMITMENT_DATE_BOOL', value=False)
                    await create_commitment(message)
            except:
                await message.answer(text='Введите пожалуйста так, как указано в примере')

    else:
        await message.answer(text='Я не понимаю.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
