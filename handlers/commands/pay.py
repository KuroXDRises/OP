import utils

def pay_handler(bot):
    @bot.message_handler(commands=["pay"])
    def pay_command(message):
        user_id = message.from_user.id
        data = utils.get_user(user_id)

        if data is None:
            return bot.reply_to(
                message,
                "Register on the bot first."
            )

        if not message.reply_to_message:
            return bot.reply_to(
                message,
                "Reply to a user to send them Beli."
            )

        target_id = message.reply_to_message.from_user.id

        if target_id == user_id:
            return bot.reply_to(
                message,
                "You cannot transfer Beli to yourself."
            )

        data2 = utils.get_user(target_id)

        if data2 is None:
            return bot.reply_to(
                message,
                "That user is not registered yet."
            )

        args = message.text.split(" ", 1)

        if len(args) < 2:
            return bot.reply_to(
                message,
                "Usage: /pay {amount}"
            )

        am = args[1].strip()

        if not am.isdigit():
            return bot.reply_to(
                message,
                "Please send a valid number."
            )

        am = int(am)

        if am <= 0:
            return bot.reply_to(
                message,
                "Amount must be greater than 0."
            )

        if am > data["currency"]["beli"]:
            return bot.reply_to(
                message,
                "You don't have enough Beli."
            )

        transfer_data = utils.transfer_beli(am)
        received = transfer_data["received"]
        tax = transfer_data["tax"]

        # Sender minus
        data["currency"]["beli"] -= am
        utils.save_user(data)

        # Receiver add
        data2["currency"]["beli"] += received
        utils.save_user(data2)

        bot.reply_to(
            message,
            f"""
<b>✧ Grand Line Transfer Complete ✧</b>

〘 Captain 〙 <b>{data["name"]}</b>
➩ Sent <code>{am}</code> Beli

〘 Receiver 〙 <b>{data2["name"]}</b>
➩ Received <code>{received}</code> Beli

〘 Marine Tax 〙 <code>{tax}</code> Beli

❖ The treasure ship arrived safely.
❖ Gold moves across the seas again.

<b>Continue your pirate journey.</b>
""",
            parse_mode="HTML"
        )