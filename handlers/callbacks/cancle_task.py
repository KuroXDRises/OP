from pyrogram import filters, types
from pyrogram.enums import (
    ButtonStyle as BS,
    ParseMode
)
import utils
from handlers.commands.mychar import (
    create_sorted_char_data,
    create_mychar_keyboard
)

def cancel_tasks_callback(bot):
    @bot.on_callback_query(filters.regex("^cancel_task:"))
    async def cancel_tasks(_, call):
        user_id = int(call.data.split(":", 1)[1])
        if call.from_user.id != user_id:
            return await call.answer(
                "This button is not for you.",
                show_alert=True
            )
        data = utils.get_user(user_id)
        if data is None:
            return await call.answer(
                "User data not found.",
                show_alert=True
            )
        sort_by = data.get("sort", "level")
        display_by = data.get("display", "level")
        mode = data.get("order", "descending")
        msg = create_sorted_char_data(
            data,
            sort_by,
            display_by,
            mode
        )
        kb = create_mychar_keyboard(user_id)
        await call.message.edit_text(
            msg,
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )
        await call.answer("Returned successfully.")