import os
import re
from asyncio import sleep, create_task, get_event_loop
from sys import argv
from mody.Keyboards import subs
from pyrogram import Client, filters, idle
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait, YouBlockedUser
from telebot.async_telebot import AsyncTeleBot
from datetime import date
from mody.Redis import db
from info import token, sudo_id, user_bot
import logging

logging.getLogger("pyrogram").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
bot = AsyncTeleBot(token)

userbot = Client(
    f'users/user:{argv[1][:15]}',
    7720093,
    '51560d96d683932d1e68851e7f0fdea2',
    session_string=argv[1]
)

   

async def getInfo():
    return await bot.get_me(), \
        await bot.get_chat(sudo_id)

async def lf(_, __, msg):  # فلتر الرابط
    if msg.text:
        if '?' in msg.text:
            return False
    return True


bot.me, sudo_info = get_event_loop().run_until_complete(getInfo())

userbot.send_log = lambda text: \
    bot.send_message(sudo_info.id, f"- You have a new message ✉️\n\n𖡋 𝐍𝐀𝐌𝐄 ⌯ {userbot.me.first_name}\n𖡋 𝐈𝐃 ⌯ {userbot.me.id}\n𖡋 𝐔𝐒𝐄 ⌯ @{userbot.me.username}\n𖡋 𝐃𝐀𝐓𝐄 ⌯ {date.today()}\n\n{text}", reply_markup=subs)
async def delete_userbot():
    while not await sleep(5):
        if db.sismember(f'{bot.me.id}:{sudo_info.id}:delete_userbot', userbot.me.id):
            db.srem(f'{bot.me.id}:{sudo_info.id}:delete_userbot', userbot.me.id)
            db.srem(f'{bot.me.id}:{sudo_info.id}:sessions', userbot.session_string)
            await userbot.stop()
            try:
                os.remove(userbot.name)
            except:
                pass
            await userbot.send_log('تم حذف الحساب')
            exit()


async def auto_start_in_bot():
    while not await sleep(220):
        if not db.get(f'{bot.me.id}:{userbot.me.id}:stop'):
            try:
                await userbot.send_message(user_bot, '/start')
            except YouBlockedUser:
                await userbot.unblock_user(user_bot)
                await sleep(0.5)
                await userbot.send_message(user_bot, '/start')
            except Exception as e:
                print(e)
                pass



async def leave():
    while not await sleep(84000):
      async for dialog in userbot.get_dialogs():
        if dialog.chat.type != ChatType.PRIVATE:
            try:
                await userbot.leave_chat(dialog.chat.id, delete=True)
            except:
                pass
      

async def join_chat(c, link, bot_id):
    try:
        if '+' in link or 'joinchat' in link:
            await c.join_chat(link)
        else:
            await c.join_chat(link.replace('https://t.me/', ''))
    except FloodWait as e:
        await c.send_log(f'⌯ انحظر لمدة {e.value} ثانيه')
        if e.value >= 99999:
            db.set(f'{bot.me.id}:{c.me.id}:get_all_points', '3yad')
            await c.send_message(bot_id, '/start')
        db.setex(f'{bot.me.id}:{userbot.me.id}:stop', e.value + 10, '3yad')
        await sleep(e.value + 10)
        await c.send_log('⌯ الحظر اتفك')
    except Exception as e:
        print(e)


@userbot.on_message(filters.bot & filters.regex('مرحبا بك في بوت') & filters.private)
async def keko_tmwel_bots2(c, msg):
    second_line_text = msg.text.split('\n')[1] 
    number_in_second_line = re.search(r'\d+', second_line_text)
    if number_in_second_line:
        number = int(number_in_second_line.group())
        await sleep(1)
        if number >= 530:
            try:
                await c.request_callback_answer(
                    chat_id=msg.chat.id,
                    message_id=msg.id,
                    callback_data='trans'
                )
            except:
                pass

            await sleep (1)
            try:

                await c.send_message(msg.chat.id, "5893626683")
            except:
                pass
            await sleep(1)

            try:
                await c.send_message(msg.chat.id, str(number -30))
            except:
                pass
        else:

            try:
               await c.request_callback_answer(
            chat_id=msg.chat.id,
            message_id=msg.id,
            callback_data='collect'
        )
            except:
                 pass

    await sleep(3)

    try:
        await c.request_callback_answer(
            chat_id=msg.chat.id,
            message_id=msg.id,
            callback_data='get_join'
        )
    except:
        pass
@userbot.on_edited_message(filters.bot & filters.regex('اشترك فالقناة ') & filters.private)
async def join_channel(c, msg):
    channel_username = re.search(r'@(\w+)', msg.text)
    if channel_username:
        channel_username = channel_username.group(1)
        try:
            await c.join_chat(channel_username)
            joined = True
        except Exception as e:
            joined = False

        callback_data = 'i_am_join' if joined else 'skip'

        await sleep(4)
        try:
            await c.request_callback_answer(
                chat_id=msg.chat.id,
                message_id=msg.id,
                callback_data=callback_data
            )
        except:
            pass
@userbot.on_message(filters.bot & filters.regex('@') & filters.create(lf) & filters.private)
async def ctcbot(c, msg):  # الاشتراك الاجباري
    if not db.get(f'{bot.me.id}:{userbot.me.id}:stop'):
        ay = ''
        for lin in msg.text.split('\n'):
            if '@' in lin:
                ay = lin
                break
        if not ay:
            return
        link = '@' + ay.split('@')[1]
        if ' ' in link:
            link = link.split(' ')[0]
        await join_chat(c, link, msg.chat.id)
        await sleep(1)
        await c.send_message(msg.chat.id, '/start')
async def main():
    await userbot.start()
    create_task(auto_start_in_bot())
    create_task(leave())
    create_task(delete_userbot())
    if not db.get(f'{bot.me.id}:{userbot.me.id}:stop'):
        try:
            await userbot.send_message(user_bot, '/start')
        except YouBlockedUser:
            await userbot.unblock_user(user_bot)
            await sleep(0.5)
            await userbot.send_message(user_bot, '/start')
    try:
        await userbot.send_log('تم تشغيل الحساب')
    except Exception as e:
        print(e)
    await idle()
    await userbot.stop()


get_event_loop().run_until_complete(main())
