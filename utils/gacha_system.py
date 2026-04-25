import random
import math
import utils

currency = {
    "beli": {
        "item": "beli",
        "amount": [500, 1000],
        "chance": 62
    },
    "neo_fragments": {
        "item": "neo_fragments",
        "amount": [1, 10],
        "chance": 25
    },
    "devil_tickets": {
        "item": "devil_tickets",
        "amount": [1, 2],
        "chance": 10
    }
}


def get_random_item():
    total_chance = sum(data["chance"] for data in currency.values())

    roll = random.uniform(1, total_chance)
    current = 0

    for key, data in currency.items():
        current += data["chance"]

        if roll <= current:
            low = data["amount"][0]
            high = data["amount"][1]

            amount = math.floor(
                random.uniform(low, high + 1)
            )

            return {
                "item": data["item"],
                "amount": amount,
                "chance": data["chance"]
            }


def sort_rewards(rewards):
    merged = {}

    for reward in rewards:
        item = reward["item"]

        if item not in merged:
            merged[item] = {
                "item": item,
                "amount": 0,
                "chance": reward["chance"]
            }

        merged[item]["amount"] += reward["amount"]

    return sorted(
        merged.values(),
        key=lambda x: x["chance"],
        reverse=True
    )


def format_rewards(rewards):
    text = ""

    for r in rewards:
        text += f"➩ {r['item']:<18} x {r['amount']}\n"

    return text


def spin_rewards(spins):
    rewards = [
        get_random_item()
        for _ in range(spins)
    ]

    return sort_rewards(rewards)


def reward_message(rewards):
    return format_rewards(rewards)


def one_spin():
    rewards = spin_rewards(1)
    return reward_message(rewards)


def five_spin():
    rewards = spin_rewards(5)
    return reward_message(rewards)


def ten_spin():
    rewards = spin_rewards(10)
    return reward_message(rewards)


def add_spin_rewards(user_id, rewards):

    data = utils.get_user(user_id)

    if data is None:
        return False

    for reward in rewards:

        item = reward["item"]
        amount = reward["amount"]

        if item in data["currency"]:
            data["currency"][item] += amount

        elif item in data["inv"]:
            data["inv"][item] += amount

        else:
            data["inv"][item] = amount

    utils.save_user(data)

    return True