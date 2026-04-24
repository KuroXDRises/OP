from pyrogram import filters
from pyrogram import types
from pyrogram.enums import ButtonStyle, ParseMode

def spin_callback(bot):
    @bot.on_callback_query(filters.regex("spin:"))
    async def spin_command_continue(_, call):
        spins = int(call.data.split(":", 2)[1])
        user_id = (call.data.split(":", 2)[2])
        if call.from_user.id != user_id:
            return
        kb = types.InlineKeyboardMarkup(
            [
                types.InlineKeyboardButton(
                    "Confirm",
                    callback_data=f"confirm_spin:{spins}:{user_id}",
                    style=ButtonStyle.SUCCESS
                    ),
                types.InlineKeyboardButton(
                    "Cancle",
                    callback_data=f"cancle_spin:{user_id}",
                    style=ButtonStyle.DANGER
                    )
                ]
            )
        await call.message.edit_text(
            f"Are you sure to confirm {spins}x spin?\nClick the button below to confirm.",
            reply_markup=kb
            )