import os
import asyncio
import logging
from decouple import config

from aiogram.exceptions import *
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from aiogram.fsm.context import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Bot.BD.work_db import *
from Bot.handlers.final_form import RegistrationF

token = config("token", default="000")
bot = Bot(token, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

scheduler2 = AsyncIOScheduler(timezone="Europe/Kaliningrad")
scheduler3 = AsyncIOScheduler(timezone="Europe/Moscow")
scheduler4 = AsyncIOScheduler(timezone="Europe/Samara")
scheduler5 = AsyncIOScheduler(timezone="Asia/Yekaterinburg")
scheduler6 = AsyncIOScheduler(timezone="Asia/Omsk")
scheduler7 = AsyncIOScheduler(timezone="Asia/Novosibirsk")


async def main_process(time: str, timezone: int):
    list_user = get_timezone_user(timezone)
    for i in list_user:
        try:
            try:
                day = get_course_day_user(i)
                mess_id = get_data_user(i)["mess_id"]
            except KeyError:
                continue
            mess_data = get_notif_mess(time, day)
            if mess_data[1] == "text":
                await asyncio.sleep(1)
                msg = await bot.send_message(i, mess_data[0])
            elif mess_data[1] == "photo":
                msg = await bot.send_photo(i, FSInputFile(f"{fun.home}/file_mess_notif/{day}/photo.jpg"),
                                     caption=mess_data[0])
            elif mess_data[1] == "doc":
                file = os.listdir(f"{fun.home}/file_mess_notif/{day}")
                for i in file:
                    if i.split(".")[0] == "file":
                        file = i
                        break
                msg = await bot.send_document(i,
                                        FSInputFile(f"{fun.home}/file_mess_notif/{day}/{file}"),
                                        caption=mess_data[0])
            elif mess_data[1] == "video":
                msg = await bot.send_video(i, FSInputFile(f"{fun.home}/file_mess_notif/{day}/video.mp4"),
                                     caption=mess_data[0])
            update_mess_id_user(i, mess_id+str(msg.message_id)+"\n")
        except (TelegramForbiddenError, TelegramBadRequest):
            await bot.send_message(get_id_all_user()[0], f"Пользователю {i}, сообщение не доставлено!")


async def dell_mess_info(user_id: int):
    data_user = get_data_user(user_id)
    for mess_id in data_user["mess_id"].split("\n"):
        try:
            await bot.delete_message(user_id, mess_id)
        except TelegramBadRequest:
            pass


@scheduler2.scheduled_job("cron", hour=0, minute=0)
@scheduler3.scheduled_job("cron", hour=0, minute=0)
@scheduler4.scheduled_job("cron", hour=0, minute=0)
@scheduler5.scheduled_job("cron", hour=0, minute=0)
@scheduler6.scheduled_job("cron", hour=0, minute=0)
@scheduler7.scheduled_job("cron", hour=0, minute=0)
async def main_process_night():
    timezone = dt.datetime.today().time().hour - 5
    user_list = get_timezone_user(timezone)
    for user_id in user_list:
        user_data = get_data_user(user_id)
        if user_data["course_day"] == 31:
            await bot.send_message(user_id, "Подписка закончилась!")
            update_course_day(user_id, 0)
            await dell_mess_info(user_id)
        elif user_data["course_day"] == 0:
            date = dt.datetime.strptime(user_data["data_start"], '%d.%m.%Y').date()
            if dt.date.today() == date:
                update_course_day(user_id, 1)
        elif user_data["course_day"] == 30:
            fsm_storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
            await dp.storage.set_state(fsm_storage_key, RegistrationF.Height)
            await bot.send_message(user_id, "Пожалуйста, введите ваш рост цифрами (в см)")
            update_course_day(user_id, user_data["course_day"] + 1)
        else:
            update_course_day(user_id, user_data["course_day"] + 1)


@scheduler2.scheduled_job("cron", hour=5, minute=0)
@scheduler3.scheduled_job("cron", hour=5, minute=0)
@scheduler4.scheduled_job("cron", hour=5, minute=0)
@scheduler5.scheduled_job("cron", hour=5, minute=0)
@scheduler6.scheduled_job("cron", hour=5, minute=0)
@scheduler7.scheduled_job("cron", hour=5, minute=0)
async def process_morning():
    timezone = dt.datetime.today().time().hour - 5
    await main_process("morning", timezone)


@scheduler2.scheduled_job("cron", hour=13, minute=0)
@scheduler3.scheduled_job("cron", hour=13, minute=0)
@scheduler4.scheduled_job("cron", hour=13, minute=0)
@scheduler5.scheduled_job("cron", hour=13, minute=0)
@scheduler6.scheduled_job("cron", hour=13, minute=0)
@scheduler7.scheduled_job("cron", hour=13, minute=0)
async def process_day():
    timezone = dt.datetime.today().time().hour - 13
    await main_process("day", timezone)


@scheduler2.scheduled_job("cron", hour=21, minute=0)
@scheduler3.scheduled_job("cron", hour=21, minute=0)
@scheduler4.scheduled_job("cron", hour=21, minute=0)
@scheduler5.scheduled_job("cron", hour=21, minute=0)
@scheduler6.scheduled_job("cron", hour=21, minute=0)
@scheduler7.scheduled_job("cron", hour=21, minute=0)
async def process_evening():
    timezone = dt.datetime.today().time().hour - 21
    list_user = get_timezone_user(timezone)
    for i in list_user:
        try:
            await bot.send_message(
                i,
                "Мы желаем Вам доброй ночи. Для лучшего прохождения курса рекомендуем Вам"
                "<a href='https://apps.apple.com/ru/app/%D0%BC%D0%BE-%D0%BC%D0%B5%D0%B4%D0%B8%D1%82%D0%B0%D1%86%D0%B8%D1%8F-%D0%B8-%D1%81%D0%BE%D0%BD/id1460803131'>"
                " скачать приложение </a>")
        except (TelegramForbiddenError, TelegramBadRequest):
            await bot.send_message(get_id_all_user()[0], f"Пользователю {i}, сообщение не доставлено!")





async def start_scheduler():
    scheduler2.start()
    scheduler3.start()
    scheduler4.start()
    scheduler5.start()
    scheduler6.start()
    scheduler7.start()
    logging.warning("Schedulers started")


async def stop_scheduler():
    scheduler2.shutdown()
    scheduler3.shutdown()
    scheduler4.shutdown()
    scheduler5.shutdown()
    scheduler6.shutdown()
    scheduler7.shutdown()
    logging.warning("Schedulers shutdowns")
