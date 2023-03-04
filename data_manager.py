import json


def add_courier(id, name,):
    with open("users_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
        except:
            data = {}
    f.close()
    courier = {
        id: {
            "name": name,
        }
    }
    data.update(courier)
    courier_json = json.dumps(data, indent=4)

    with open("users_data.json", "w", encoding='utf-8') as my_file:
        my_file.write(courier_json)
    my_file.close()
    return None