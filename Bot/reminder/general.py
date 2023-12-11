from aiogram import Bot
import datetime as dt

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Bot.google_doc.googleSheets import get_active_user

scheduler = AsyncIOScheduler(timezone="Asia/Novosibirsk")


# №	id_photo	описание	Ответственный	id_responsible	Дедлайн	Чаты_публикации
async def mail_notif(bot: Bot, id_record: int):
    data = get_active_user()
    try:
        if data[1] != "":
            await bot.send_photo(data[4], data[1])
        await bot.send_message(data[4], f"Описание:\n{data[2]}\n"
                                        f"Ответственный: {data[3]}\n"
                                        f"Дедлайн: {data[5]}\n")
    except:
        await bot.send_message(111, f"Сообщение не доставлено ответственному лицу!"
                                                   f"Описание:\n{data[2]}\n"
                                                   f"Ответственный: {data[3]}\n"
                                                   f"Дедлайн: {data[5]}\n")


def add_notif(id_record: int, bot: Bot, data: str):
    data_list = data.split(".")
    data_start = dt.datetime(int(data_list[2]), int(data_list[1]), int(data_list[0]), 8, 0) - dt.timedelta(days=1)
    print(data_start)
    if data_start > dt.datetime.today():
        scheduler.add_job(mail_notif, "date",
                          run_date=data_start,
                          kwargs={"id_record": id_record, "bot": bot})
