from pyrogram import filters
from pyrogram.enums import ParseMode
from config import Config
import utils

def add_char_handler(bot):
    @bot.on_message(filters.command("addchar"))
    async def addchar_command(_, message):
        user_id = message.from_user.id
        # Only Devs
        devs_raw = str(Config.get_variable("DEVS"))
        dev_ids = [int(x.strip()) for x in devs_raw.split(",") if x.strip()]
        if user_id not in dev_ids:
            return await message.reply(
                "❌ This command is only for developers."
            )
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            return await message.reply(
                "Usage:\n"
                "<code>/addchar user_id character_name</code>\n\n"
                "Example:\n"
                "<code>/addchar 123456789 Zoro</code>",
                parse_mode=ParseMode.HTML
            )
        # Get target user id
        try:
            target_id = int(args[1])
        except:
            return await message.reply(
                "❌ Invalid user id."
            )
        char_name = args[2].strip()
        data = utils.get_user(target_id)
        if data is None:
            return await message.reply(
                "❌ Target user not registered."
            )
        # Find character in DB
        char_data = utils.get_char(char_name)
        if char_data is None:
            return await message.reply(
                f"❌ Character <b>{char_name}</b> not found.",
                parse_mode=ParseMode.HTML
            )
        # Duplicate check
        already = next(
            (
                x for x in data["chars"]
                if x["name"].lower() == char_name.lower()
            ),
            None
        )
        if already:
            return await message.reply(
                "⚠️ User already owns this character."
            )
        # Add character
        data["chars"].append(char_data)
        utils.save_user(data)
        await message.reply(
            f"""
<b>✅ Character Added Successfully</b>

👤 User ID: <code>{target_id}</code>
⭐ Character: <b>{char_data['name']}</b>

Developer action completed.
""",
            parse_mode=ParseMode.HTML
        )