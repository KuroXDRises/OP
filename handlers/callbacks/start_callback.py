from telebot import types
import utils
from db.starters import starters

def welcome_message(user):
    first_name = user.first_name or "Captain"
    username = f"@{user.username}" if user.username else "No Username"
    user_id = user.id

    return f"""
🏴‍☠️ Welcome aboard, {first_name}!

Your pirate registration is complete successfully.

👤 Captain Info
🪪 Name: {first_name}
🔖 Username: {username}
🆔 ID: {user_id}

⚓ You are now ready to sail the seas, recruit crewmates, gain power, and raise your bounty across the Grand Line.

📜 Starter Commands

👤 /profile - View your pirate profile
⭐ /char - View selected main character stats
👥 /mychars - View all your collected characters
🎒 /inv - Check your inventory items
💰 /bal - Check your currencies & balance
⚔️ /battle - Fight enemies or rivals
🗺️ /quest - Start missions
🏴‍☠️ /crew - Manage your crew
🎰 /spin - Summon new characters
🏆 /rank - Leaderboard rankings

🌊 Set sail now and become the next Pirate King!
"""

def start_callback(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("register:"))
    def register_callback(call):
        bot.answer_callback_query(
            call.id
            )
        user_id = int(call.data.split(":", 1)[1])
        if utils.get_user(user_id) is not None:
            bot.answer_callback_query(
                call.id,
                "You already registered!",
                show_alert=True
                )
            return
        char_data = utils.prepare_starters_data(0)
        msg = utils.starter_stats_message(char_data)
        pic = char_data["pic"]
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(
                "Previous", callback_data=f"select_char:0"
                ),
            types.InlineKeyboardButton(
                "Next", callback_data=f"select_char:1"
                )
                )
        kb.add(
            types.InlineKeyboardButton(
                "Choose", callback_data=f"choose_char:0"
                )
                )
                
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
            )
        bot.send_photo(
            call.message.chat.id,
            photo=pic,
            caption=msg,
            reply_markup=kb
            )
    @bot.callback_query_handler(func=lambda call: call.data.startswith("select_char:"))
    def previous_next_callback(call):
        bot.answer_callback_query(
            call.id
            )
        index = int(call.data.split(":", 1)[1])
        total = len(starters)
        if index<0:
            index = total-1
        if index>=total:
            index = 0
        char = utils.prepare_starters_data(index)
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(
                "Previous", callback_data=f"select_char:{index-1}"
                ),
            types.InlineKeyboardButton(
                "Next", callback_data=f"select_char:{index+1}"
                )
                )
        kb.add(
            types.InlineKeyboardButton(
                "Choose", callback_data=f"choose_char:{index}"
                )
                )
        bot.edit_message_media(
            media=types.InputMediaPhoto(
                char["pic"],
                caption=utils.starter_stats_message(char),
                parse_mode="HTML"
                ),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=kb
            )
    @bot.callback_query_handler(func=lambda call: call.data.startswith("choose_char:"))
    def choose_character_callback(call):
        bot.answer_callback_query(
            call.id
            )
        user_id = call.from_user.id
        index = int(call.data.split(":", 1)[1])
        char = utils.prepare_starters_data(index)
        if utils.get_user(user_id) is not None:
            return bot.answer_callback_query(
                call.id,
                "You already registered!",
                show_alert=True
                )
        utils.create_user(call.from_user, char)
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=welcome_message(call.from_user),
            parse_mode="HTML"
            )