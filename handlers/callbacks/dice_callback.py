from pyrogram import filters
import utils
import html

base_multiplier = 1.15
MAX_MULTIPLIER = 1.92


def get_multiplier(bet):
    factor = bet / 500
    m = base_multiplier + (factor * 0.75 * base_multiplier)
    return min(m, MAX_MULTIPLIER)


def dice_callback(bot):
    @bot.on_callback_query(filters.regex("^high:"))
    def high(client, call):
        handle_game(client, call, "high")

    @bot.on_callback_query(filters.regex("^low:"))
    def low(client, call):
        handle_game(client, call, "low")

    @bot.on_callback_query(filters.regex("^even:"))
    def even(client, call):
        handle_game(client, call, "even")

    @bot.on_callback_query(filters.regex("^odd:"))
    def odd(client, call):
        handle_game(client, call, "odd")


def handle_game(bot, call, mode):
    bet = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])

    if call.from_user.id != user_id:
        return call.answer("This button is not for you.", show_alert=True)

    user = utils.get_user(user_id)

    if not user or user["currency"]["beli"] < bet:
        return call.answer("Not enough Beli!", show_alert=True)

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

    call.message.delete()

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
            parse_mode="html"
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
            parse_mode="html"
        )

    call.answer()