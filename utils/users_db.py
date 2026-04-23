import json
import pathlib
from datetime import datetime
import copy
from config import Config

BASE_FOLDER = pathlib.Path(__file__).resolve().parent.parent
USERS_PATH = BASE_FOLDER / Config.get_variable("UserPath")

def ensure_directory():
    USERS_PATH.mkdir(parents=True, exist_ok=True)

def create_user_structure(user, char):
    return {
        "name": user.first_name,
        "username": user.username,
        "_id": user.id,

        "level": 1,
        "exp": 0,
        "max_exp": 100,

        "power": 100,
        "rank": "Rookie",

        "bounty": 0,

        "chars": [char],
        "fav_char": None,

        "devil_fruit": {
            "owned": None,
            "mastery": 0,
            "awakened": False
        },

        "inv": {
            "boosters": 0,
            "rename_cards": 0,
            "revive_food": 0
        },

        "currency": {
            "beli": 1000,
            "neo_fragments": 10,
            "devil_tickets": 5
        },

        "main_team": 1,
        "teams": build_user_teams(),
        
        "ship": "Not Build",

        "wins": 0,
        "loss": 0,
        "draw": 0,

        "daily_streak": 0,
        "last_daily": None,

        "last_transaction": None,
        "last_battle": None,
        "last_spin": None,

        "title": "New Pirate",
        "crew": None,

        "region": "East Blue",
        "story_progress": 1,

        "premium": False,

        "created_at": datetime.utcnow().isoformat()
    }

def get_user_file(uid):
    ensure_directory()
    return USERS_PATH / f"{uid}.json"

def get_user(uid):
    file = get_user_file(uid)
    if not file.exists():
        return None
    with file.open("r", encoding="UTF-8") as x:
        return json.load(x)
        
def build_user_teams():
    return {str(index): [] for index in range(1, 7)}

def create_user(user, char):
    data = create_user_structure(user, char)
    save_user(data)

def save_user(data):
    file = get_user_file(data['_id'])
    with file.open("w", encoding="UTF-8") as x:
        json.dump(data, x, indent=2, ensure_ascii=False)


def compact_character_db(base_char):
    char = copy.deepcopy(base_char)

    new_data = {
        "_id": char["_id"],
        "name": char["name"],
        "level": char["level"],
        "xp": char["xp"],
        "max_xp": char["max_xp"],
        "bounty": char["bounty"],

        "hp": char["hp"],
        "max_hp": char["max_hp"],
        "attack": char["attack"],
        "defense": char["defense"],
        "speed": char["speed"],
        "crit_rate": char["crit_rate"],

        "skill_1": char["skill_1"],
        "skill_2": char["skill_2"],
        "ultimate": char["ultimate"]
    }

    return new_data

def update_user(uid, key=None, value=None, mode="set"):
    data = get_user(uid)
    if data is None:
        return None

    if key is None:
        save_user(data)
        return data

    if key in ["beli", "neo_fragments", "devil_tickets"]:
        if mode == "add":
            data["currency"][key] += value
        elif mode == "minus":
            data["currency"][key] -= value
        else:
            data["currency"][key] = value

    elif key == "inv":
        item = value["type"]
        amount = value.get("amount", 1)

        if mode == "add":
            data["inv"][item] = data["inv"].get(item, 0) + amount
        elif mode == "minus":
            data["inv"][item] = max(0, data["inv"].get(item, 0) - amount)

    elif key == "devil_fruit":
        if mode == "add":
            data["devil_fruit"] = value
        elif mode == "minus":
            data["devil_fruit"] = None

    else:
        data[key] = value

    save_user(data)
    return data

def apply_tax(amount, tax_per_100=25):
    tax = (amount // 100) * tax_per_100
    return amount - tax, tax

def convert_neo_to_beli(neo, rate=100, tax_per_100=25):
    gross = neo * rate
    final, tax = apply_tax(gross, tax_per_100)

    return {
        "neo": neo,
        "gross_beli": gross,
        "tax": tax,
        "final_beli": final
    }

def transfer_beli(amount, tax_per_100=25):
    final, tax = apply_tax(amount, tax_per_100)

    return {
        "sent": amount,
        "tax": tax,
        "received": final
    }