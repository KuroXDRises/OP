from pyrogram import filters
from pyrogram import types
from pyrogram.enums import ButtonStyle, ChatType
import asyncio
import utils

def spin_handler(bot):
    @bot.on_message(filters.command("spin"))
    async def spin_command(_, message):
        user_id = message.from_user.id
        data = utils.get_user(user_id)
        if message.chat.type != ChatType.PRIVATE:
            return await message.reply(
                "Spin only works in private chat. Message me privately to use this command."
            )
        if data is None:
            return await message.reply_text(
                "You are not registered yet."
            )
        msg = """
<b>✧ GRAND LINE SPIN WHEEL ✧</b>

🏴‍☠️ Welcome, Captain.

The mysterious wheel of fate holds
treasure, rare items, fragments,
tickets, and legendary rewards.

〘 Available Spins 〙
➩ 1x  - Single Fate Spin
➩ 5x  - Pirate Rush Spin
➩ 10x - Emperor Storm Spin

〘 Possible Rewards 〙
✦ Beli
✦ Neo Fragments
✦ Devil Tickets
✦ Rare Treasure Drops

❖ The sea rewards the brave.
❖ Spin now and chase destiny.

<b>Choose your spin amount below.</b>
"""
        kb = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton(
                        "1x",
                        callback_data=f"spin:1:{user_id}",
                        style=ButtonStyle.DEFAULT
                    ),
                    types.InlineKeyboardButton(
                        "5x",
                        callback_data=f"spin:5:{user_id}",
                        style=ButtonStyle.DEFAULT
                    ),
                    types.InlineKeyboardButton(
                        "10x",
                        callback_data=f"spin:10:{user_id}",
                        style=ButtonStyle.DEFAULT
                    )
                ]
            ]
        )
        await message.reply_text(
            msg,
            reply_markup=kb
        )