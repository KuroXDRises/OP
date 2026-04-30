import copy
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHAR_PATH = BASE_DIR / "db" / "characters.json"

def load_characters():
    with open(CHAR_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def compact_character_data(character):
    char = copy.deepcopy(character)

    return {
        "_id": char["_id"],
        "name": char["name"],
        "pic": char["pic"],
        "level": char.get("level", 1),
        "xp": char.get("xp", 0),
        "max_xp": char.get("max_xp", 2700),
        "bounty": char.get("bounty", 0),
        "stamina": char.get("stamina", 78000),
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

def prepare_starters_data(index: int):
    characters = load_characters()
    return compact_character_data(characters[index])

def starter_stats_message(character):
    return f"""🏴‍☠️ <b>PIRATE STATUS</b>

⚓ <b>{character["name"]}</b>
🆔 <code>{character["_id"]}</code>

🌊 New pirate entered the Grand Line.
💰 Bounty awaits. Fame awaits.

⚔ Build your legend.
"""

def load_stats_msg(value: int, char):
    messages = {
        1: f"""
✦═══════════════✦
      PIRATE INFO
✦═══════════════✦
➤ Name   : {char["name"]}
➤ ID     : {char["_id"]}
➤ Level  : {char["level"]}
➤ Bounty : ฿ {char["bounty"]}
✦═══════════════✦
""",

        2: f"""
❖═══════════════❖
   PROGRESS
❖═══════════════❖
➩ XP : {char["xp"]}/{char["max_xp"]}
➩ HP : {char["hp"]}/{char["max_hp"]}
❖═══════════════❖
""",

        3: f"""
✞═══════════════✞
   STATS
✞═══════════════✞
HP     : {char["hp"]}
ATK    : {char["attack"]}
DEF    : {char["defense"]}
SPD    : {char["speed"]}
CRIT   : {char["crit_rate"]}%
✞═══════════════✞
""",

        4: f"""
✧═══════════════✧
   SKILLS
✧═══════════════✧
➤ {char["skill_1"]["name"]}
   Power : {char["skill_1"]["power"]}

➤ {char["skill_2"]["name"]}
   Power : {char["skill_2"]["power"]}

➤ {char["ultimate"]["name"]}
   Power : {char["ultimate"]["power"]}
✧═══════════════✧
"""
    }

    return messages.get(value, messages[1])

def get_char(char_name):
    characters = load_characters()

    return next(
        (
            copy.deepcopy(char)
            for char in characters
            if char["name"].lower() == char_name.lower()
        ),
        None
    )