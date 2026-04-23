from telebot import types
import utils

base_multiplier = 1.15
MAX_MULTIPLIER = 1.92
MAX_BET = 15000


def dice_handler(bot):

    @bot.message_handler(commands=["dice"])
    def dice_command(message):
        user_id = message.from_user.id
        data = utils.get_user(user_id)

        if data is None:
            return bot.reply_to(message, "You are not registered yet!")

        args = message.text.split(" ", 1)

        if len(args) < 2:
            return bot.reply_to(message, "Usage: /dice {bet}\nExample: /dice 100")

        if not args[1].isdigit():
            return bot.reply_to(message, "Bet must be a valid number.")

        bet = int(args[1])

        if bet <= 0:
            return bot.reply_to(message, "Invalid bet amount.")

        if bet > MAX_BET:
            return bot.reply_to(message, "Max Bet Is 15000")

        if bet % 100 != 0:
            return bot.reply_to(message, "Bet must be multiple of 100.")

        if data["currency"]["beli"] < bet:
            return bot.reply_to(message, "Not enough balance.")

        msg = f"""<b>〘 🏴‍☠️ Gamble Panel 〙</b>

➩ Bet: <code>{bet}</code>
➩ Max Multiplier: <code>{MAX_MULTIPLIER}x</code>

👇 Choose your fate, Pirate:
"""

        kb = types.InlineKeyboardMarkup()

        kb.add(
            types.InlineKeyboardButton("High", callback_data=f"high:{bet}:{user_id}"),
            types.InlineKeyboardButton("Low", callback_data=f"low:{bet}:{user_id}")
        )

        kb.add(
            types.InlineKeyboardButton("Even", callback_data=f"even:{bet}:{user_id}"),
            types.InlineKeyboardButton("Odd", callback_data=f"odd:{bet}:{user_id}")
        )

        return bot.reply_to(message, msg, reply_markup=kb, parse_mode="HTML")


def get_multiplier(bet):
    factor = bet / 500
    m = base_multiplier + (factor * 0.75 * base_multiplier)
    return min(m, MAX_MULTIPLIER)


def dice_callback(bot):

    @bot.callback_query_handler(func=lambda call: call.data.startswith(("high:", "low:", "even:", "odd:")))
    def handle(call):
        mode = call.data.split(":")[0]
        bet = int(call.data.split(":")[1])
        user_id = int(call.data.split(":")[2])

        if call.from_user.id != user_id:
            return

        user = utils.get_user(user_id)

        if not user or user["currency"]["beli"] < bet:
            return bot.answer_callback_query(call.id, "Not enough Beli!")

        utils.update_user(user_id, "beli", bet, mode="minus")

        roll = bot.send_dice(call.message.chat.id, emoji="🎲")
        num = roll.dice.value

        multiplier = get_multiplier(bet)

        win = False

        if mode == "high" and num >= 4:
            win = True
        elif mode == "low" and num <= 3:
            win = True
        elif mode == "even" and num % 2 == 0:
            win = True
        elif mode == "odd" and num % 2 != 0:
            win = True

        if win:
            reward = int(bet * multiplier)
            utils.update_user(user_id, "beli", reward, mode="add")

            bot.send_message(
                call.message.chat.id,
                f"""
🏴‍☠️ ONE PIECE GAMBLE WIN!

⚡ Result: {num}
💰 Bet: {bet} Beli
📈 Multiplier: {round(multiplier, 2)}x (CAP {MAX_MULTIPLIER}x)
🏆 Reward: {reward} Beli

☠️ "Luck is also a weapon of a Pirate King!"
— Grand Line
""",
                parse_mode="Markdown"
            )

        else:
            bot.send_message(
                call.message.chat.id,
                f"""
💀 DEFEAT AT SEA!

⚡ Result: {num}
💸 Lost: {bet} Beli

📉 Multiplier Used: {round(multiplier, 2)}x

☠️ "The sea shows no mercy..."
— Grand Line Rule
""",
                parse_mode="Markdown"
            )