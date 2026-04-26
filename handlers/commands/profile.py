from pyrogram import (
    filters,
    types
    )
from pyrogram.enums import (
    ParseMode,
    ButtonStyle
    )
from PIL import (
    Image,
    ImageDraw,
    ImageFont
    )
import os
import utils


async def create_profile_picture(bot, data):
    user_id = data["_id"]
    bg = Image.open("profile.jpg").convert("RGBA")
    file_path = None

    try:
        photos = []
        async for p in bot.get_chat_photos(user_id, limit=1):
            photos.append(p)

        if photos:
            file_path = await bot.download_media(
                photos[0].file_id
            )
    except:
        file_path = None

    if file_path and os.path.exists(file_path):
        img = Image.open(file_path).convert("RGBA")
        img = img.resize((220, 220))

        mask = Image.new("L", (220, 220), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 220, 220), fill=255)

        img.putalpha(mask)

    draw = ImageDraw.Draw(bg)

    try:
        font1 = ImageFont.truetype("one piece font.ttf", 62)
        font2 = ImageFont.truetype("one piece font.ttf", 58)
    except:
        font1 = ImageFont.load_default()
        font2 = ImageFont.load_default()

    draw.text(
        (305, 510),
        str(data["name"]),
        font=font1,
        fill="white"
    )

    draw.text(
        (355, 620),
        str(data["bounty"]),
        font=font2,
        fill="white"
    )

    output = f"profile_{user_id}.png"
    bg.save(output)

    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except:
        pass

    return output


def profile_buttons(user_id):
    return types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    "Stats",
                    callback_data=f"profile_stats:{user_id}",
                    style=ButtonStyle.DEFAULT
                ),
                types.InlineKeyboardButton(
                    "Wealth",
                    callback_data=f"profile_wealth:{user_id}",
                    style=ButtonStyle.DEFAULT
                )
            ],
            [
                types.InlineKeyboardButton(
                    "Battle",
                    callback_data=f"profile_battle:{user_id}",
                    style=ButtonStyle.DEFAULT
                ),
                types.InlineKeyboardButton(
                    "Activity",
                    callback_data=f"profile_activity:{user_id}",
                    style=ButtonStyle.DEFAULT
                )
            ],
            [
                types.InlineKeyboardButton(
                    "Close",
                    callback_data=f"profile_close:{user_id}",
                    style=ButtonStyle.DANGER
                )
            ]
        ]
    )


def stats_msg(data):
    return f"""
✧═══════════════✧
      PIRATE STATS
✧═══════════════✧

➤ Name     : {data["name"]}
➤ ID       : {data["_id"]}
➤ Rank     : {data["rank"]}
➤ Title    : {data["title"]}

➩ Level    : {data["level"]}
➩ XP       : {data["exp"]}/{data["max_exp"]}
➩ Power    : {data["power"]}

☠ Rise higher on the seas
✧═══════════════✧
"""


def wealth_msg(data):
    return f"""
✞═══════════════✞
       TREASURE HOLD
✞═══════════════✞

✟ Bounty   : ฿ {data["bounty"]}
✟ Beli     : ฿ {data["currency"]["beli"]}
✟ Neo Frag : {data["currency"]["neo_fragments"]}
✟ Tickets  : {data["currency"]["devil_tickets"]}

➤ Characters : {len(data["chars"])}

⚔ Wealth attracts rivals
✞═══════════════✞
"""


def battle_msg(data):
    return f"""
❖═══════════════❖
       BATTLE RECORD
❖═══════════════❖

➤ Wins     : {data["wins"]}
➤ Loss     : {data["loss"]}
➤ Draw     : {data["draw"]}

➤ Region   : {data["region"]}
➤ Story    : {data["story_progress"]}
➤ Ship     : {data["ship"]}

☠ Glory is earned in war
❖═══════════════❖
"""


def activity_msg(data):
    return f"""
✦═══════════════✦
      LAST ACTIVITY
✦═══════════════✦

➤ Daily Claim :
{data["last_daily"]}

➤ Transaction :
{data["last_transaction"]}

➤ Battle :
{data["last_battle"]}

➤ Spin :
{data["last_spin"]}

➤ Created :
{data["created_at"]}

☠ Every move leaves a mark
✦═══════════════✦
"""


def profile_handler(bot):

    @bot.on_message(filters.command("profile"))
    async def profile_command(_, message):

        user_id = message.from_user.id
        data = utils.get_user(user_id)

        if data is None:
            return await message.reply(
                "Please start the bot first."
            )

        img = await create_profile_picture(bot, data)

        await message.reply_photo(
            photo=img,
            caption=stats_msg(data),
            reply_markup=profile_buttons(user_id),
            parse_mode=ParseMode.HTML
        )

        try:
            os.remove(img)
        except:
            pass

    @bot.on_callback_query(filters.regex("^profile_"))
    async def profile_callbacks(_, call):

        action = call.data.split(":")[0]
        user_id = int(call.data.split(":")[1])

        if call.from_user.id != user_id:
            return await call.answer(
                "This panel is not for you.",
                show_alert=True
            )

        data = utils.get_user(user_id)

        if data is None:
            return await call.answer(
                "User not found.",
                show_alert=True
            )

        if action == "profile_stats":
            text = stats_msg(data)

        elif action == "profile_wealth":
            text = wealth_msg(data)

        elif action == "profile_battle":
            text = battle_msg(data)

        elif action == "profile_activity":
            text = activity_msg(data)

        elif action == "profile_close":
            return await call.message.delete()

        await call.message.edit_caption(
            caption=text,
            reply_markup=profile_buttons(user_id),
            parse_mode=ParseMode.HTML
        )

        await call.answer()