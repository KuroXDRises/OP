from pyrogram import (
    filters,
    types,
    enums
)
import random
import math
from datetime import (
    datetime,
    timedelta
)
import asyncio
import utils


def can_claim_daily(data):
    last = data.get("last_daily", None)

    if not last:
        return (True, 0)

    last_time = datetime.fromisoformat(last)
    next_time = last_time + timedelta(hours=24)

    if datetime.utcnow() >= next_time:
        return (True, 0)

    left = next_time - datetime.utcnow()

    return (
        False,
        int(left.total_seconds())
    )


def claim_daily(data):
    ok, left = can_claim_daily(data)

    if not ok:
        h = math.floor(left / 3600)
        m = math.floor((left % 3600) / 60)

        return f"""
✦═══════════════✦
      DAILY LOCKED
✦═══════════════✦
Come back in {h}h {m}m
✦═══════════════✦
"""

    roll = math.floor(random.random() * 100) + 1

    if roll <= 35:
        reward = random.randint(500, 1200)
        data["currency"]["beli"] += reward
        msg = f"You got {reward} Beli"

    elif roll <= 55:
        reward = random.randint(2, 5)
        data["currency"]["neo_fragments"] += reward
        msg = f"You got {reward} Neo Fragments"

    elif roll <= 70:
        reward = random.randint(40, 100)
        data["exp"] += reward
        msg = f"You got {reward} EXP"

    elif roll <= 82:
        reward = 1
        data["currency"]["devil_tickets"] += reward
        msg = f"You got {reward} Devil Ticket"

    elif roll <= 92:
        reward = random.randint(1500, 2500)
        data["currency"]["beli"] += reward
        msg = f"Rare Reward! {reward} Beli"

    else:
        reward = random.randint(3000, 5000)
        data["currency"]["beli"] += reward
        msg = f"Epic Reward! {reward} Beli"

    data["daily_streak"] += 1
    data["last_daily"] = datetime.utcnow().isoformat()

    utils.save_user(data)

    return f"""
✦═══════════════✦
      DAILY CLAIM
✦═══════════════✦
{msg}

Roll   : {roll}
Streak : {data["daily_streak"]}
✦═══════════════✦
"""


def daily_handler(bot):
    @bot.on_message(filters.command("daily"))
    async def daily_command(_, message):
        user_id = message.from_user.id
        data = utils.get_user(user_id)

        if data is None:
            return await message.reply_text(
                "Please start first."
            )

        text = claim_daily(data)
        
        msg = await message.reply_text(
            "."
            )
        
        for x in [".", "..", "..."]:
            await msg.edit_text(
                f"Spinning Daily Wheel{x}"
                )
            await asyncio.sleep(0.5)
        await message.reply_text(
            text,
            parse_mode=enums.ParseMode.HTML
        )