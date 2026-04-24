from pyrogram import filters
from pyrogram.types import *
from pyrogram.enums import ButtonStyle
import utils

base_multiplier = 1.15
MAX_MULTIPLIER = 1.92
MAX_BET = 15000


def dice_handler(bot):

    @bot.on_message(filters.command("dice"))
    async def dice_command(client, message):

        user_id = message.from_user.id
        data = utils.get_user(user_id)

        if data is None:
            return await message.reply(
                "You are not registered yet!"
            )

        args = message.text.split(" ", 1)

        if len(args) < 2:
            return await message.reply(
                "Usage: /dice {bet}\nExample: /dice 100"
            )

        if not args[1].isdigit():
            return await message.reply(
                "Bet must be a valid number."
            )

        bet = int(args[1])

        if bet <= 0:
            return await message.reply(
                "Invalid bet amount."
            )

        if bet > MAX_BET:
            return await message.reply(
                "Max Bet Is 15000"
            )

        if bet % 100 != 0:
            return await message.reply(
                "Bet must be multiple of 100."
            )

        if data["currency"]["beli"] < bet:
            return await message.reply(
                "Not enough balance."
            )

        msg = f"""
<b>✧ GRAND LINE GAMBLE PANEL ✧</b>

🏴‍☠️ Pirate Bet: <code>{bet}</code> Beli
⚡ Max Boost: <code>{MAX_MULTIPLIER}x</code>

❖ Choose your fate below.
❖ Fortune favors bold pirates.
"""

        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "High",
                        callback_data=f"high:{bet}:{user_id}",
                        style=ButtonStyle.PRIMARY
                    ),
                    InlineKeyboardButton(
                        "Low",
                        callback_data=f"low:{bet}:{user_id}",
                        style=ButtonStyle.PRIMARY
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Even",
                        callback_data=f"even:{bet}:{user_id}",
                        style=ButtonStyle.SUCCESS
                    ),
                    InlineKeyboardButton(
                        "Odd",
                        callback_data=f"odd:{bet}:{user_id}",
                        style=ButtonStyle.DANGER
                    )
                ]
            ]
        )

        await message.reply(
            msg,
            reply_markup=kb
        )


def get_multiplier(bet):
    factor = bet / 500
    m = base_multiplier + (factor * 0.75 * base_multiplier)
    return min(m, MAX_MULTIPLIER)