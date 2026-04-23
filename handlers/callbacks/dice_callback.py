from telebot import types
import utils
import random
import html

base_multiplier = 1.15
MAX_MULTIPLIER = 1.92


def get_multiplier(bet):
    factor = bet / 500
    m = base_multiplier + (factor * 0.75 * base_multiplier)
    return min(m, MAX_MULTIPLIER)


def dice_callback(bot):

    @bot.callback_query_handler(func=lambda call: call.data.startswith("high:"))
    def high(call):
        handle_game(bot, call, "high")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("low:"))
    def low(call):
        handle_game(bot, call, "low")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("even:"))
    def even(call):
        handle_game(bot, call, "even")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("odd:"))
    def odd(call):
        handle_game(bot, call, "odd")

def handle_game(bot, call, mode):
    bet = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])

    if call.from_user.id != user_id:
        return

    user = utils.get_user(user_id)

    if not user or user["currency"]["beli"] < bet:
        return bot.answer_callback_query(
            call.id,
            "Not enough Beli!"
        )

    utils.update_user(user_id, "beli", bet, mode="minus")

    roll_msg = bot.send_dice(
        call.message.chat.id,
        emoji="🎲"
    )

    num = roll_msg.dice.value
    multiplier = get_multiplier(bet)

    name = html.escape(call.from_user.first_name)

    win = False

    if mode == "high" and num >= 4:
        win = True
    elif mode == "low" and num <= 3:
        win = True
    elif mode == "even" and num % 2 == 0:
        win = True
    elif mode == "odd" and num % 2 != 0:
        win = True

    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )

    if win:
        reward = int(bet * multiplier)

        utils.update_user(
            user_id,
            "beli",
            reward,
            mode="add"
        )

        bot.send_message(
            call.message.chat.id,
            f"""
<b>✧ GRAND LINE JACKPOT ✧</b>

〘 Result 〙 <code>{num}</code>
〘 Bet     〙 <code>{bet}</code> Beli
〘 Pirate  〙 <a href="tg://user?id={call.from_user.id}">{name}</a>

〘 Boost   〙 <code>{round(multiplier,2)}x</code>
〘 Reward  〙 <code>{reward}</code> Beli

❖ Fortune smiles upon fearless pirates.
❖ The sea grants treasure today.
""",
            parse_mode="HTML"
        )

    else:
        bot.send_message(
            call.message.chat.id,
            f"""
<b>✧ STORM OF DEFEAT ✧</b>

〘 Result 〙 <code>{num}</code>
〘 Lost    〙 <code>{bet}</code> Beli
〘 Pirate  〙 <a href="tg://user?id={call.from_user.id}">{name}</a>

〘 Boost   〙 <code>{round(multiplier,2)}x</code>

❖ The sea takes what it wants.
❖ Return stronger, Captain.
""",
            parse_mode="HTML"
            )