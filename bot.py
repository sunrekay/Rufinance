import logging
import data_manager
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
RULE_INPUT_BOOL: bool = False
RULE_INPUT_STR: str

MONEY_INPUT_BOOL: bool = False
MONEY_INPUT_INT: int

TRANSACTION_INPUT_PLUS_BOOL: bool = False
TRANSACTION_INPUT_MINUS_BOOL: bool = False

########################################################################
##                    Основная часть бота                             ##
########################################################################

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    #chart_manager.set_pie_chart(message.chat.id)
    await bot.send_message(message.chat.id,
                           text='Добро пожаловать!',
                           reply_markup=inline_keyboard.START)

    # Ветка с обучением
    # reset_inputs()
    # await message.answer(text=bot_messages.start(),
    #                      reply_markup=inline_keyboard.OKEY_LETS_GO)

# ГЛАВНОЕ МЕНЮ
@dp.callback_query_handler(text='menu')
async def menu(callback_query: types.CallbackQuery):
    reset_inputs()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))

    caption = get_rules_and_cost_string(callback_query.from_user.id)
    last_message = await bot.send_photo(chat_id=callback_query.from_user.id,
                                        photo=chart_manager.get_pie_chart(callback_query.from_user.id),
                                        reply_markup=inline_keyboard.MENU,
                                        caption=caption)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


# МЕНЮ "ТРАНЗАКЦИОННЫЕ ИЗМЕНЕНИЯ" И ЕЕ ВЕТКИ
@dp.callback_query_handler(text='transaction_change')
async def transaction_change_menu(callback_query: types.CallbackQuery):
    reset_inputs()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=service_data_manager.get_last_message_id(callback_query.from_user.id))
    sum_of_plus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                          operation="Доход")
    sum_of_minus = transaction_change_data_manager.sum_of_(tg_id=callback_query.from_user.id,
                                                          operation="Расход")
    text = f'Сумма всех пополнений: {sum_of_plus}\n' \
           f'Сумма всех затрат: {sum_of_minus}\n' \
           f'Баланс: {sum_of_plus-sum_of_minus}'
    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text=text,
                                          reply_markup=inline_keyboard.TRANSACTION_CHANGE_MENU)
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='add_transaction')
async def transaction_change_add_transaction(callback_query: types.CallbackQuery):
    reset_inputs()
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Выберите категорию:',
                                reply_markup=inline_keyboard.TURN_CATEGORY_FOR_ADD)


@dp.callback_query_handler(text='plus_transaction_change')
async def plus_transaction_change(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_PLUS_BOOL
    reset_inputs()
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите название транзакции (НАЗВАНИЕ:СУММА)\nНапример: Подработка:2599',
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)
    TRANSACTION_INPUT_PLUS_BOOL = True


@dp.callback_query_handler(text='minus_transaction_change')
async def minus_transaction_change(callback_query: types.CallbackQuery):
    reset_inputs()
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите название транзакции (НАЗВАНИЕ:СУММА)\nНапример: Продукты:599',
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)


@dp.callback_query_handler(text='transaction_history_plus')
async def transaction_history_plus(callback_query: types.CallbackQuery):
    reset_inputs()
    text = transaction_change_data_manager.get_transactions(tg_id=callback_query.from_user.id,
                                                            operation="Доход")
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=text,
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)


@dp.callback_query_handler(text='transaction_history_minus')
async def transaction_history_plus(callback_query: types.CallbackQuery):
    reset_inputs()
    text = transaction_change_data_manager.get_transactions(tg_id=callback_query.from_user.id,
                                                            operation="Расход")
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=text,
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)


@dp.callback_query_handler(text='transaction_history_all')
async def transaction_history_plus(callback_query: types.CallbackQuery):
    reset_inputs()
    text = transaction_change_data_manager.get_transactions_all(tg_id=callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=text,
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)


# Ветка обучения
@dp.callback_query_handler(text='lets')
async def okey_lets_go(callback_query: types.CallbackQuery):
    reset_inputs()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text='И так давай с тобой создадим правило!',
                           reply_markup=inline_keyboard.CREATE_RULE)


@dp.callback_query_handler(text='create_rule')
async def create_rule(callback_query: types.CallbackQuery):
    global RULE_INPUT_BOOL
    RULE_INPUT_BOOL = True

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=bot_messages.create_rule())


@dp.callback_query_handler(text='next_step')
async def next_step(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=bot_messages.calendar())
######################

@dp.message_handler(content_types='text')
async def input_data(message: types.Message):
    global RULE_INPUT_STR
    global RULE_INPUT_BOOL
    global MONEY_INPUT_INT
    global MONEY_INPUT_BOOL
    global TRANSACTION_INPUT_PLUS_BOOL
    global TRANSACTION_INPUT_MINUS_BOOL

    if RULE_INPUT_BOOL:
        RULE_INPUT_BOOL = False
        RULE_INPUT_STR = message.text

        MONEY_INPUT_BOOL = True
        await message.answer(text='Укажите сумму')

    elif MONEY_INPUT_BOOL:
        MONEY_INPUT_BOOL = False
        try:
            MONEY_INPUT_INT = float(message.text)
            # Добавить в это место функцию записи названия правила и суммы в json
            await message.answer(text='Перейдем к следующему шагу? Или добавим еще правило?',
                                 reply_markup=inline_keyboard.END_TRAINING)
        except:
            MONEY_INPUT_BOOL = True
            await message.answer(text='Введите пожалуйста число')

    elif TRANSACTION_INPUT_PLUS_BOOL or TRANSACTION_INPUT_MINUS_BOOL:
        try:
            data = message.text
            data = data.split(':')
            name = data[0].strip()
            cost = data[1].strip()
            cost = int(cost)

            if TRANSACTION_INPUT_PLUS_BOOL:
                operation = 'Доход'
            elif TRANSACTION_INPUT_MINUS_BOOL:
                operation = 'Расход'

            transaction_change_data_manager.add_record(tg_id=message.chat.id,
                                                       name=name,
                                                       cost=cost,
                                                       operation=operation)
            TRANSACTION_INPUT_PLUS_BOOL = False
            TRANSACTION_INPUT_MINUS_BOOL = False
            await transaction_change_menu(message)

        except:
            await message.answer(text='Введите пожалуйста так, как указано в примере.')

    else:
        await message.answer(text='Я не понимаю.')


########################################################################
##                   Вспомогательные функции                          ##
########################################################################
def reset_inputs():
    global RULE_INPUT_STR
    global RULE_INPUT_BOOL
    global MONEY_INPUT_INT
    global MONEY_INPUT_BOOL
    global TRANSACTION_INPUT_PLUS_BOOL
    global TRANSACTION_INPUT_MINUS_BOOL
    RULE_INPUT_BOOL = False
    RULE_INPUT_STR = ''
    MONEY_INPUT_BOOL = False
    MONEY_INPUT_INT = 0
    TRANSACTION_INPUT_PLUS_BOOL = False
    TRANSACTION_INPUT_MINUS_BOOL = False


def get_rules_and_cost_string(tg_id) -> str:
    rules_list = data_manager.get_rule(tg_id)
    cost_list = data_manager.get_cost(tg_id)
    unifier: str = ''
    for i in range(len(rules_list)):
        unifier += f'{i+1}) {rules_list[i]} - {cost_list[i]} руб.\n'
    return unifier


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
