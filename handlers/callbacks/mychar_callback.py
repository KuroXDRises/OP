from pyrogram import filters, types
from handlers.commands.mychar import *
from pyrogram.enums import (
    ParseMode,
    ChatType,
    ButtonStyle
)
from config import Config
import utils

def my_char_callbacks(bot):
    @bot.on_callback_query(filters.regex("^sort:"))
    async def change_char_sorter(_, call):
        user_id = int(call.data.split(":", 1)[1])
        if call.from_user.id != user_id:
            return await call.answer(
                "This button is not for you.",
                show_alert=True
            )
        data = utils.get_user(user_id)
        if data is None:
            return await call.answer(
                Config.get_variable("NotRegisterMessage"),
                show_alert=True
            )
        msg = "<b>Select a sorting method below.</b>\n\n"
        msg += f"<b>Current:</b> <code>{data.get('sort', 'level')}</code>"
        buttons = []
        for sort_type in sort_types:
            buttons.append(
                [
                    types.InlineKeyboardButton(
                        sort_type.title(),
                        callback_data=f"sort_user:{sort_type}:{user_id}",
                        style=ButtonStyle.DEFAULT
                    )
                ]
            )
        buttons.append(
            [
                types.InlineKeyboardButton(
                    "Cancel",
                    callback_data=f"cancel_task:{user_id}",
                    style=ButtonStyle.DANGER
                )
            ]
        )
        kb = types.InlineKeyboardMarkup(buttons)
        await call.message.edit_text(
            msg,
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )
        await call.answer()
    @bot.on_callback_query(filters.regex('^sort_user:'))
    async def sort_user_callback(_, call):
        _id = int(call.data.split(":", 2)[2])
        _sort_type = call.data.split(":", 2)[1]
        if call.from_user.id != _id:
            return
        data = utils.get_user(_id)
        data["sort"] = _sort_type
        utils.save_user(data)
        keyboard = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton(
                        "Return",
                        callback_data=f"cancel_task:{_id}",
                        style=ButtonStyle.PRIMARY
                        )
                    ]
                ]
            )
        await call.message.edit_text(
            f"Characters sorted successfully\nSort Type: {_sort_type}.",
            reply_markup=keyboard
            )
    @bot.on_callback_query(filters.regex("^display:"))
    async def change_char_sorter(_, call):
        user_id = int(call.data.split(":", 1)[1])
        if call.from_user.id != user_id:
            return await call.answer(
                "This button is not for you.",
                show_alert=True
            )
        data = utils.get_user(user_id)
        if data is None:
            return await call.answer(
                Config.get_variable("NotRegisterMessage"),
                show_alert=True
            )
        msg = "<b>Select a display method below.</b>\n\n"
        msg += f"<b>Current:</b> <code>{data.get('display', 'level')}</code>"
        buttons = []
        for sort_type in sort_types:
            buttons.append(
                [
                    types.InlineKeyboardButton(
                        sort_type.title(),
                        callback_data=f"display_user:{sort_type}:{user_id}",
                        style=ButtonStyle.DEFAULT
                    )
                ]
            )
        buttons.append(
            [
                types.InlineKeyboardButton(
                    "Cancel",
                    callback_data=f"cancel_task:{user_id}",
                    style=ButtonStyle.DANGER
                )
            ]
        )
        kb = types.InlineKeyboardMarkup(buttons)
        await call.message.edit_text(
            msg,
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )
        await call.answer()
    @bot.on_callback_query(filters.regex('^display_user:'))
    async def sort_user_callback(_, call):
        _id = int(call.data.split(":", 2)[2])
        _sort_type = call.data.split(":", 2)[1]
        if call.from_user.id != _id:
            return
        data = utils.get_user(_id)
        data["display"] = _sort_type
        utils.save_user(data)
        keyboard = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton(
                        "Return",
                        callback_data=f"cancel_task:{_id}",
                        style=ButtonStyle.PRIMARY
                        )
                    ]
                ]
            )
        await call.message.edit_text(
            f"Characters sorted successfully\nSort Type: {_sort_type}.",
            reply_markup=keyboard
            )
    @bot.on_callback_query(filters.regex("^order:"))
    async def change_order(_, call):
        _id = int(call.data.split(":", 1)[1])
        if call.from_user.id != _id:
            return
        data = utils.get_user(_id)
        keyboard = types.InlineKeyboardMarkup(
           [
               [
                   types.InlineKeyboardButton(
                       "Ascending",
                       callback_data=f"set_order:ascending:{_id}",
                       style=ButtonStyle.PRIMARY
                       ),
                    types.InlineKeyboardButton(
                        "Descending",
                        callback_data=f"set_order:descending:{_id}",
                        style=ButtonStyle.PRIMARY
                        )
                   ]
               ]
           )
        msg = f"Choose the order below\n\n1• Ascending\n2• Descending.\n\nCurrent: {data['order']}"
        await call.message.edit_text(
            msg,
            reply_markup=keyboard
            )
        @bot.on_callback_query(filters.regex('^set_order:'))
        async def set_order(_, call):
            mode = call.data.split(":", 2)[1]
            _id = int(call.data.split(":", 2)[2])
            if call.from_user.id != _id:
                return
            data = utils.get_user(_id)
            data["order"] = mode
            utils.save_user(data)
            keyboard = types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(
                            "Return",
                            callback_data=f"cancel_task:{_id}",
                            style=ButtonStyle.PRIMARY
                            )
                        ]
                    ]
                )
            await call.message.edit_text(
                f"Order changed successfully to {mode}",
                reply_markup=keyboard
                )