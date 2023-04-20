import json


def add_new_account(tg_id):
    with open("users_data/statistiek.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
        except:
            data = {}
    f.close()
    tg_id = str(tg_id)
    users = {
        tg_id: {
            'click_counter': 0,
            'everything': 0
        }
    }
    data.update(users)
    users_json = json.dumps(data, indent=1)
    with open("users_data/statistiek.json", "w", encoding='utf-8') as my_file:
        my_file.write(users_json)
    my_file.close()


def click_counter_plus_one(tg_id):
    with open("users_data/statistiek.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
        except:
            data = {}
    f.close()
    tg_id = str(tg_id)
    data[tg_id]['click_counter'] += 1
    users_json = json.dumps(data, indent=1)
    with open("users_data/statistiek.json", "w", encoding='utf-8') as my_file:
        my_file.write(users_json)
    my_file.close()


def update(tg_id: int) -> dict:
    with open("users_data/service_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
        except:
            data = {}
    f.close()
    tg_id = str(tg_id)
    users = {
        tg_id: {
            'last_message_id': 0,
            'RULE_INPUT_BOOL': False,
            'RULE_INPUT_STR': 'Ввести название',
            'RULE_INPUT_INT': 'Ввести сумму',
            'RULE_INPUT_STR_BOOL': '',
            'TRANSACTION_INPUT_MINUS_BOOL': False,
            'TRANSACTION_INPUT_CATEGORY_BOOL': False,
            'TRANSACTION_INPUT_OPERATION_BOOL': False,
            'TRANSACTION_INPUT_MINUS_INT': 'Ввести сумму',
            'TRANSACTION_INPUT_MINUS_CATEGORY': 'Ввести название',
            'TRANSACTION_INPUT_OPERATION': 'Выберите операцию',
            'COMMITMENT_SUM': 'Ввести сумму',
            'COMMITMENT_NAME': 'Ввести название',
            'COMMITMENT_DATE': 'Ввести дату',
            'COMMITMENT_SUM_BOOL': False,
            'COMMITMENT_NAME_BOOL': False,
            'COMMITMENT_DATE_BOOL': False,
            'TRAINIG_DICT_BOOL': False
        }
    }
    data.update(users)
    users_json = json.dumps(data, indent=1)
    with open("users_data/service_data.json", "w", encoding='utf-8') as my_file:
        my_file.write(users_json)
    my_file.close()
    return users


def get(tg_id: str, key):
    with open("users_data/service_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            tg_id = str(tg_id)
            return data[tg_id][key]
        except:
            return None
    f.close()


def set(tg_id: str, key, value):
    try:
        with open("users_data/service_data.json", "r", encoding='utf-8') as f:
            try:
                data = json.loads(f.read())
            except:
                data = {}
        f.close()

        tg_id = str(tg_id)
        data[tg_id][key] = value

        users_json = json.dumps(data, indent=1)
        with open("users_data/service_data.json", "w", encoding='utf-8') as my_file:
            my_file.write(users_json)
        my_file.close()
        return True
    except:
        return False


def add_record(tg_id: int, last_message_id):
    try:
        with open("users_data/service_data.json", "r", encoding='utf-8') as f:
            try:
                data = json.loads(f.read())
            except:
                data = {}
        f.close()

        tg_id = str(tg_id)
        data[tg_id]['last_message_id'] = last_message_id

        users_json = json.dumps(data, indent=1)
        with open("users_data/service_data.json", "w", encoding='utf-8') as my_file:
            my_file.write(users_json)
        my_file.close()
        return True
    except:
        return False


def get_last_message_id(tg_id: int):
    with open("users_data/service_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['last_message_id']
        except:
            f.close()
            return None
