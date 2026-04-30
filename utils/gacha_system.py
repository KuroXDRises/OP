import random
import math
import utils

characters = utils.load_characters()

selected_chars = ["Helmeppo", "Morgan", "Cabaji", "Usopp", "Nami"]

currency = {
    "beli": {
        "item": "beli",
        "amount": [500, 1000],
        "chance": 55
    },
    "neo_fragments": {
        "item": "neo_fragments",
        "amount": [1, 10],
        "chance": 20
    },
    "devil_tickets": {
        "item": "devil_tickets",
        "amount": [1, 2],
        "chance": 10
    }
}

CHARACTER_CHANCE = 15

def get_spin_chars():
    return [c for c in characters if c["name"] in selected_chars]

def get_random_character():
    return random.choice(get_spin_chars())

def get_random_currency():
    total = sum(d["chance"] for d in currency.values())
    roll = random.uniform(1, total)

    current = 0
    for d in currency.values():
        current += d["chance"]

        if roll <= current:
            low, high = d["amount"]

            amount = math.floor(
                random.uniform(low, high + 1)
            )

            return {
                "type": "currency",
                "item": d["item"],
                "amount": amount,
                "chance": d["chance"]
            }

def spin_once():
    if random.randint(1, 100) <= CHARACTER_CHANCE:
        return {
            "type": "character",
            "data": get_random_character()
        }

    return get_random_currency()

def spin_multiple(spins=1):
    return [spin_once() for _ in range(spins)]

def merge_rewards(rewards):
    merged = {}
    chars = []

    for r in rewards:
        if r["type"] == "character":
            chars.append(r["data"])
            continue

        item = r["item"]
        merged[item] = merged.get(item, 0) + r["amount"]

    return merged, chars

def format_rewards(rewards):
    merged, chars = merge_rewards(rewards)

    text = "✧═══════════════✧\n"
    text += "        GACHA RESULT\n"
    text += "✧═══════════════✧\n"

    for c in chars:
        text += f"➤ {c['name']}\n"

    for item, amount in merged.items():
        text += f"➤ {item:<15} x {amount}\n"

    text += "✧═══════════════✧"

    return text

def format_character_msg(char):
    return f"""
✧═══════════════✧
      NEW CHARACTER
✧═══════════════✧
➤ {char['name']}
➤ Type    : {char['type']}
➤ Element : {char['element']}

☠ A new fighter joined your crew
✧═══════════════✧
"""

def add_rewards(user_id, rewards):
    data = utils.get_user(user_id)

    if not data:
        return False

    merged, chars = merge_rewards(rewards)

    for item, amount in merged.items():
        if item in data["currency"]:
            data["currency"][item] += amount
        else:
            data["currency"][item] = amount

    if "chars" not in data:
        data["chars"] = []

    existing_names = {x["name"] for x in data["chars"] if isinstance(x, dict)}

    for c in chars:

        if not isinstance(c, dict):
            continue

        if c["name"] in existing_names:
            data["currency"]["beli"] += 5000
            continue

        _nc = utils.compact_character_data(c)
        data["chars"].append(_nc)

    data["last_spin"] = str(rewards)

    utils.save_user(data)

    return True

def one_spin(user_id):
    rewards = spin_multiple(1)
    add_rewards(user_id, rewards)
    return format_rewards(rewards), rewards

def five_spin(user_id):
    rewards = spin_multiple(5)
    add_rewards(user_id, rewards)
    return format_rewards(rewards), rewards

def ten_spin(user_id):
    rewards = spin_multiple(10)
    add_rewards(user_id, rewards)
    return format_rewards(rewards), rewards