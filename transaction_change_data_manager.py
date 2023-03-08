import json
import pytz
from datetime import datetime


def add_record(tg_id:str, name:str, cost:str, operation: str) -> dict:
    '''tg_id:str, name:str, cost:str, operation:str'''
    with open("transaction_change_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
        except:
            data = {}
    f.close()

    tg_id = str(tg_id)
    date = datetime.now(pytz.timezone('Europe/Moscow'))
    date = date.strftime("%d-%m-%Y")

    if tg_id not in data.keys():
        transactions = {
            tg_id: {
                'name': [name],
                'cost': [cost],
                'date': [date],
                'operation': [operation]
            }
        }
    else:

        new_name = get_name(tg_id)
        new_cost = get_cost(tg_id)
        new_operation = get_operation(tg_id)
        new_date = get_date(tg_id)

        new_name.append(name)
        new_cost.append(cost)
        new_operation.append(operation)
        new_date.append(date)

        transactions = {
            tg_id: {
                'name': new_name,
                'cost': new_cost,
                'date': new_date,
                'operation': new_operation
            }
        }

    data.update(transactions)
    transactions_json = json.dumps(data, indent=4)

    with open("transaction_change_data.json", "w", encoding='utf-8') as my_file:
        my_file.write(transactions_json)
    my_file.close()
    return transactions


def get_name(tg_id) -> list:
    with open("transaction_change_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['name']
        except:
            f.close()
            return []



def get_cost(tg_id) -> list:
    with open("transaction_change_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['cost']
        except:
            f.close()
            return []


def get_operation(tg_id) -> list:
    with open("transaction_change_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['operation']
        except:
            f.close()
            return []


def get_date(tg_id) -> list:
    with open("transaction_change_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['date']
        except:
            f.close()
            return []


def get_transactions(tg_id, operation) -> list:
    with open("transaction_change_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            name_list = data[str(tg_id)]['name']
            cost_list = data[str(tg_id)]['cost']
            operation_list = data[str(tg_id)]['operation']
            date_list = data[str(tg_id)]['date']

            unifier: str = ''
            for i in range(len(name_list)):
                if operation_list[i] == operation:
                    unifier += f'[{date_list[i]}] {name_list[i]} - {cost_list[i]} руб.\n'
            return unifier

        except:
            f.close()
            return []


def get_transactions_all(tg_id) -> str:
    with open("transaction_change_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            name_list = data[str(tg_id)]['name']
            cost_list = data[str(tg_id)]['cost']
            operation_list = data[str(tg_id)]['operation']
            date_list = data[str(tg_id)]['date']

            unifier: str = ''
            for i in range(len(name_list)):
                unifier += f'[{date_list[i]}][{operation_list[i]}] {name_list[i]} - {cost_list[i]} руб.\n'
            return unifier

        except:
            f.close()
            return ''


def sum_of_(tg_id, operation):
    with open("transaction_change_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            cost_list = data[str(tg_id)]['cost']
            operation_list = data[str(tg_id)]['operation']
            sum = 0
            for i in range(len(cost_list)):
                if operation_list[i] == operation:
                    sum += cost_list[i]
            return sum
        except:
            f.close()
            return 0