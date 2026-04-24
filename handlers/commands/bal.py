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
    async def balance_command(client, message):

        user_id = message.from_user.id
        user_data = utils.get_user(user_id)

        if user_data is None:
            return await message.reply(
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

        await message.reply(
            msg,
            reply_markup=kb
        )

    @bot.on_callback_query(filters.regex("^exit:"))
    async def balance_callback(client, call):

        user_id = int(call.data.split(":", 1)[1])

        if call.from_user.id != user_id:
            return await call.answer(
                "Not your vault.",
                show_alert=True
            )

        await call.message.delete()

        await client.send_message(
            call.message.chat.id,
            "Exited from balance vault."
        )

        await call.answer()