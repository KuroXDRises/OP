from telebot import types
import utils

def stats_handler(bot):
    @bot.message_handler(commands=["stats", "info"])
    def stats_command(message):
        user_id = message.from_user.id
        data = utils.get_user(user_id)
        if data is None:
            return bot.reply_to(
                message,
                "Sorry! I cant get your data because you did not started the bot yet.\nPlease start the bot first."
                )
        args = message.text.split(" ", 1)
        if len(args) < 2:
            return bot.reply_to(
                message,
                "No chatacter name found in your message."
                )
        char_name = args[1].strip()
        char_data = next(
            (
                x for x in data["chars"] if x["name"].lower() == char_name.lower()),
                None
                )
        if not char_data:
            return bot.reply_to(
                message,
                "You do not own this character."
                )
        msg = utils.load_stats_msg(1, char_data)
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(
                "Progress", callback_data=f"data:2:{user_id}:{char_name}"
                ),
            types.InlineKeyboardButton(
                "Stats", callback_data=f"data:3:{user_id}:{char_name}"
                ),
            types.InlineKeyboardButton(
                "Skills", callback_data=f"data:4:{user_id}:{char_name}"
                )
                )
        bot.send_photo(
            chat_id=message.chat.id,
            photo=char_data["pic"],
            caption=msg,
            reply_markup=kb,
            parse_mode="HTML"
            )