from pyrogram import (
    filters,
    types,
    enums
)
import pathlib
import json
import utils
from config import Config

BASE_PATH_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
USERS_PATH_DIR = BASE_PATH_DIR / Config.get_variable("UserPath")

def get_lb_users(sort_by="level", mode="strongest", limit=10):
    users = []
    for filex in USERS_PATH_DIR.glob("*.json"):
        data = json.loads(filex.read_text())
        users.append(data)
    reverse = mode == "strongest"
    users = sorted(
        users,
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse
    )
    return users[:limit]

def build_lb_text(users, title, stat):
    text = f"<b>🏴‍☠️ {title}</b>\n\n"
    for i, user in enumerate(users, start=1):
        name = user.get("name", "Unknown")
        value = user.get(stat, 0)
        text += (
            f"<b>{i}.</b> {name}\n"
            f"└ <code>{stat.title()}</code>: {value}\n\n"
        )
    return text


def lb_keyboard():
    return types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    "Level",
                    callback_data="lb:level"
                ),
                types.InlineKeyboardButton(
                    "Bounty",
                    callback_data="lb:bounty"
                )
            ],
            [
                types.InlineKeyboardButton(
                    "Wealth",
                    callback_data="lb:beli"
                ),
                types.InlineKeyboardButton(
                    "EXP",
                    callback_data="lb:exp"
                )
            ],
            [
                types.InlineKeyboardButton(
                    "Weakest",
                    callback_data="lb:weak"
                ),
                types.InlineKeyboardButton(
                    "Strongest",
                    callback_data="lb:strong"
                )
            ]
        ]
    )


def lb_handler(bot):
    @bot.on_message(filters.command("leaderboard"))
    async def lb_command(_, message):
        _id = message.from_user.id
        data = utils.get_user(_id)
        if data is None:
            return await message.reply_text(
                Config.get_variable(
                    "NotRegisterMessage"
                )
            )
        users = get_lb_users(
            "level",
            "strongest",
            10
            )
        msg = build_lb_text(
            users,
            "Top Pirates By Level",
            "level"
        )
        await message.reply_text(
            msg,
            reply_markup=lb_keyboard(),
            parse_mode=enums.ParseMode.HTML
        )

    @bot.on_callback_query(filters.regex("^lb:"))
    async def lb_callback(_, call):
        value = call.data.split(":")[1]
        if value == "level":
            users = get_lb_users(
                "level",
                "strongest",
                10
            )
            msg = build_lb_text(
                users,
                "Top Pirates By Level",
                "level"
            )
        elif value == "bounty":
            users = get_lb_users(
                "bounty",
                "strongest",
                10
            )
            msg = build_lb_text(
                users,
                "Top Pirates By Bounty",
                "bounty"
            )
        elif value == "beli":
            users = get_lb_users(
                "currency",
                "strongest",
                10
            )
            users = sorted(
                users,
                key=lambda x: x["currency"].get(
                    "beli",
                    0
                ),
                reverse=True
            )[:10]
            msg = "<b>💰 Richest Pirates</b>\n\n"
            for i, user in enumerate(
                users,
                start=1
            ):
                msg += (
                    f"<b>{i}.</b> {user['name']}\n"
                    f"└ <code>Beli</code>: "
                    f"{user['currency'].get('beli',0)}\n\n"
                )
        elif value == "exp":
            users = get_lb_users(
                "exp",
                "strongest",
                10
            )
            msg = build_lb_text(
                users,
                "Top Pirates By EXP",
                "exp"
            )
        elif value == "weak":
            users = get_lb_users(
                "level",
                "weakest",
                10
            )
            msg = build_lb_text(
                users,
                "Weakest Pirates",
                "level"
            )
        else:
            users = get_lb_users(
                "level",
                "strongest",
                10
            )
            msg = build_lb_text(
                users,
                "Strongest Pirates",
                "level"
            )
        await call.message.edit_text(
            msg,
            reply_markup=lb_keyboard(),
            parse_mode=enums.ParseMode.HTML
        )
        await call.answer()