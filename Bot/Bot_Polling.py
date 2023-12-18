import os
import asyncio
import logging
import datetime as dt
from decouple import config

from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

import Bot.payments as pay
import Bot.handlers as hand
from function import admins, home
from Bot.reminder.general import start_scheduler

logging.basicConfig(level=logging.INFO)

token = config("token", default="000")
bot = Bot(token, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(hand.router_general)
dp.include_router(pay.general.router)
dp.include_router(hand.router_reg)
dp.include_router(hand.router_admin)
dp.include_router(hand.router_ff)


logger = logging.getLogger()
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(f"{home}/logging/bot{dt.date.today()}", "a+", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)

logging.debug("Сообщения уровня DEBUG, необходимы при отладке ")
logging.info("Сообщения уровня INFO, полезная информация при работе программы")
logging.warning("Сообщения уровня WARNING, не критичны, но проблема может повторится")
logging.error("Сообщения уровня ERROR, программа не смогла выполнить какую-либо функцию")
logging.critical("Сообщения уровня CRITICAL, серьезная ошибка нарушающая дальнейшую работу")


if not os.path.exists(f"{home}/user_photo"):
    os.makedirs(f"{home}/user_photo")
if not os.path.exists(f"{home}/file_mess_notif"):
    os.makedirs(f"{home}/file_mess_notif")
    for i in range(1, 32):
        os.makedirs(f"{home}/file_mess_notif/{i}")
if not os.path.exists(f"{home}/logging"):
    os.makedirs(f"{home}/logging")


@dp.message(Command(commands=["stops159"]))
async def stop(message: types.Message):
    await message.answer("Все сценарии работы выключены!")
    await bot.close()
    exit(1)


async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)

    await bot.send_message(admins[0], "Бот запущен")
    return


async def on_shutdown():
    await bot.send_message(admins[0], "Бот выключен")
    await dp.storage.close()
    await bot.close()
    return


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)


async def main():
    await start_scheduler()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
