import json


def add_record(tg_id:str, category:str, cost:str) -> dict:
    with open("users_data/my_rules_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
        except:
            data = {}
    f.close()

    tg_id = str(tg_id)
    new_category = get_categories(tg_id)
    new_cost = get_costs(tg_id)

    new_category.append(category)
    new_cost.append(cost)

    my_rule = {
        tg_id: {
            'category': new_category,
            'cost': new_cost
        }
    }

    data.update(my_rule)
    my_rule_json = json.dumps(data, indent=4)

    with open("users_data/my_rules_data.json", "w", encoding='utf-8') as my_file:
        my_file.write(my_rule_json)
    my_file.close()
    return my_rule


def get_categories(tg_id: str) -> list:
    with open("users_data/my_rules_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['category']
        except:
            f.close()
            return []



def get_costs(tg_id: str) -> list:
    with open("users_data/my_rules_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            f.close()
            return data[str(tg_id)]['cost']
        except:
            f.close()
            return []


def delete_record(tg_id: str, index: int):
    with open("users_data/my_rules_data.json", "r", encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
        except:
            data = {}
    f.close()

    tg_id = str(tg_id)
    new_category = get_categories(tg_id)
    new_cost = get_costs(tg_id)

    new_category.pop(index)
    new_cost.pop(index)

    my_rule = {
        tg_id: {
            'category': new_category,
            'cost': new_cost
        }
    }

    data.update(my_rule)
    my_rule_json = json.dumps(data, indent=4)

    with open("users_data/my_rules_data.json", "w", encoding='utf-8') as my_file:
        my_file.write(my_rule_json)
    my_file.close()
    return my_rule