from pyrogram import filters
from pyrogram.types import *
import utils


def balance_message(data):
    currency = data["currency"]
    beli = currency["beli"]
    neo = currency["neo_fragments"]
    tickets = currency["devil_tickets"]

    return f"""
✦══════════════✦
        TREASURE VAULT
✦══════════════✦

〘 Pirate Account Status 〙

➣ Beli            : <code>{beli}</code>
➣ Neo Fragments   : <code>{neo}</code>
➣ Devil Tickets   : <code>{tickets}</code>

❖ Wealth decides power on sea
❖ Spend wisely, grow greatly

✦═════════════✦
"""


def balance_handler(bot):

    @bot.on_message(filters.command("bal"))
    def balance_command(client, message):
        user_id = message.from_user.id
        user_data = utils.get_user(user_id)

        if user_data is None:
            return message.reply(
                "You are not registered yet!"
            )

        msg = balance_message(user_data)

        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Exit Vault",
                        callback_data=f"exit:{user_id}"
                    )
                ]
            ]
        )

        message.reply(
            msg,
            reply_markup=kb
        )

    @bot.on_callback_query(filters.regex("^exit:"))
    def balance_callback(client, call):

        user_id = int(call.data.split(":", 1)[1])

        if call.from_user.id != user_id:
            return

        call.message.delete()

        client.send_message(
            call.message.chat.id,
            "Exited from balance vault."
        )