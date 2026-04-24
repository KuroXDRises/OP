from pyrogram import filters
from pyrogram.types import *
import utils


def stats_callback(bot):
    @bot.on_callback_query(filters.regex("^data:"))
    def info_callback(client, call):

        page = int(call.data.split(":", 3)[1])
        user_id = int(call.data.split(":", 3)[2])
        char_name = call.data.split(":", 3)[3]

        if call.from_user.id != user_id:
            return call.answer(
                "This button is not for you.",
                show_alert=True
            )

        kb = InlineKeyboardMarkup([])

        if page == 1:
            kb = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "Progress",
                        callback_data=f"data:2:{user_id}:{char_name}"
                    ),
                    InlineKeyboardButton(
                        "Stats",
                        callback_data=f"data:3:{user_id}:{char_name}"
                    ),
                    InlineKeyboardButton(
                        "Skills",
                        callback_data=f"data:4:{user_id}:{char_name}"
                    )
                ]]
            )

        elif page == 2:
            kb = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "Info",
                        callback_data=f"data:1:{user_id}:{char_name}"
                    ),
                    InlineKeyboardButton(
                        "Stats",
                        callback_data=f"data:3:{user_id}:{char_name}"
                    ),
                    InlineKeyboardButton(
                        "Skills",
                        callback_data=f"data:4:{user_id}:{char_name}"
                    )
                ]]
            )

        elif page == 3:
            kb = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "Info",
                        callback_data=f"data:1:{user_id}:{char_name}"
                    ),
                    InlineKeyboardButton(
                        "Progress",
                        callback_data=f"data:2:{user_id}:{char_name}"
                    ),
                    InlineKeyboardButton(
                        "Skills",
                        callback_data=f"data:4:{user_id}:{char_name}"
                    )
                ]]
            )

        elif page == 4:
            kb = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "Info",
                        callback_data=f"data:1:{user_id}:{char_name}"
                    ),
                    InlineKeyboardButton(
                        "Progress",
                        callback_data=f"data:2:{user_id}:{char_name}"
                    ),
                    InlineKeyboardButton(
                        "Stats",
                        callback_data=f"data:3:{user_id}:{char_name}"
                    )
                ]]
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

        call.message.edit_caption(
            caption=msg,
            reply_markup=kb
        )

        call.answer()