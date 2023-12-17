import os
import logging
import datetime as dt
from aiohttp import web
from decouple import config

from datetime import timedelta

from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from Bot.handlers import *
import Bot.payments as pay
from function import admins, home
from Bot.reminder.general import start_scheduler, stop_scheduler

token = config("token", default="")
REDIS_DSN = "redis://127.0.0.1:6379"
storage = RedisStorage.from_url(REDIS_DSN, key_builder=DefaultKeyBuilder(with_bot_id=True),
                                data_ttl=timedelta(days=1.0), state_ttl=timedelta(days=1.0))
bot = Bot(token, parse_mode="HTML")
dp = Dispatcher(storage=storage)
statistics_general = [0, 0]


MAIN_BOT_PATH = f"/LITE"
BASE_URL = f"https://<ip>{MAIN_BOT_PATH}"
WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 8000

dp.include_router(router_general)
dp.include_router(pay.general.router)
dp.include_router(router_reg)
dp.include_router(router_admin)
dp.include_router(router_ff)

if not os.path.exists(f"{home}/user_photo"):
    os.makedirs(f"{home}/user_photo")
if not os.path.exists(f"{home}/file_mess_notif"):
    os.makedirs(f"{home}/file_mess_notif")
if not os.path.exists(f"{home}/logging"):
    os.makedirs(f"{home}/logging")

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


# ______________________________СТАРТОВЫЕ_КОМАНДЫ______________________________________
@dp.message(Command(commands="stops159"), F.from_user.id.in_(admins))
async def stop():
    await on_shutdown()
    await bot.close()
    exit(1)


async def on_startup():
    logger.error("Снятие и установка webhook")
    await start_scheduler()
    await bot.delete_webhook()
    await bot.set_webhook(
            url=BASE_URL,
            certificate=types.FSInputFile("/etc/ssl/certs/Bot.crt"),  # Путь до сертификата
            drop_pending_updates=True)

    await bot.send_message(1235360344, "Бот запущен")
    return


async def on_shutdown():
    logging.warning('Выключение бота')
    list_log = os.listdir(f"{home}/logging")
    list_log.sort()
    log = types.FSInputFile(f"{home}/logging/{list_log[-1]}")
    await bot.send_document(1235360344, log)
    await bot.delete_webhook()
    await bot.send_message(1235360344, "Бот выключен")
    await stop_scheduler()
    return


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)


def main():
    logger.error("Запуск веб-сервера")
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=MAIN_BOT_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    return


if __name__ == "__main__":
    main()
