from datetime import datetime
import pytz

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from aiogram.types import InputFile
import data_manager
import my_rules_manager
import transaction_change_data_manager


def set_pie_chart(telegram_id):
    rule_list = data_manager.get_rule(telegram_id)
    cost_list = data_manager.get_cost(telegram_id)
    fig, ax = plt.subplots(figsize=(6, 6))

    _, __, autotext = ax.pie(cost_list, labels=rule_list,
                             autopct='%1.1f%%',
                             wedgeprops=dict(width=0.5),
                             radius=1.4, center=(4, 4),
                             pctdistance=0.83)
    plt.setp(autotext, size=18)
    plt.savefig(f'static/{telegram_id}_pie.png')


def get_pie_chart(telegram_id):
    try:
        return InputFile(f'static/{telegram_id}_pie.png')
    except:
        return InputFile('static/nothing.png')


def set_my_rules_table(telegram_id):
    table_data = [["Категория затрат", "Ограничение", "Можно потратить"]]

    categories = my_rules_manager.get_categories(telegram_id)
    costs = my_rules_manager.get_costs(telegram_id)

    for i in range(len(categories)):
        sum_of_minus_category = transaction_change_data_manager.category_sum_of_(telegram_id, "Расход", categories[i])
        can_spend = int(costs[i]) - sum_of_minus_category
        table_data.append([categories[i], f'{costs[i]} ₽', f'{can_spend} ₽'])

    fig, ax = plt.subplots()
    table = ax.table(cellText=table_data, loc='center', cellLoc='center',
                     bbox=(-0.15, -0.11, 1.265, 1.24))
    table.set_fontsize(30)
    table.scale (1.2,4)
    ax.axis('off')
    plt.savefig(f'static/{telegram_id}_my_rules_table.png')


def get_my_rules_table(telegram_id):
    try:
        return InputFile(f'static/{telegram_id}_my_rules_table.png')
    except:
        # TODO: Создать картинку в случае отсутсвия списка "Мои правила",
        #  когда картинка создана раскомментировать код ниже.
        return InputFile(f'static/nothing.png')




def set_calendar_table(telegram_id):
    table_data = [["Дата", "Наименование", "Сумма", "Осталось дней"]]

    date = data_manager.get_date(telegram_id)
    name = data_manager.get_rule(telegram_id)
    sum_ = data_manager.get_cost(telegram_id)

    for i in range(len(date)):
        date[i] = date[i].split("-")
        fday = datetime(int(date[i][2]), int(date[i][1]), int(date[i][0]))
        today = datetime.now()
        diff = fday - today
        diff = str(diff).split(',')
        remains = sum_[i] - transaction_change_data_manager.category_sum_of_(tg_id=telegram_id,
                                                                             operation="Расход",
                                                                             category=name[i])
        different = diff[0].replace("days", "")
        different = different.replace("day", "")
        table_data.append(['-'.join(date[i]), name[i], f'{remains} ₽', f'{different} дней'])

    fig, ax = plt.subplots()
    table = ax.table(cellText=table_data, loc='center', cellLoc='center',
                     bbox=(-0.15, -0.11, 1.265, 1.24))
    table.set_fontsize(30)
    table.scale (1.2,4)
    ax.axis('off')
    plt.savefig(f'static/{telegram_id}_calendar_table.png')


def get_calendar_table(telegram_id):
    try:
        return InputFile(f'static/{telegram_id}_calendar_table.png')
    except:
        return InputFile(f'static/nothing.png')
