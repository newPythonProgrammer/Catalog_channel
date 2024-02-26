import config
from bot import bot, dp, scheduler, client_pyrogram
from aiogram.utils import executor
from handlers import admin
from handlers import client
from database.admin import Chanel
import time
from telemetr import parse_telemetr

Chanel_db = Chanel()


async def update_stat():
    client_pyrogram.start()
    chanels = await Chanel_db.get_all_chanels()
    for chanel_id, link in chanels:
        subs = await parse_telemetr.get_sub(link)
        views = await parse_telemetr.get_views(link)
        stats = await parse_telemetr.get_photo_stat_and_sub(chanel_id, link)
        if stats == None:
            continue
        await Chanel_db.edit_stat(chanel_id, stats)
        await Chanel_db.edit_views(chanel_id, views)
        await Chanel_db.edit_subs(chanel_id, subs)
        time.sleep(5)


async def main(_):  # Функция выполняется при запуске
    scheduler.add_job(update_stat, "interval", seconds=21600)
    for admin in config.ADMINS:
        try:
            await bot.send_message(admin, 'Бот запущен!')
        except:
            pass


client_pyrogram.start()
scheduler.start()
executor.start_polling(dp, on_startup=main, skip_updates=True)
