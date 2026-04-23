from telebot import types
import utils

def inventory_panel_msg(data):
    fruit = data["devil_fruit"]
    inv = data["inv"]
    currency = data["currency"]

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

──────────────────────

‹ Protect your loot.
‹ Rule the seas.
‹ Chase the One Piece.
"""

def inventory_handler(bot):
    @bot.message_handler(commands=["inv"])
    def inv_command(message):
        user_id = message.from_user.id
        data = utils.get_user(user_id)
        if data is None:
            return bot.reply_to(
                message,
                "You are not registered yet!"
                )
        msg = inventory_panel_msg(data)
        pic = "https://i.ibb.co/NnZQ53cb/7a41459c71f1.jpg"
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(
                "Exit", callback_data=f"inv_exit:{user_id}"
                )
            )
        bot.send_photo(
            message.chat.id,
            photo=pic,
            caption=msg,
            reply_markup=kb
            )
    @bot.callback_query_handler(func=lambda call: call.data.startswith("inv_exit:"))
    def inventory_exit(call):
        user_id = int(call.data.split(":", 1)[1])
        if call.from_user.id != user_id:
            return
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
            )
        bot.send_message(
            call.message.chat.id,
            "Exited from Inventory Panel."
            )
        