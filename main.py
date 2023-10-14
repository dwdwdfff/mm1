from pyrogram import idle

import DRGLIB
from mody.Keyboards import start_key
from mody.Redis import db
from mody.get_info import sudo_info, get_bot
from mody.yad import Bot


async def main():
    await Bot.start()
    print("تم تشغيل البوت بنجاح")
    await idle()
    await Bot.stop()
    print("تم ايقاف البوت بنجاح")


if __name__ == '__main__':
    DRGLIB.client.loop.run_until_complete(main())
