from pyrogram import filters, types
from pyrogram.enums import (
    ParseMode,
    ChatType,
    ButtonStyle
)
import utils

sort_types = {
    "bounty",
    "level",
    "hp",
    "attack",
    "defense",
    "speed",
    "crit_rate",
    "stamina"
}

def create_sorted_char_data(user, sort_by, display_by, mode="descending"):
    chars = user["chars"]
    if mode == "descending":
        new_chars = sorted(
            chars,
            key=lambda x:
                x.get(sort_by, 0),
            reverse=True
        )
    else:
        new_chars = sorted(
            chars,
            key=lambda x:
                x.get(sort_by, 0)
        )
    text = "<b><i>🏴‍☠️ Your Characters Panel</i></b>\n\n"
    for i, char in enumerate(new_chars, start=1):
        display = char.get(display_by, 0)
        text += f'<b>{i}. {char["name"]}</b> | {display}\n'
    return text
def create_mychar_keyboard(user_id):
    kb = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    "Sort",
                    callback_data=f"sort:{user_id}",
                    style=ButtonStyle.DEFAULT
                    ),
                types.InlineKeyboardButton(
                    "Display",
                    callback_data=f"display:{user_id}",
                    style=ButtonStyle.DEFAULT
                    )
                ],
            [
                types.InlineKeyboardButton(
                    "Order",
                    callback_data=f'order:{user_id}',
                    style=ButtonStyle.DEFAULT
                    )
                ],
            [
                types.InlineKeyboardButton(
                    "Exit",
                    callback_data=f'exit_mychar:{user_id}',
                    style=ButtonStyle.DANGER
                    )
                ]
            ]
        )
    return kb
def my_char_handler(bot):
    @bot.on_message(filters.command("mychar"))
    async def mychar_command(_,m):
        user_id = m.from_user.id
        data = utils.get_user(user_id)
        if data is None:
            return await m.reply(
                "Please Start the bot first. I am not able to fetch your data."
                )
        if len(data["chars"])==0:
            return m.reply(
                "You dont have any characters."
                )
        sort_by = data["sort"]
        display_by = data["display"]
        mode = data["order"]
        msg = create_sorted_char_data(data, sort_by, display_by, mode)
        kb = create_mychar_keyboard(user_id)
        await m.reply(
            msg,
            reply_markup=kb
            )