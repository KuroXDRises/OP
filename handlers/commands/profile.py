from pyrogram import filters
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
        bg.paste(img, (310, 220), img)
    draw = ImageDraw.Draw(bg)
    try:
        font1 = ImageFont.truetype(
            "one piece font.ttf",
            62
        )
        font2 = ImageFont.truetype(
            "one piece font.ttf",
            58
        )
    except:
        font1 = ImageFont.load_default()
        font2 = ImageFont.load_default()
    name = str(data.get("name", "Unknown"))
    bounty = str(data.get("bounty", 0))
    draw.text(
        (305, 470),
        name,
        font=font1,
        fill="white"
    )
    draw.text(
        (355, 565),
        bounty,
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

def build_profile_caption(data):
    return f"""
✧═══════════════✧
        PIRATE PROFILE
✧═══════════════✧

➤ Captain   : {data["name"]}
➤ ID        : {data["_id"]}
➤ Title     : {data["title"]}
➤ Rank      : {data["rank"]}

☠ A pirate rising on the seas
✧═══════════════✧

❖═══════════════❖
       PROGRESS REPORT
❖═══════════════❖

➩ Level     : {data["level"]}
➩ XP        : {data["exp"]}/{data["max_exp"]}
➩ Power     : {data["power"]}

〘 Keep sailing forward 〙
❖═══════════════❖

✞═══════════════✞
        TREASURE HOLD
✞═══════════════✞

✟ Bounty    : ฿ {data["bounty"]}
✟ Beli      : ฿ {data["currency"]["beli"]}
✟ Neo Frag  : {data["currency"]["neo_fragments"]}
✟ Tickets   : {data["currency"]["devil_tickets"]}

⚔ Wealth attracts danger
✞═══════════════✞

✦═══════════════✦
         CREW STATUS
✦═══════════════✦

➤ Characters : {len(data["chars"])}
➤ Wins       : {data["wins"]}
➤ Loss       : {data["loss"]}
➤ Draw       : {data["draw"]}

☠ Build the strongest crew
✦═══════════════✦

✧═══════════════✧
        WORLD STATUS
✧═══════════════✧

➤ Region    : {data["region"]}
➤ Story     : {data["story_progress"]}
➤ Ship      : {data["ship"]}
➤ Crew      : {data["crew"] if data["crew"] else "None"}

❖ The Grand Line awaits...
✧═══════════════✧
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
        img = await create_profile_picture(
            bot,
            data
        )
        caption = build_profile_caption(data)
        await message.reply_photo(
            photo=img,
            caption=caption
        )
        try:
            os.remove(img)
        except:
            pass