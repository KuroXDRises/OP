from telebot import types
import utils


def stats_callback(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("data:"))
    def info_callback(call):
        bot.answer_callback_query(call.id)

        page = int(call.data.split(":", 3)[1])
        user_id = int(call.data.split(":", 3)[2])
        char_name = call.data.split(":", 3)[3]

        if call.from_user.id != user_id:
            return bot.answer_callback_query(
                call.id,
                "This button is not for you.",
                show_alert=True
            )

        kb = types.InlineKeyboardMarkup()

        if page == 1:
            kb.add(
                types.InlineKeyboardButton(
                    "Progress",
                    callback_data=f"data:2:{user_id}:{char_name}"
                ),
                types.InlineKeyboardButton(
                    "Stats",
                    callback_data=f"data:3:{user_id}:{char_name}"
                ),
                types.InlineKeyboardButton(
                    "Skills",
                    callback_data=f"data:4:{user_id}:{char_name}"
                )
            )

        elif page == 2:
            kb.add(
                types.InlineKeyboardButton(
                    "Info",
                    callback_data=f"data:1:{user_id}:{char_name}"
                ),
                types.InlineKeyboardButton(
                    "Stats",
                    callback_data=f"data:3:{user_id}:{char_name}"
                ),
                types.InlineKeyboardButton(
                    "Skills",
                    callback_data=f"data:4:{user_id}:{char_name}"
                )
            )

        elif page == 3:
            kb.add(
                types.InlineKeyboardButton(
                    "Info",
                    callback_data=f"data:1:{user_id}:{char_name}"
                ),
                types.InlineKeyboardButton(
                    "Progress",
                    callback_data=f"data:2:{user_id}:{char_name}"
                ),
                types.InlineKeyboardButton(
                    "Skills",
                    callback_data=f"data:4:{user_id}:{char_name}"
                )
            )

        elif page == 4:
            kb.add(
                types.InlineKeyboardButton(
                    "Info",
                    callback_data=f"data:1:{user_id}:{char_name}"
                ),
                types.InlineKeyboardButton(
                    "Progress",
                    callback_data=f"data:2:{user_id}:{char_name}"
                ),
                types.InlineKeyboardButton(
                    "Stats",
                    callback_data=f"data:3:{user_id}:{char_name}"
                )
            )

        data = utils.get_user(user_id)

        char = next(
            (
                x for x in data["chars"]
                if x["name"].lower() == char_name.lower()
            ),
            None
        )

        if char is None:
            return

        msg = utils.load_stats_msg(page, char)

        bot.edit_message_caption(
            caption=msg,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=kb
        )