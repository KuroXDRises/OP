from pyrogram import filters
from pyrogram import types
from pyrogram.enums import ButtonStyle, ParseMode
import asyncio
import utils

spin_costs = {
    1: {"price": 1},
    5: {"price": 75},
    10: {"price": 125}
}


def spin_menu(user_id):
    msg = """
<b>🎡 Grand Line Spin Wheel</b>

Choose your spin amount below.

💎 Rewards may include:
• Beli
• Neo Fragments
• Devil Tickets
"""

    kb = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    "1x",
                    callback_data=f"spin:1:{user_id}",
                    style=ButtonStyle.PRIMARY
                ),
                types.InlineKeyboardButton(
                    "5x",
                    callback_data=f"spin:5:{user_id}",
                    style=ButtonStyle.PRIMARY
                ),
                types.InlineKeyboardButton(
                    "10x",
                    callback_data=f"spin:10:{user_id}",
                    style=ButtonStyle.PRIMARY
                )
            ]
        ]
    )

    return msg, kb


def spin_callback(bot):

    @bot.on_callback_query(filters.regex("^spin:"))
    async def spin_command_continue(_, call):

        spins = int(call.data.split(":")[1])
        user_id = int(call.data.split(":")[2])

        if call.from_user.id != user_id:
            return await call.answer(
                "This button is not for you.",
                show_alert=True
            )

        data = utils.get_user(user_id)

        if data is None:
            return await call.answer(
                "You are not registered.",
                show_alert=True
            )

        neo = data["currency"]["neo_fragments"]
        price = spin_costs[spins]["price"]

        kb = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton(
                        "Confirm",
                        callback_data=f"confirm_spin:{spins}:{user_id}",
                        style=ButtonStyle.SUCCESS
                    ),
                    types.InlineKeyboardButton(
                        "Cancel",
                        callback_data=f"cancel_spin:{user_id}",
                        style=ButtonStyle.DANGER
                    )
                ]
            ]
        )

        await call.message.edit_text(
            f"""
<b>🎡 Spin Confirmation</b>

Use <code>{spins}x</code> Spin?

💎 Cost: <code>{price}</code>
💰 You Have: <code>{neo}</code>
""",
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )

        await call.answer()

    @bot.on_callback_query(filters.regex("^cancel_spin:"))
    async def cancel_spin(_, call):

        user_id = int(call.data.split(":")[1])

        if call.from_user.id != user_id:
            return await call.answer(
                "Not for you.",
                show_alert=True
            )

        msg, kb = spin_menu(user_id)

        await call.message.edit_text(
            msg,
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )

        await call.answer("Returned to menu.")

    @bot.on_callback_query(filters.regex("^confirm_spin:"))
    async def confirm_spin(_, call):

        spins = int(call.data.split(":")[1])
        user_id = int(call.data.split(":")[2])

        if call.from_user.id != user_id:
            return await call.answer(
                "This button is not for you.",
                show_alert=True
            )

        data = utils.get_user(user_id)

        if data is None:
            return await call.answer(
                "User not found.",
                show_alert=True
            )

        price = spin_costs[spins]["price"]
        neo = data["currency"]["neo_fragments"]

        if neo < price:
            return await call.answer(
                "Not enough Neo Fragments!",
                show_alert=True
            )

        for x in ["❶", "❶❷", "❶❷❸"]:
            await call.message.edit_text(x)
            await asyncio.sleep(0.5)

        utils.update_user(
            user_id,
            "neo_fragments",
            price,
            mode="minus"
        )

        if spins == 1:
            rewards = [utils.get_random_item()]
        elif spins == 5:
            rewards = [utils.get_random_item() for _ in range(5)]
        else:
            rewards = [utils.get_random_item() for _ in range(10)]

        rewards = utils.sort_rewards(rewards)
        utils.add_spin_rewards(user_id, rewards)

        reward_text = utils.format_rewards(rewards)

        kb = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton(
                        "Spin Again",
                        callback_data=f"spin:{spins}:{user_id}",
                        style=ButtonStyle.PRIMARY
                    )
                ]
            ]
        )

        await call.message.edit_text(
            f"""
<b>🏆 Spin Rewards</b>

<code>{reward_text}</code>

✨ Rewards added successfully.
""",
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )

        await call.answer()