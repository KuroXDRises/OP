import telebot
import handlers
from config import Config

def create_bot():
    token = Config.get_variable("Token")
    return telebot.TeleBot(token, parse_mode="HTML")

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

if __name__=="__main__":
    print("OnePieceSaga Bot Started...")
    bot.infinity_polling(skip_pending=True)