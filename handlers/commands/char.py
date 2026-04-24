from pyrogram import filters
from pyrogram.types import *
import utils

def stats_handler(bot):
    @bot.on_message(filters.command(["stats", "info"]))
    def stats_command(client, message):
        user_id = message.from_user.id
        data = utils.get_user(user_id)

        if data is None:
            return message.reply(
                "Sorry! I cant get your data because you did not started the bot yet.\nPlease start the bot first."
            )

        args = message.text.split(" ", 1)

        if len(args) < 2:
            return message.reply(
                "No chatacter name found in your message."
            )

        char_name = args[1].strip()

        char_data = next(
            (
                x for x in data["chars"]
                if x["name"].lower() == char_name.lower()
            ),
            None
        )

        if not char_data:
            return message.reply(
                "You do not own this character."
            )

        msg = utils.load_stats_msg(1, char_data)

        kb = InlineKeyboardMarkup(
            [
                [
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
                ]
            ]
        )

        message.reply_photo(
            photo=char_data["pic"],
            caption=msg,
            reply_markup=kb
        )