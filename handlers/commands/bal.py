from telebot import types
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
    @bot.message_handler(commands=["bal"])
    def balance_command(message):
        user_id = message.from_user.id
        user_data = utils.get_user(user_id)
        if user_data is None:
            return bot.reply_to(
                message,
                "You are not registered yet!"
                )
        msg = balance_message(user_data)
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(
                "Exit Vault", callback_data=f"exit:{user_id}"
                )
                )
        bot.reply_to(
            message,
            msg,
            reply_markup=kb)
        @bot.callback_query_handler(func=lambda call: call.data.startswith("exit:"))
        def balance_callback(call):
            bot.answer_callback_query(
                call.id
                )
            user_id = int(call.data.split(":", 1)[1])
            if call.from_user.id != user_id:
                return
            bot.delete_message(
                call.message.chat.id,
                call.message.message_id
                )
            bot.send_message(
                call.message.chat.id,
                "Exited from balance vault."
                )