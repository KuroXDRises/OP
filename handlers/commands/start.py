from pyrogram import filters, Client
from pyrogram.types import *
from pyrogram.enums import *
import utils

def start_handler(bot):
    @bot.on_message(filters.command("start"), group=1)
    async def start_command(client, message):
        user_id = message.from_user.id
        if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            return await message.reply(
                "🏴‍☠️ /start only works in private chat.\n"
                "Please message me privately to begin your pirate journey."
            )
        if utils.get_user(user_id) is not None:
            msg = """
🏴‍☠️ You are already registered, Captain!

Your pirate journey is already active in the One Piece world.

⚓ /profile - View your pirate stats
🎒 /inv - Check your items
⚔️ /battle - Fight enemies
🗺️ /quest - Start missions
💰 /bounty - View your bounty

Set sail and chase the Grand Line glory!
"""
            return await message.reply(msg)
        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏴‍☠️ Register",
                        callback_data=f"register:{user_id}"
                    )
                ]
            ]
        )
        msg = """
🏴‍☠️ Welcome to the Great One Piece World!

The seas are full of danger, treasure, rivals, and endless adventure.

Create your pirate identity, grow stronger, collect powerful allies, raise your bounty, and sail toward glory.

⚔️ Fight enemies
🗺️ Complete missions
🏝️ Explore islands
👑 Become a legendary captain

⬇️ Tap Register below to begin your pirate journey!
"""
        await message.reply_photo(
            photo="https://i.ibb.co/ynrdpVw0/0179e4fd0ca6.png",
            caption=msg,
            reply_markup=kb
        )