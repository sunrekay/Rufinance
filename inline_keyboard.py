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

# Внести затраты меню
def enter_minus_menu(enter_minus: str = 'Ввести сумму', choose_category: str = 'Выберите Категорию',
                     choose_sub_category: str = 'Выберите Подкатегорию'):
    BTN_ENRER_MINUS = InlineKeyboardButton(enter_minus, callback_data='enter_minus')
    BTN_CHOOSE_CATEGORY = InlineKeyboardButton(choose_category, callback_data='choose_category')
    BTN_CHOOSE_SUB_CATEGORY = InlineKeyboardButton(choose_sub_category, callback_data='choose_sub_category')
    BTN_SAVE_MINUS_CHOOSE = InlineKeyboardButton('Сохранить', callback_data='save_minus_choose')

    ENTER_DATA_MINUS_MENU = InlineKeyboardMarkup().add(BTN_ENRER_MINUS).add(BTN_CHOOSE_CATEGORY).add(BTN_CHOOSE_SUB_CATEGORY)\
        .add(BTN_SAVE_MINUS_CHOOSE).add(BTN_BACK_TO_TRANSACTION_MENU)
    return ENTER_DATA_MINUS_MENU


# Кнопки Категорий
def get_category_list():
    return ['category_nutrion', 'category_credits', 'category_home', 'category_car', 'category_health',
            'category_clothes', 'category_public_transport', 'category_recreation_and_entertaiment',
            'category_education']
def translate_key(key):
    keys = { 'category_nutrion': 'Питание',
             'category_credits': 'Кредиты',
             'category_home': 'Дом',
             'category_car': 'Машина',
             'category_health': 'Здоровье',
             'category_clothes': 'Одежда',
             'category_public_transport': 'Общественный транспорт',
             'category_recreation_and_entertaiment': 'Отдых и развлечения',
             'category_education': 'Образование'}
    return keys[key]

BTN_CATEGORY_NUTRION = InlineKeyboardButton('Питание', callback_data='category_nutrion')
BTN_CATEGORY_CREDITS = InlineKeyboardButton('Кредиты', callback_data='category_credits')
BTN_CATEGORY_HOME = InlineKeyboardButton('Дом', callback_data='category_home')
BTN_CATEGORY_CAR = InlineKeyboardButton('Машина', callback_data='category_car')
BTN_CATEGORY_HEALTH = InlineKeyboardButton('Здоровье', callback_data='category_health')
BTN_CATEGORY_CLOTHES = InlineKeyboardButton('Одежда', callback_data='category_clothes')
BTN_CATEGORY_PUBLIC_TRANSPORT = InlineKeyboardButton('Общественный транспорт',
                                                     callback_data='category_public_transport')
BTN_CATEGORY_RECREATION_AND_ENTERTAIMENT = InlineKeyboardButton('Отдых и развлечения',
                                                                callback_data='category_recreation_and_entertaiment')
BTN_CATEGORY_EDUCATION = InlineKeyboardButton('Образование', callback_data='category_education')
BTN_BACK_TO_ENTER_DATA_MINUS_MENU = InlineKeyboardButton('Назад', callback_data='minus_transaction_change')

CATEGORIES_MENU = InlineKeyboardMarkup().add(BTN_CATEGORY_NUTRION).add(BTN_CATEGORY_CREDITS).add(BTN_CATEGORY_HOME)\
    .add(BTN_CATEGORY_CAR).add(BTN_CATEGORY_HEALTH).add(BTN_CATEGORY_CLOTHES).add(BTN_CATEGORY_PUBLIC_TRANSPORT)\
    .add(BTN_CATEGORY_RECREATION_AND_ENTERTAIMENT).add(BTN_CATEGORY_EDUCATION).add(BTN_BACK_TO_ENTER_DATA_MINUS_MENU)

# Список ПодКатегорий
def get_sub_category_list(category: str):
    if category == 'Питание':
        nutrion_callback_data_sub_category_list = ['products', 'food_at_work', 'school_breakfast', 'fastfood']
        return nutrion_callback_data_sub_category_list

    if category == 'Кредиты':
        pass

    if category == 'Дом':
        pass

    if category == 'Машина':
        pass

    if category == 'Здоровье':
        pass

    if category == 'Одежда':
        pass

    if category == 'Общественный транспорт':
        pass

    if category == 'Отдых и развлечения':
        pass

    if category == 'Образование':
        pass

def get_sub_category_BTNS(category: str):
    SUB_CATEGORIES_MENU = InlineKeyboardMarkup()
    if category == 'Питание':
        nutrion_sub_category_list = ['Продукты', 'Еда на работе', 'Школные завтраки', 'Фастфуд']
        nutrion_callback_data_sub_category_list = ['products', 'food_at_work', 'school_breakfast', 'fastfood']

        for i in range(len(nutrion_sub_category_list)):
            SUB_CATEGORIES_MENU.add(InlineKeyboardButton(nutrion_sub_category_list[i],
                                                         callback_data=nutrion_callback_data_sub_category_list[i]))
        SUB_CATEGORIES_MENU.add(BTN_BACK_TO_ENTER_DATA_MINUS_MENU)
        return SUB_CATEGORIES_MENU

    if category == 'Кредиты':
        pass
    if category == 'Дом':
        pass
    if category == 'Машина':
        pass
    if category == 'Здоровье':
        pass
    if category == 'Одежда':
        pass
    if category == 'Общественный транспорт':
        pass
    if category == 'Отдых и развлечения':
        pass
    if category == 'Образование':
        pass

def translate_sub_key(sub_category: str):
    sub_category_dict = {
        'products': 'Продукты',
        'food_at_work': 'Еда на работе',
        'school_breakfast': 'Школные завтраки',
        'fastfood': 'Фастфуд'
    }
    return sub_category_dict[sub_category]