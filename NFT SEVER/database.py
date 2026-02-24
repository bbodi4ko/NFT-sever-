import json
import os

DB_FILE = "db.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"users": {}}, f)

def get_data():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_balance(user_id):
    data = get_data()
    return data["users"].get(str(user_id), {}).get("balance", 0)

def update_balance(user_id, amount):
    data = get_data()
    user = data["users"].setdefault(str(user_id), {"balance": 0})
    user["balance"] += amount
    save_data(data)

def set_stake(user_id, stake, multiplier):
    data = get_data()
    user = data["users"].setdefault(str(user_id), {"balance": 0})
    user["stake"] = stake
    user["multiplier"] = multiplier
    save_data(data)

def get_stake(user_id):
    data = get_data()
    user = data["users"].get(str(user_id), {})
    return user.get("stake", 0), user.get("multiplier", 0)

def clear_stake(user_id):
    data = get_data()
    user = data["users"].get(str(user_id), {})
    user.pop("stake", None)
    user.pop("multiplier", None)
    save_data(data)
