from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


BTN_OKEY_LETS_GO = InlineKeyboardButton('Поехали!', callback_data='lets')
OKEY_LETS_GO = InlineKeyboardMarkup().add(BTN_OKEY_LETS_GO)

BTN_CREATE_RULE = InlineKeyboardButton('Создать правило', callback_data='create_rule')
CREATE_RULE = InlineKeyboardMarkup().add(BTN_CREATE_RULE)

BTN_NEXT_STEP = InlineKeyboardButton('Следующий шаг', callback_data='next_step')
END_TRAINING = InlineKeyboardMarkup().add(BTN_CREATE_RULE, BTN_NEXT_STEP)
