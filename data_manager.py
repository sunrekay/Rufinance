import json


def add_record(tg_id:str, rule:str, cost:str, date:str) -> dict:
    with open("users_data/users_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
        except:
            data = {}
    f.close()

    tg_id = str(tg_id)

    new_rule = get_rule(tg_id)
    new_cost = get_cost(tg_id)
    new_date = get_date(tg_id)

    new_rule.append(rule)
    new_cost.append(cost)
    new_date.append(date)

    users = {
        tg_id: {
            'rule': new_rule,
            'cost': new_cost,
            'date': new_date
        }
    }

    data.update(users)
    users_json = json.dumps(data, indent=3)

    with open("users_data/users_data.json", "w", encoding='utf-8') as my_file:
        my_file.write(users_json)
    my_file.close()
    return users


def delete_record(tg_id:str, index: int) -> dict:
    with open("users_data/users_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
        except:
            data = {}
    f.close()

    tg_id = str(tg_id)

    new_rule = get_rule(tg_id)
    new_cost = get_cost(tg_id)
    new_date = get_date(tg_id)

    new_rule.pop(index)
    new_cost.pop(index)
    new_date.pop(index)

    users = {
        tg_id: {
            'rule': new_rule,
            'cost': new_cost,
            'date': new_date
        }
    }

    data.update(users)
    users_json = json.dumps(data, indent=3)

    with open("users_data/users_data.json", "w", encoding='utf-8') as my_file:
        my_file.write(users_json)
    my_file.close()
    return users


def get_rule(tg_id) -> list:
    with open("users_data/users_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['rule']
        except:
            f.close()
            return []


def get_cost(tg_id) -> list:
    with open("users_data/users_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['cost']
        except:
            f.close()
            return []


def get_date(tg_id) -> list:
    with open("users_data/users_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['date']
        except:
            f.close()
            return []
