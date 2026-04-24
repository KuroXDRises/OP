import utils
from pyrogram import filters


def pay_handler(bot):
    @bot.on_message(filters.command("pay"))
    def pay_command(client, message):

        user_id = message.from_user.id
        data = utils.get_user(user_id)

        if data is None:
            return message.reply(
                "Register on the bot first."
            )

        if not message.reply_to_message:
            return message.reply(
                "Reply to a user to send them Beli."
            )

        target_id = message.reply_to_message.from_user.id

        if target_id == user_id:
            return message.reply(
                "You cannot transfer Beli to yourself."
            )

        data2 = utils.get_user(target_id)

        if data2 is None:
            return message.reply(
                "That user is not registered yet."
            )

        args = message.text.split(" ", 1)

        if len(args) < 2:
            return message.reply(
                "Usage: /pay {amount}"
            )

        am = args[1].strip()

        if not am.isdigit():
            return message.reply(
                "Please send a valid number."
            )

        am = int(am)

        if am <= 0:
            return message.reply(
                "Amount must be greater than 0."
            )

        if am > data["currency"]["beli"]:
            return message.reply(
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

        message.reply(
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
"""
        )