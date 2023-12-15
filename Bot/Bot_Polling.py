import os
import asyncio
import logging
from decouple import config
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

import Bot.payments as pay
from Bot.reminder.general import scheduler
import Bot.handlers as hand
from function import admins, home

logging.basicConfig(level=logging.INFO)

token = config("token", default="000")
bot = Bot(token, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(hand.router_general)
dp.include_router(pay.general.router)
dp.include_router(hand.router_reg)
dp.include_router(hand.router_admin)

if not os.path.exists(f"{home}/user_photo"):
    os.makedirs(f"{home}/user_photo")
if not os.path.exists(f"{home}/file_mess_notif"):
    os.makedirs(f"{home}/file_mess_notif")


# @dp.message()
# async def start_is_active(mess: Message):
#     print(mess)
#     print()


@dp.message(Command(commands=["stops159"]))
async def stop(message: types.Message):
    await message.answer("Все сценарии работы выключены!")
    await bot.close()
    exit(1)


async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    scheduler.start()
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
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
