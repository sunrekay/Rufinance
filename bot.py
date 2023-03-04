import logging
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

########################################################################
##                    Основная часть бота                             ##
########################################################################


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # await bot.send_photo(chat_id=message.from_user.id,
    #                      photo=chart_manager.get_pie_chart(message.chat.id))
    await message.answer_photo(chart_manager.get_pie_chart(message.chat.id))
    # Ветка с обучением
    # reset_inputs()
    # await message.answer(text=bot_messages.start(),
    #                      reply_markup=inline_keyboard.OKEY_LETS_GO)


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


@dp.message_handler(content_types='text')
async def input_data(message: types.Message):
    global RULE_INPUT_STR
    global RULE_INPUT_BOOL
    global MONEY_INPUT_INT
    global MONEY_INPUT_BOOL

    if RULE_INPUT_BOOL:
        RULE_INPUT_BOOL = False
        RULE_INPUT_STR = message.text

        MONEY_INPUT_BOOL = True
        await message.answer(text='Укажите сумму')

    elif MONEY_INPUT_BOOL:
        MONEY_INPUT_BOOL = False
        try:
            MONEY_INPUT_INT = int(message.text)
            # Добавить в это место функцию записи названия правила и суммы в json
            await message.answer(text='Перейдем к следующему шагу? Или добавим еще правило?',
                                 reply_markup=inline_keyboard.END_TRAINING)
        except:
            MONEY_INPUT_BOOL = True
            await message.answer(text='Введите пожалуйста число')

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
    RULE_INPUT_BOOL = False
    RULE_INPUT_STR = ''
    MONEY_INPUT_BOOL = False
    MONEY_INPUT_INT = 0


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
