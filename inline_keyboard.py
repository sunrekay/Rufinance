from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Ветка с обучением
BTN_OKEY_LETS_GO = InlineKeyboardButton('Поехали!', callback_data='lets')
OKEY_LETS_GO = InlineKeyboardMarkup().add(BTN_OKEY_LETS_GO)

BTN_CREATE_RULE = InlineKeyboardButton('Создать правило', callback_data='create_rule')
CREATE_RULE = InlineKeyboardMarkup().add(BTN_CREATE_RULE)

BTN_NEXT_STEP = InlineKeyboardButton('Следующий шаг', callback_data='next_step')
END_TRAINING = InlineKeyboardMarkup().add(BTN_CREATE_RULE, BTN_NEXT_STEP)
######
BTN_START = InlineKeyboardButton('Начать!', callback_data='menu')
START = InlineKeyboardMarkup().add(BTN_START)

# Главное меню
BTN_MY_RULES = InlineKeyboardButton('Мои правила', callback_data='my_rules')
BTN_SLAVE_CALENDAR = InlineKeyboardButton('Календарь обязательств', callback_data='calendar')
BTN_TRANSACTION_CHANGE = InlineKeyboardButton('Транзакционные изменения', callback_data='transaction_change')
MENU = InlineKeyboardMarkup().add(BTN_MY_RULES).add(BTN_SLAVE_CALENDAR).add(BTN_TRANSACTION_CHANGE)

# Меню Транзакционные изменения
BTN_ADD_TRASACTION = InlineKeyboardButton('Добавить транзакцию', callback_data='add_transaction')
BTN_DELETE_TRANSACTION = InlineKeyboardButton('Удалить транзакцию', callback_data='delete_transaction')
BTN_HISTORY_PLUS = InlineKeyboardButton('История "Доход"', callback_data='transaction_history_plus')
BTN_HISTORY_MINUS = InlineKeyboardButton('История "Расход"', callback_data='transaction_history_minus')
BTN_HISTORY_ALL = InlineKeyboardButton('История "Все"', callback_data='transaction_history_all')
BTN_BACK_TO_MENU = InlineKeyboardButton('Назад', callback_data='menu')
TRANSACTION_CHANGE_MENU = InlineKeyboardMarkup().add(BTN_ADD_TRASACTION).add(BTN_DELETE_TRANSACTION)\
    .add(BTN_HISTORY_PLUS).add(BTN_HISTORY_MINUS).add(BTN_HISTORY_ALL).add(BTN_BACK_TO_MENU)


BTN_PLUS = InlineKeyboardButton('Доход', callback_data='plus_transaction_change')
BTN_MINUS = InlineKeyboardButton('Расход', callback_data='minus_transaction_change')
BTN_BACK_TO_TRANSACTION_MENU = InlineKeyboardButton('Назад', callback_data='transaction_change')
TURN_CATEGORY_FOR_ADD = InlineKeyboardMarkup().add(BTN_PLUS, BTN_MINUS).add(BTN_BACK_TO_TRANSACTION_MENU)

BACK_TO_TRANSACTION_MENU = InlineKeyboardMarkup().add(BTN_BACK_TO_TRANSACTION_MENU)