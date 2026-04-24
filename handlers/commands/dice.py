from pyrogram import filters
from pyrogram.types import *
import utils

base_multiplier = 1.15
MAX_MULTIPLIER = 1.92
MAX_BET = 15000


def dice_handler(bot):
    @bot.on_message(filters.command("dice"))
    def dice_command(client, message):
        user_id = message.from_user.id
        data = utils.get_user(user_id)

        if data is None:
            return message.reply("You are not registered yet!")

        args = message.text.split(" ", 1)

        if len(args) < 2:
            return message.reply("Usage: /dice {bet}\nExample: /dice 100")

        if not args[1].isdigit():
            return message.reply("Bet must be a valid number.")

        bet = int(args[1])

        if bet <= 0:
            return message.reply("Invalid bet amount.")

        if bet > MAX_BET:
            return message.reply("Max Bet Is 15000")

        if bet % 100 != 0:
            return message.reply("Bet must be multiple of 100.")

        if data["currency"]["beli"] < bet:
            return message.reply("Not enough balance.")

        msg = f"""<b>〘 🏴‍☠️ Gamble Panel 〙</b>

➩ Bet: <code>{bet}</code>
➩ Max Multiplier: <code>{MAX_MULTIPLIER}x</code>

👇 Choose your fate, Pirate:
"""

        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("High", callback_data=f"high:{bet}:{user_id}"),
                    InlineKeyboardButton("Low", callback_data=f"low:{bet}:{user_id}")
                ],
                [
                    InlineKeyboardButton("Even", callback_data=f"even:{bet}:{user_id}"),
                    InlineKeyboardButton("Odd", callback_data=f"odd:{bet}:{user_id}")
                ]
            ]
        )

        return message.reply(msg, reply_markup=kb)


def get_multiplier(bet):
    factor = bet / 500
    m = base_multiplier + (factor * 0.75 * base_multiplier)
    return min(m, MAX_MULTIPLIER)