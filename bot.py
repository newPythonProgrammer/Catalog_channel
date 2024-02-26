from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import config
import pyrogram

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()
client_pyrogram = pyrogram.Client("my_account", config.API_ID_ACC, config.API_HASH_ACC)