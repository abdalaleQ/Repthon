import random
import re
import time
import os
from datetime import datetime
from platform import python_version

import requests
from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from repthon import StartTime, zq_lo, repversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import repalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "العروض"
ALIVE = gvarstatus("R_ALIVE") or "فحص"

# @E_7_V 
file_path = "installation_date.txt"
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    with open(file_path, "r") as file:
        installation_time = file.read().strip()
else:
    installation_time = datetime.now().strftime("%Y-%m-%d")
    with open(file_path, "w") as file:
        file.write(installation_time)

@zq_lo.rep_cmd(pattern=f"{ALIVE}$")
async def alive(event):
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    repevent = await edit_or_reply(event, "**𓅓┊جـاري .. فحـص البـوت الخـاص بك**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    R_EMOJI = gvarstatus("ALIVE_EMOJI") or "𓃰┊"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "** بـوت ريبـــثون 𝐑𝐞𝐩𝐭𝐡𝐨𝐧 يعمـل .. بنجـاح ☑️ 𓆩 **"
    REP_IMG = gvarstatus("ALIVE_PIC") or "https://graph.org/file/f701e179b634b5a873e8c.mp4"
    rep_caption = gvarstatus("ALIVE_TEMPLATE") or rep_temp
    caption = rep_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        R_EMOJI=R_EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        repver=repversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
        repthon_Tare5=installation_time
    )
    if REP_IMG:
        REP = [x for x in REP_IMG.split()]
        PIC = random.choice(REP)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await repevent.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                repevent,
                f"**⌔∮ عـذراً عليـك الـرد ع صـوره او ميـديـا  ⪼  `.اضف صورة الفحص` <بالرد ع الصـوره او الميـديـا> ",
            )
    else:
        await edit_or_reply(
            repevent,
            caption,
        )


rep_temp = """{ALIVE_TEXT}

**{R_EMOJI} قاعدۿ البيانات :** تعمل بنـجاح
**{R_EMOJI} إصـدار التـيليثون :** `{telever}`
**{R_EMOJI} إصـدار ريبـــثون :** `{repver}`
**{R_EMOJI} إصـدار البـايثون :** `{pyver}`
**{R_EMOJI} الوقـت :** `{uptime}`
**{R_EMOJI} المسـتخدم:** {mention}
**{R_EMOJI} التـاريـخ:** {repthon_Tare5}
**{R_EMOJI} قنـاة السـورس :** [اضغـط هنـا](https://t.me/rr_r_v)"""


@zq_lo.rep_cmd(
    pattern="الفحص$",
    command=("الفحص", plugin_category),
    info={
        "header": "- لـ التحـقق من ان البـوت يعمـل بنجـاح .. بخـاصيـة الانـلايـن ✓",
        "الاسـتخـدام": [
            "{tr}الفحص",
        ],
    },
)
async def amireallyialive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    R_EMOJI = gvarstatus("ALIVE_EMOJI") or "𓅓┊"
    rep_caption = "** بـوت ريبـــثون 𝐑𝐞𝐩𝐭𝐡𝐨𝐧 يعمـل .. بنجـاح ☑️ 𓆩 **\n"
    rep_caption += f"**{R_EMOJI} إصـدار التـيليثون :** `{version.__version__}\n`"
    rep_caption += f"**{R_EMOJI} إصـدار ريبـــثون :** `{repversion}`\n"
    rep_caption += f"**{R_EMOJI} إصـدار البـايثون :** `{python_version()}\n`"
    rep_caption += f"**{R_EMOJI} المسـتخدم :** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, rep_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@zq_lo.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await repalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
