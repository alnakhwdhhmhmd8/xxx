
from pyrogram import Client as app, filters
from pyrogram.types import *
from pyrogram.enums import *
import config
from config import r as redus
import asyncio
from nudenet import NudeDetector
from aiohttp import ClientSession
from asyncio import run as RUN
import cv2
from Python_ARQ import ARQ
import os
ARQ_API_KEY = "OZJRWV-SAURXD-PMBUKF-GMVSNS-ARQ"
ARQ_API_URL = "https://arq.hamker.dev"

async def Dev_us(id, Dev_Zaid) -> bool:
   if id == 7728230165 or id == 7728230165:
      return True
   if id == int(redus.hget(Dev_Zaid + "music", "dev-bot")):
       return True

# تفعيل أو تعطيل الفلاتر عبر أوامر محددة
@app.on_message(filters.command("قفل الاباحي","") & ~filters.private)
async def enable_filter(client, message):
 if not redus.get(f'Disabsabahy:{client.me.id}'):
    chat_id = message.chat.id
    # تحقق من إذن المستخدم (المالك أو المسؤولين)
    chat_member = await client.get_chat_member(chat_id, message.from_user.id)
    if await Dev_us(message.from_user.id, str(client.me.id)) or  redus.sismember(f"{client.me.id}MSAED", message.from_user.id) or chat_member.status ==ChatMemberStatus.OWNER:
        # تفعيل الفلاتر في هذه القناة
        redus.set(f"{chat_id}_abahy", "enabled")
        await message.reply("تم قفل الاباحي في هذه المجموعة | 🚨")
    else:
        await message.reply("أنت لست المالك أو المسؤول | ♻️")

@app.on_message(filters.command("فتح الاباحي","") & ~filters.private)
async def disable_filter(client, message):
 if not redus.get(f'Disabsabahy:{client.me.id}'):
    chat_id = message.chat.id
    # تحقق من إذن المستخدم (المالك أو المسؤولين)
    chat_member = await client.get_chat_member(chat_id, message.from_user.id)
    if await Dev_us(message.from_user.id, str(client.me.id)) or  redus.sismember(f"{client.me.id}MSAED", message.from_user.id) or chat_member.status ==ChatMemberStatus.OWNER:
        # تعطيل الفلاتر في هذه القناة
        redus.set(f"{chat_id}_abahy", "disabled")
        await message.reply("تم فتح الاباحي في هذه المجموعة | 👑")
    else:
        await message.reply("أنت لست المالك أو المسؤول | 🛑")



from pyrogram import Client, filters
import asyncio
from aiohttp import ClientSession


session = ClientSession() 
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)

@app.on_message(~filters.private, group=5)
async def delete_photo(c, m):
    if not redus.get(f'Disabsabahy:{c.me.id}'):
        try:
            user_id = None
            mention = None
            chat_id = m.chat.id
            filter_status = redus.get(f"{chat_id}_abahy")

            if m.sender_chat:
                user_id = m.sender_chat.id
                mention = f"[{m.sender_chat.title}](t.me/{channel})"
            elif m.from_user:
                user_id = m.from_user.id
                mention = m.from_user.mention

            media = None
            if m.photo:
                media = m.photo.file_id
            elif m.sticker and m.sticker.thumbs:
                media = m.sticker.thumbs[0].file_id
            elif m.video and m.video.thumbs:
                media = m.video.thumbs[0].file_id
            elif m.animation and m.animation.thumbs:
                media = m.animation.thumbs[0].file_id

            if media:
                asyncio.create_task(scan4(c, m, media))
        except Exception as e:
            print(f"Error: {e}")

async def scan4(c, m, media_id):
    try:
        file = await c.download_media(media_id)
        resp = await arq.nsfw_scan(file=file)

        if resp.result.is_nsfw:
            print("xNSFW detected")
            await m.delete()
            await m.reply(
                f"「 {m.from_user.mention} 」\nتم حذف رسالتك لإحتوائها على محتوى إباحي .\n☆"
            )

        await asyncio.to_thread(os.remove, file)
    except Exception as e:
        print(f"Scan Error: {e}")
import asyncio
import time
import sys
import re
import os
import datetime

@Client.on_message(filters.service & filters.group, group=15467)
async def on_servfsices(c, m):
        if m.video_chat_ended:
            duration = m.video_chat_ended.duration
            strtime = time.strftime("%H:%M:%S", time.gmtime(duration)).split(":")
            if duration >= 86400:
                status = "{} يوم و {} ساعة و {} دقيقة".format(
                    datetime.timedelta(seconds=duration).days, strtime[0], strtime[1]
                )
            elif duration >= 3600:
                status = "{} ساعة و {} دقيقة".format(strtime[0], strtime[1])
            elif duration >= 60:
                status = "{} دقيقة و {} ثانية".format(strtime[1], strtime[2])
            else:
                status = "{} ثانية".format(strtime[2])
            return await m.reply("- تم انهاء مكالمة  مده المكالمه : {}".format(status))

        elif m.video_chat_started:
            return await m.reply("↵ تم بدء تشغيل المكالمة")

        elif m.video_chat_members_invited:
            return await m.reply(
                " ⇽ تعال يا حلو للمكالمه :  {}\n ⇽ هالحلو يبيك  : {}".format(
                    m.video_chat_members_invited.users[0].mention, m.from_user.mention
                )
            )