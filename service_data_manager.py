import json


def add_record(tg_id: int, last_message_id:str) -> dict:
    with open("users_data/service_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
        except:
            data = {}
    f.close()

    tg_id = str(tg_id)

    users = {
        tg_id: {
            'last_message_id': last_message_id,
        }
    }

    data.update(users)
    users_json = json.dumps(data, indent=1)

    with open("users_data/service_data.json", "w", encoding='utf-8') as my_file:
        my_file.write(users_json)
    my_file.close()
    return users


def get_last_message_id(tg_id: int):
    with open("users_data/service_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['last_message_id']
        except:
            f.close()
            return None
