from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import utils


def inventory_panel_msg(data):
    fruit = data["devil_fruit"]
    inv = data["inv"]

    fruit_name = fruit["owned"] if fruit["owned"] else "No Fruit"

    return f"""
╔════════════════════╗
         GRAND LINE STORAGE
╚════════════════════╝

〘 CAPTAIN LOG 〙
✧ Name      : {data["name"]}
✧ Title     : {data["title"]}
✧ Rank      : {data["rank"]}

─────────────────────

〘 DEVIL FRUIT VAULT 〙
✟ Fruit     : {fruit_name}
✟ Mastery   : {fruit["mastery"]}%
✟ Awakened  : {fruit["awakened"]}

─────────────────────

〘 PIRATE ITEMS 〙
❖ Boosters      : {inv["boosters"]}
❖ Rename Cards  : {inv["rename_cards"]}
❖ Revive Food   : {inv["revive_food"]}

─────────────────────

‹ Protect your loot.
‹ Rule the seas.
‹ Chase the One Piece.
"""


def inventory_handler(bot):
    @bot.on_message(filters.command("inv"))
    def inv_command(client, message):

        user_id = message.from_user.id
        data = utils.get_user(user_id)

        if data is None:
            return message.reply(
                "You are not registered yet!"
            )

        msg = inventory_panel_msg(data)

        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Exit",
                        callback_data=f"inv_exit:{user_id}"
                    )
                ]
            ]
        )

        message.reply_photo(
            photo="https://i.ibb.co/NnZQ53cb/7a41459c71f1.jpg",
            caption=msg,
            reply_markup=kb
        )

    @bot.on_callback_query(filters.regex("^inv_exit:"))
    def inventory_exit(client, call):

        user_id = int(call.data.split(":", 1)[1])

        if call.from_user.id != user_id:
            return call.answer("Not your panel.", show_alert=True)

        call.message.delete()

        call.message.reply(
            "Exited from Inventory Panel."
        )

        call.answer()