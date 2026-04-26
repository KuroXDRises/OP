from pyrogram import Client
import handlers
from config import Config

def create_bot():
    return Client(
        "OnePieceSagaBot",
        bot_token=Config.get_variable("Token"),
        api_id=int(Config.get_variable("ApiId")),
        api_hash=Config.get_variable("ApiHash")
    )

bot = create_bot()

handlers.start_handler(bot)
handlers.start_callback(bot)
handlers.stats_handler(bot)
handlers.stats_callback(bot)
handlers.balance_handler(bot)
handlers.inventory_handler(bot)
handlers.dice_handler(bot)
handlers.dice_callback(bot)
handlers.pay_handler(bot)
handlers.spin_handler(bot)
handlers.spin_callback(bot)
handlers.my_char_handler(bot)
handlers.my_char_callbacks(bot)
handlers.cancel_tasks_callback(bot)
handlers.add_char_handler(bot)
handlers.profile_handler(bot)

if __name__ == "__main__":
    print("OnePieceSaga Bot Started...")
    bot.run()