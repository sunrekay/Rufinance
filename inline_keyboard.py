import pytz
import my_rules_manager
from datetime import datetime
import transaction_change_data_manager
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import data_manager

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
BTN_SLAVE_CALENDAR = InlineKeyboardButton('Календарь обязательств', callback_data='calendar_of_commitments')
BTN_TRANSACTION_CHANGE = InlineKeyboardButton('Транзакционные изменения', callback_data='transaction_change')
MENU = InlineKeyboardMarkup().add(BTN_MY_RULES).add(BTN_SLAVE_CALENDAR).add(BTN_TRANSACTION_CHANGE)


########################################################################################################################
#                                        Меню "Транзакционные изменения"                                               #
########################################################################################################################
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
BTN_BACK_TO_TRANSACTION_MENU = InlineKeyboardButton('❌', callback_data='transaction_change')
TURN_CATEGORY_FOR_ADD = InlineKeyboardMarkup().add(BTN_PLUS, BTN_MINUS).add(BTN_BACK_TO_TRANSACTION_MENU)

BACK_TO_TRANSACTION_MENU = InlineKeyboardMarkup().add(BTN_BACK_TO_TRANSACTION_MENU)


def get_transaction_list(tg_id: str):
    dates = transaction_change_data_manager.get_date(tg_id)
    operations = transaction_change_data_manager.get_operation(tg_id)
    names = transaction_change_data_manager.get_name(tg_id)
    costs = transaction_change_data_manager.get_cost(tg_id)

    date = datetime.now(pytz.timezone('Europe/Moscow'))
    date = date.strftime("%m-%Y")
    DELETE_LIST = InlineKeyboardMarkup()
    for i in range(len(dates)):
        if date in dates[i]:
            DELETE_LIST.add(InlineKeyboardButton(f'[{dates[i]}][{operations[i]}]{names[i]}: {costs[i]} (₽)', callback_data=f'{i}_transaction'))
    DELETE_LIST.add(InlineKeyboardButton('❌', callback_data='transaction_change'))
    return DELETE_LIST


def get_index_transaction_delete():
    _list = []
    for i in range(50):
        _list.append(f'{i}_transaction')
    return _list


def enter_minus_menu(enter_minus: str, choose_category: str, choose_sub_category: str):
    BTN_ENRER_MINUS = InlineKeyboardButton(enter_minus, callback_data='enter_minus')
    BTN_CHOOSE_CATEGORY = InlineKeyboardButton(choose_category, callback_data='choose_category')
    BTN_CHOOSE_SUB_CATEGORY = InlineKeyboardButton(choose_sub_category, callback_data='choose_sub_category')
    BTN_SAVE_MINUS_CHOOSE = InlineKeyboardButton('✅', callback_data='save_minus_choose')

    ENTER_DATA_MINUS_MENU = InlineKeyboardMarkup().add(BTN_ENRER_MINUS).add(BTN_CHOOSE_CATEGORY).add(BTN_CHOOSE_SUB_CATEGORY)\
        .add(BTN_BACK_TO_TRANSACTION_MENU, BTN_SAVE_MINUS_CHOOSE)
    return ENTER_DATA_MINUS_MENU


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


def get_sub_category_list():
    return ['products',
            'food_at_work',
            'school_breakfast',
            'fastfood',
            'pay_for_credit',
            'pay_for_house_credit',
            'early_repayment',
            'percentages',
            'rent',
            'ZHKH',
            'household_expenses',
            'gas',
            'clean',
            'repair',
            'insurance',
            'parking',
            'another_money_lose',
            'medicine',
            'beauty_place',
            'cosmetic',
            'perfumery',
            'barber_shop',
            'clothes',
            'shoes',
            'accessories',
            'decorating',
            'atelier',
            'dry_cleaning',
            'metro',
            'taxi',
            'proezd',
            'books',
            'cafe',
            'movie',
            'theatre',
            'exhibitions',
            'bowling',
            'study_books',
            'pay_for_study',
            'tutor']


def get_sub_category_BTNS(category: str):
    if category == 'Питание':
        sub_category_list = ['Продукты',
                             'Еда на работе',
                             'Школные завтраки',
                             'Фастфуд']
        callback_data_sub_category_list = ['products',
                                           'food_at_work',
                                           'school_breakfast',
                                           'fastfood']

    if category == 'Кредиты':
        sub_category_list = ['Выплата по Кредиту',
                             'Выплата по Ипотеке',
                             'Досрочное погашение долга',
                             'Покрытие процентов']
        callback_data_sub_category_list = ['pay_for_credit',
                                           'pay_for_house_credit',
                                           'early_repayment',
                                           'percentages']

    if category == 'Дом':
        sub_category_list = ['Аренда',
                             'ЖКХ',
                             'Бытовые расходы для дома']
        callback_data_sub_category_list = ['rent',
                                           'ZHKH',
                                           'household_expenses']

    if category == 'Машина':
        sub_category_list = ['Бензин',
                             'Мойка',
                             'Ремонт',
                             'Страховка',
                             'Парковка',
                             'Другие расходы']
        callback_data_sub_category_list = ['gas',
                                           'clean',
                                           'repair',
                                           'insurance',
                                           'parking',
                                           'another_money_lose']

    if category == 'Здоровье':
        sub_category_list = ['Лекарства',
                             'Салон красоты',
                             'Косметика',
                             'Парфюмерия',
                             'Услуга парикмахера']
        callback_data_sub_category_list = ['medicine',
                                           'beauty_place',
                                           'cosmetic',
                                           'perfumery',
                                           'barber_shop']

    if category == 'Одежда':
        sub_category_list = ['Одежда',
                             'Обувь',
                             'Аксессуары',
                             'Украшения',
                             'Ателье',
                             'Химчистка']
        callback_data_sub_category_list = ['clothes',
                                           'shoes',
                                           'accessories',
                                           'decorating',
                                           'atelier',
                                           'dry_cleaning']

    if category == 'Общественный транспорт':
        sub_category_list = ['Метро',
                             'Такси',
                             'Проездные']
        callback_data_sub_category_list = ['metro',
                                           'taxi',
                                           'proezd']

    if category == 'Отдых и развлечения':
        sub_category_list = ['Книги',
                             'Кафе и рестораны',
                             'Кино',
                             'Театр',
                             'Выставки',
                             'Боулинг']
        callback_data_sub_category_list = ['books',
                                           'cafe',
                                           'movie',
                                           'theatre',
                                           'exhibitions',
                                           'bowling']

    if category == 'Образование':
        sub_category_list = ['Учебники',
                             'Плата за обучение',
                             'Репетитор']
        callback_data_sub_category_list = ['study_books',
                                           'pay_for_study',
                                           'tutor']

    SUB_CATEGORIES_MENU = InlineKeyboardMarkup()
    for i in range(len(sub_category_list)):
        SUB_CATEGORIES_MENU.add(InlineKeyboardButton(sub_category_list[i],
                                                     callback_data=callback_data_sub_category_list[i]))
    SUB_CATEGORIES_MENU.add(BTN_BACK_TO_ENTER_DATA_MINUS_MENU)
    return SUB_CATEGORIES_MENU


def translate_sub_key(sub_category: str):
    sub_category_dict = {
        'products': 'Продукты',
        'food_at_work': 'Еда на работе',
        'school_breakfast': 'Школные завтраки',
        'fastfood': 'Фастфуд',
        'pay_for_credit': 'Выплата по Кредиту',
        'pay_for_house_credit': 'Выплата по Ипотеке',
        'early_repayment': 'Досрочное погашение долга',
        'percentages': 'Покрытие процентов',
        'rent': 'Аренда',
        'ZHKH': 'ЖКХ',
        'household_expenses': 'Бытовые расходы для дома',
        'gas': 'Бензин',
        'clean': 'Мойка',
        'repair': 'Ремонт',
        'insurance': 'Страховка',
        'parking': 'Парковка',
        'another_money_lose': 'Другие расходы',
        'medicine': 'Лекарства',
        'beauty_place': 'Салон красоты',
        'cosmetic': 'Косметика',
        'perfumery': 'Парфюмерия',
        'barber_shop': 'Услуга парикмахера',
        'clothes': 'Одежда',
        'shoes': 'Обувь',
        'accessories': 'Аксессуары',
        'decorating': 'Украшения',
        'atelier': 'Ателье',
        'dry_cleaning': 'Химчистка',
        'metro': 'Метро',
        'taxi': 'Такси',
        'proezd': 'Проездные',
        'books': 'Книги',
        'cafe': 'Кафе и рестораны',
        'movie': 'Кино',
        'theatre': 'Театр',
        'exhibitions': 'Выставки',
        'bowling': 'Боулинг',
        'study_books': 'Учебники',
        'pay_for_study': 'Плата за обучение',
        'tutor': 'Репетитор'
    }
    return sub_category_dict[sub_category]
########################################################################################################################
#                                       Конец Меню "Транзакционные изменения"                                          #
########################################################################################################################


########################################################################################################################
#                                        Меню "Мои Правила"                                                            #
########################################################################################################################
BTN_CREATE_RULE = InlineKeyboardButton('Создать правило', callback_data='create_rule')
BTN_DELETE_RULE = InlineKeyboardButton('Удалить правило', callback_data='delete_rule')
MY_RULE_MENU = InlineKeyboardMarkup().add(BTN_CREATE_RULE).add(BTN_DELETE_RULE).add(BTN_BACK_TO_MENU)


def create_rule_menu(category: str, limitation: str):
    BTN_CHOOSE_CATEGORY_RULE = InlineKeyboardButton(category, callback_data='choose_category_rule')
    BTN_ENTER_LIMITATION_RULE = InlineKeyboardButton(limitation, callback_data='enter_limitation_rule')
    BTN_SAVE_RULE = InlineKeyboardButton('Сохранить', callback_data='save_rule')
    BTN_BACK_TO_RULE_MENU = InlineKeyboardButton('Назад', callback_data='my_rules')
    CREATE_RULE = InlineKeyboardMarkup().add(BTN_ENTER_LIMITATION_RULE).add(BTN_CHOOSE_CATEGORY_RULE) \
        .add(BTN_SAVE_RULE).add(BTN_BACK_TO_RULE_MENU)
    return CREATE_RULE


BTN_RULE_CATEGORY_NUTRION = InlineKeyboardButton('Питание', callback_data='rule_category_nutrion')
BTN_RULE_CATEGORY_CREDITS = InlineKeyboardButton('Кредиты', callback_data='rule_category_credits')
BTN_RULE_CATEGORY_HOME = InlineKeyboardButton('Дом', callback_data='rule_category_home')
BTN_RULE_CATEGORY_CAR = InlineKeyboardButton('Машина', callback_data='rule_category_car')
BTN_RULE_CATEGORY_HEALTH = InlineKeyboardButton('Здоровье', callback_data='rule_category_health')
BTN_RULE_CATEGORY_CLOTHES = InlineKeyboardButton('Одежда', callback_data='rule_category_clothes')
BTN_RULE_CATEGORY_PUBLIC_TRANSPORT = InlineKeyboardButton('Общественный транспорт',
                                                     callback_data='rule_category_public_transport')
BTN_RULE_CATEGORY_RECREATION_AND_ENTERTAIMENT = InlineKeyboardButton('Отдых и развлечения',
                                                                callback_data='rule_category_recreation_and_entertaiment')
BTN_RULE_CATEGORY_EDUCATION = InlineKeyboardButton('Образование', callback_data='rule_category_education')
BTN_BACK_TO_RULE_MENU = InlineKeyboardButton('Назад', callback_data='create_rule')

BACK_TO_RULE_MENU = InlineKeyboardMarkup().add(BTN_BACK_TO_RULE_MENU)
RULE_CATEGORIES_MENU = InlineKeyboardMarkup().add(BTN_RULE_CATEGORY_NUTRION)\
    .add(BTN_RULE_CATEGORY_HOME).add(BTN_RULE_CATEGORY_CAR).add(BTN_RULE_CATEGORY_HEALTH)\
    .add(BTN_RULE_CATEGORY_CLOTHES).add(BTN_RULE_CATEGORY_PUBLIC_TRANSPORT)\
    .add(BTN_RULE_CATEGORY_RECREATION_AND_ENTERTAIMENT).add(BTN_RULE_CATEGORY_EDUCATION)\
    .add(BTN_BACK_TO_RULE_MENU)


def ger_list_of_btn_rule(tg_id: str):
    global BTN_BACK_TO_RULE_MENU
    rules = my_rules_manager.get_categories(tg_id)
    DELETE_LIST = InlineKeyboardMarkup()
    for i in range(len(rules)):
        BTN_RULE = InlineKeyboardButton(rules[i], callback_data=f'{i}_rule')
        DELETE_LIST.add(BTN_RULE)
    DELETE_LIST.add(InlineKeyboardButton('Назад', callback_data='my_rules'))
    return DELETE_LIST


def get_index_list_delete():
    return ['0_rule', '1_rule', '2_rule', '3_rule', '4_rule', '5_rule', '6_rule', '7_rule',
            '8_rule', '9_rule', '10_rule', '11_rule', '12_rule', '13_rule', '14_rule', '15_rule']


def get_rule_category_list():
    return ['rule_category_nutrion', 'rule_category_credits', 'rule_category_home', 'rule_category_car',
            'rule_category_health', 'rule_category_clothes', 'rule_category_public_transport',
            'rule_category_recreation_and_entertaiment', 'rule_category_education']


def rule_translate_key(key):
    keys = { 'rule_category_nutrion': 'Питание',
             'rule_category_credits': 'Кредиты',
             'rule_category_home': 'Дом',
             'rule_category_car': 'Машина',
             'rule_category_health': 'Здоровье',
             'rule_category_clothes': 'Одежда',
             'rule_category_public_transport': 'Общественный транспорт',
             'rule_category_recreation_and_entertaiment': 'Отдых и развлечения',
             'rule_category_education': 'Образование'}
    return keys[key]
########################################################################################################################
#                                       Конец Меню "Мои Правила"                                                       #
########################################################################################################################


########################################################################################################################
#                                       Меню "Календарь обязательств"                                                  #
########################################################################################################################
BTN_CREATE_COMMITMENT = InlineKeyboardButton('Создать обязательство', callback_data='create_commitment')
BTN_DELETE_COMMITMENT = InlineKeyboardButton('Удалить обязательство', callback_data='delete_commitment')
CALENDAR_MENU = InlineKeyboardMarkup().add(BTN_CREATE_COMMITMENT).add(BTN_DELETE_COMMITMENT).add(BTN_BACK_TO_MENU)
BTN_BACK_TO_CREATE_COMMITMENT_MENU = InlineKeyboardMarkup().add(InlineKeyboardButton('Назад',
                                                                                     callback_data='create_commitment'))


def create_commitment_menu(sum: str, name: str, date: str):
    BTN_ENTER_SUM_OF_COMMITMENT = InlineKeyboardButton(sum, callback_data='enter_sum_commitment')
    BTN_ENTER_NAME_OF_COMMITMENT = InlineKeyboardButton(name, callback_data='enter_name_of_commitment')
    BTN_ENTER_DATE_OF_COMMITMENT = InlineKeyboardButton(date, callback_data='enter_date_of_commitment')
    BTN_SAVE_RULE = InlineKeyboardButton('Сохранить', callback_data='save_commitment')
    BTN_BACK_TO_RULE_MENU = InlineKeyboardButton('Назад', callback_data='calendar_of_commitments')
    CREATE_RULE = InlineKeyboardMarkup().add(BTN_ENTER_SUM_OF_COMMITMENT).add(BTN_ENTER_NAME_OF_COMMITMENT)\
        .add(BTN_ENTER_DATE_OF_COMMITMENT).add(BTN_SAVE_RULE).add(BTN_BACK_TO_RULE_MENU)
    return CREATE_RULE


def get_commitment(telegram_id):
    LIST_DELETE_COMMITMENT = InlineKeyboardMarkup()
    commitment = data_manager.get_rule(telegram_id)
    for i in range(len(commitment)):
        LIST_DELETE_COMMITMENT.add(InlineKeyboardButton(commitment[i], callback_data=f'{i}_commitment'))
    LIST_DELETE_COMMITMENT.add(InlineKeyboardButton('Назад', callback_data='calendar_of_commitments'))
    return LIST_DELETE_COMMITMENT


def get_index_delete_commitment():
    _list = []
    for i in range(30):
        _list.append(f'{i}_commitment')
    return _list
########################################################################################################################
#                                        Конец "Календарь обязательств"                                                #
########################################################################################################################
