from pyrogram import filters
from pyrogram.types import *
from pyrogram.enums import ParseMode
import utils

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

    @bot.on_callback_query(filters.regex("^register:"))
    async def register_callback(client, call):

        user_id = int(call.data.split(":", 1)[1])

        if utils.get_user(user_id) is not None:
            return await call.answer(
                "You already registered!",
                show_alert=True
            )

        char_data = utils.prepare_starters_data(0)

        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Previous",
                        callback_data="select_char:0"
                    ),
                    InlineKeyboardButton(
                        "Next",
                        callback_data="select_char:1"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Choose",
                        callback_data="choose_char:0"
                    )
                ]
            ]
        )

        await call.message.delete()

        await client.send_photo(
            call.message.chat.id,
            photo=char_data["pic"],
            caption=utils.starter_stats_message(char_data),
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )

        await call.answer()

    @bot.on_callback_query(filters.regex("^select_char:"))
    async def previous_next_callback(client, call):

        index = int(call.data.split(":", 1)[1])
        total = len(starters)

        if index < 0:
            index = total - 1

        if index >= total:
            index = 0

        char = utils.prepare_starters_data(index)

        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Previous",
                        callback_data=f"select_char:{index-1}"
                    ),
                    InlineKeyboardButton(
                        "Next",
                        callback_data=f"select_char:{index+1}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Choose",
                        callback_data=f"choose_char:{index}"
                    )
                ]
            ]
        )

        await call.message.edit_media(
            media=InputMediaPhoto(
                media=char["pic"],
                caption=utils.starter_stats_message(char),
                parse_mode=ParseMode.HTML
            ),
            reply_markup=kb
        )

        await call.answer()

    @bot.on_callback_query(filters.regex("^choose_char:"))
    async def choose_character_callback(client, call):

        user_id = call.from_user.id
        index = int(call.data.split(":", 1)[1])

        char = utils.prepare_starters_data(index)

        if utils.get_user(user_id) is not None:
            return await call.answer(
                "You already registered!",
                show_alert=True
            )

        utils.create_user(call.from_user, char)

        await call.message.edit_caption(
            caption=welcome_message(call.from_user),
            parse_mode=ParseMode.HTML
        )

        await call.answer()