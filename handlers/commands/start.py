from telebot import types
import utils
from db.starters import *

def start_handler(bot):
    @bot.message_handler(commands=["start"])
    def start_command(message):
        user_id = message.from_user.id

        if message.chat.type != "private":
            return bot.reply_to(
                message,
                "🏴‍☠️ /start only works in private chat.\nPlease message me privately to begin your pirate journey."
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
            bot.reply_to(message, msg)
            return

        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(
                "🏴‍☠️ Register",
                callback_data=f"register:{user_id}"
            )
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

        bot.send_photo(
            message.chat.id,
            photo="https://i.ibb.co/ynrdpVw0/0179e4fd0ca6.png",
            caption=msg,
            reply_markup=kb
        )