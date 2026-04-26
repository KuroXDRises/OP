from db.starters import starters as st
import copy


def compact_character_data(character):
    char = copy.deepcopy(character)

    return {
        "_id": char["_id"],
        "name": char["name"],
        "pic": char["pic"],
        "level": char["level"],
        "xp": char["xp"],
        "max_xp": 2700,
        "bounty": char["bounty"],
        "stamina": 78000,
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


def prepare_starters_data(x: int):
    return compact_character_data(st[x])


def starter_stats_message(character):
    return f"""🏴‍☠️ <b>PIRATE STATUS REPORT</b> 🏴‍☠️

⚓ <b>Name:</b> {character["name"]}
🆔 <b>ID:</b> {character["_id"]}

🌊 A new pirate has entered the Grand Line.
Power, fame, and treasure await ahead.

🔥 Build your legend.
💰 Raise your bounty.
👑 Become the King of the Pirates."""


def load_stats_msg(value: int, char):
    messages = {
        1: f"""
✦═══════════════✦
             PIRATE INFO
✦═══════════════✦
➤ Name     : {char["name"]}
➤ ID       : {char["_id"]}
➤ Level    : {char["level"]}
➤ Bounty   : ฿ {char["bounty"]}

☠ A pirate feared by the seas...
✦═══════════════✦
""",

        2: f"""
❖═══════════════❖
           PROGRESS REPORT
❖═══════════════❖
➩ XP       : {char["xp"]}/{char["max_xp"]}
➩ HP       : {char["hp"]}/{char["max_hp"]}

〘 Keep sailing forward 〙
❖═══════════════❖
""",

        3: f"""
✞═══════════════✞
            BATTLE POWER
✞═══════════════✞
✟ HP        : {char["hp"]}
✟ Attack    : {char["attack"]}
✟ Defense   : {char["defense"]}
✟ Speed     : {char["speed"]}
✟ CritRate  : {char["crit_rate"]}%

⚔ Ready for Grand Line wars
☯══════════════☯
""",

        4: f"""
✧═══════════════✧
            DEVIL SKILLS
✧═══════════════✧
➤ Skill I
〘 {char["skill_1"]["name"]} 〙
➩ Power : {char["skill_1"]["power"]}

➤ Skill II
〘 {char["skill_2"]["name"]} 〙
➩ Power : {char["skill_2"]["power"]}

➤ ULTIMATE
『 {char["ultimate"]["name"]} 』
➩ Power : {char["ultimate"]["power"]}

☠ Unleash destruction
✧═══════════════✧
"""
    }

    return messages.get(value, messages[1])