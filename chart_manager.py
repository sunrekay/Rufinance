import matplotlib.pyplot as plt
import numpy as np
from aiogram.types import InputFile
import data_manager


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

    plt.savefig(f'static/{telegram_id}.png')


def get_pie_chart(telegram_id):
    try:
        return InputFile(f'static/{telegram_id}.png')
    except:
        return InputFile('static/nothing.png')