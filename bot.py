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

TRANSACTION_INPUT_MINUS_INT: int = 'Ввести сумму'
TRANSACTION_INPUT_MINUS_CATEGORY: str = 'Выберите Категорию'
TRANSACTION_INPUT_MINUS_SUB_CATEGORY: str = 'Выберите ПодКатегорию'

########################################################################
##                    Основная часть бота                             ##
########################################################################

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    #chart_manager.set_pie_chart(message.chat.id)
    last_message = await bot.send_message(message.chat.id,
                                          text='Добро пожаловать!',
                                          reply_markup=inline_keyboard.START)
    service_data_manager.add_record(message.chat.id, message.message_id)
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
    reset_minus_menu_data()
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
                                text='Выберите "Доход" или "Расход":',
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


# Ветка ввода "Расход"
@dp.callback_query_handler(text='minus_transaction_change')
async def minus_transaction_change(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_INT
    global TRANSACTION_INPUT_MINUS_CATEGORY
    global TRANSACTION_INPUT_MINUS_SUB_CATEGORY
    await bot.delete_message(callback_query.from_user.id,
                             service_data_manager.get_last_message_id(callback_query.from_user.id))
    last_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Внести "Расход":',
                                          reply_markup=inline_keyboard.enter_minus_menu(TRANSACTION_INPUT_MINUS_INT,
                                                                                        TRANSACTION_INPUT_MINUS_CATEGORY,
                                                                                        TRANSACTION_INPUT_MINUS_SUB_CATEGORY)
                                          )
    service_data_manager.add_record(callback_query.from_user.id, last_message.message_id)


@dp.callback_query_handler(text='enter_minus')
async def enter_minus(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_BOOL
    reset_inputs()
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Введите число:',
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)
    TRANSACTION_INPUT_MINUS_BOOL = True


@dp.callback_query_handler(text='choose_category')
async def choose_category(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text='Выберите Категорию:',
                                reply_markup=inline_keyboard.CATEGORIES_MENU)


@dp.callback_query_handler(text=inline_keyboard.get_category_list())
async def category_list(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_CATEGORY
    TRANSACTION_INPUT_MINUS_CATEGORY = inline_keyboard.translate_key(callback_query.data)
    await minus_transaction_change(callback_query)


@dp.callback_query_handler(text='choose_sub_category')
async def choose_sub_category(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_CATEGORY
    if TRANSACTION_INPUT_MINUS_CATEGORY == 'Выберите Категорию':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Сначала выберите Категорию')
    else:
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                    text='Выберите ПодКатегорию:',
                                    reply_markup=inline_keyboard.get_sub_category_BTNS(TRANSACTION_INPUT_MINUS_CATEGORY))


@dp.callback_query_handler(text=inline_keyboard.get_sub_category_list())
async def sub_category_list(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_SUB_CATEGORY
    TRANSACTION_INPUT_MINUS_SUB_CATEGORY = inline_keyboard.translate_sub_key(callback_query.data)
    await minus_transaction_change(callback_query)


@dp.callback_query_handler(text='save_minus_choose')
async def save_minus_choose(callback_query: types.CallbackQuery):
    global TRANSACTION_INPUT_MINUS_INT
    global TRANSACTION_INPUT_MINUS_CATEGORY
    global TRANSACTION_INPUT_MINUS_SUB_CATEGORY

    if TRANSACTION_INPUT_MINUS_INT == 'Ввести сумму'\
        or TRANSACTION_INPUT_MINUS_CATEGORY == 'Выберите Категорию'\
        or TRANSACTION_INPUT_MINUS_SUB_CATEGORY == 'Выберите ПодКатегорию':
        bot.send_message(chat_id=callback_query.from_user.id,
                         text='Заполните пожалуйста все поля')
    else:
        transaction_change_data_manager.add_record(tg_id=callback_query.from_user.id,
                                                   name=f'{TRANSACTION_INPUT_MINUS_CATEGORY}({TRANSACTION_INPUT_MINUS_SUB_CATEGORY})',
                                                   cost=TRANSACTION_INPUT_MINUS_INT,
                                                   operation='Расход')
        await transaction_change_menu(callback_query)


######################

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
async def transaction_history_all(callback_query: types.CallbackQuery):
    reset_inputs()
    text = transaction_change_data_manager.get_transactions_all(tg_id=callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=service_data_manager.get_last_message_id(callback_query.from_user.id),
                                text=text,
                                reply_markup=inline_keyboard.BACK_TO_TRANSACTION_MENU)
# КОНЕЦ ВЕТКИ "ТРАНЗАКЦИОННЫЕ ИЗМЕНЕНИЯ"


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
    global TRANSACTION_INPUT_MINUS_INT

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

    elif TRANSACTION_INPUT_PLUS_BOOL:
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
            TRANSACTION_INPUT_PLUS_BOOL = False
            await transaction_change_menu(message)

        except:
            await message.answer(text='Введите пожалуйста так, как указано в примере.')

    elif TRANSACTION_INPUT_MINUS_BOOL:
        try:
            data = message.text
            TRANSACTION_INPUT_MINUS_INT = int(data)
            await minus_transaction_change(message)
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


def reset_minus_menu_data():
    global TRANSACTION_INPUT_MINUS_INT
    global TRANSACTION_INPUT_MINUS_CATEGORY
    global TRANSACTION_INPUT_MINUS_SUB_CATEGORY
    TRANSACTION_INPUT_MINUS_INT = 'Ввести сумму'
    TRANSACTION_INPUT_MINUS_CATEGORY = 'Выберите Категорию'
    TRANSACTION_INPUT_MINUS_SUB_CATEGORY = 'Выберите ПодКатегорию'


def get_rules_and_cost_string(tg_id) -> str:
    rules_list = data_manager.get_rule(tg_id)
    cost_list = data_manager.get_cost(tg_id)
    unifier: str = ''
    for i in range(len(rules_list)):
        unifier += f'{i+1}) {rules_list[i]} - {cost_list[i]} руб.\n'
    return unifier


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
