import os
import datetime as dt
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, StateFilter, Command

import Bot.keyboard as kb
import Bot.function as fun
from .registration import Registration
from Bot.filters.filters import UserIsActive
from Bot.BD.work_db import update_data_start, get_data_user, get_actual_mess, update_mess_id_user

router_general = Router()


@router_general.message(CommandStart(), UserIsActive())
async def start_is_active(mess: Message, bot: Bot):
    data_user = get_data_user(mess.chat.id)

    if data_user["course_day"] == 0:
        await mess.answer(f"ФИО: {data_user['full_name']}\n"
                          f"Адрес: {data_user['address']}\n"
                          f"Контакт: {data_user['phone_email']}\n"
                          f"Дата старта: {data_user['data_start']}\n",
                          reply_markup=kb.main_menu(True))
    else:
        data_mess = get_actual_mess(data_user["course_day"])
        if data_mess['type'] == "text":
            msg = await mess.answer(
                f"Идет {data_mess['num_day']} день курса\n\n" +
                data_mess['text'],
                reply_markup=kb.main_menu()
            )
        elif data_mess['type'] == "photo":
            await bot.send_chat_action(mess.from_user.id, "upload_photo")
            msg = await mess.answer_photo(
                FSInputFile(f"{fun.home}/file_mess_notif/{mess.data.split('_')[0]}/photo.jpg"),
                caption=data_mess['text'],
                reply_markup=kb.main_menu()
            )
        elif data_mess['type'] == "doc":
            await bot.send_chat_action(mess.from_user.id, "upload_document")
            file = os.listdir(f"{fun.home}/file_mess_notif/{data_mess['num_day']}")
            for i in file:
                if i.split(".")[0] == "file":
                    file = i
                    break
            msg = await mess.answer_document(
                FSInputFile(f"{fun.home}/file_mess_notif/{data_mess['num_day']}/{file}"),
                caption=data_mess['text'],
                reply_markup=kb.main_menu()
            )
        elif data_mess['type'] == "video":
            await bot.send_chat_action(mess.from_user.id, "upload_video")
            msg = await mess.answer_video(
                FSInputFile(f"{fun.home}/file_mess_notif/{data_mess['num_day']}/video.mp4"),
                caption=data_mess['text'],
                reply_markup=kb.main_menu()
            )
        update_mess_id_user(mess.from_user.id, data_user["mess_id"] + str(msg.message_id) + "\n")


@router_general.callback_query(F.data == "menu", StateFilter(None))
async def main_menu(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await start_is_active(call.message, bot)


@router_general.callback_query(F.data == "edit_data_start", StateFilter(None))
@router_general.callback_query(F.data == "test")
async def edit_data_start(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = get_data_user(call.from_user.id)
    data_user = [int(i) for i in data["data_start"].split(".")]
    if dt.datetime.today()+dt.timedelta(hours=data['timezone']) < dt.datetime(data_user[2], data_user[1], data_user[0]):
        await state.set_state(Registration.DataStartR)
        await call.message.answer("Пожалуйста, выберите дату старта курса", reply_markup=kb.kalendar())
    else:
        await call.message.answer("Курс начнется меньше, чем через 5 часов. Дату старта нельзя изменить!")


@router_general.callback_query(Registration.DataStart, F.data.split("-")[0] == "next")
async def view_next_month(call: CallbackQuery):
    in_data = dt.date(int(call.data.split("-")[1]), int(call.data.split("-")[2]), int(call.data.split("-")[3]))
    if dt.date.today() + dt.timedelta(days=14) < in_data:
        await call.message.edit_reply_markup(
            reply_markup=kb.kalendar((dt.date(in_data.year, in_data.month, in_data.day)+dt.timedelta(days=31))))
    else:
        await call.answer("Доступных дат больше нет")


@router_general.callback_query(Registration.DataStart, F.data.split("-")[0] == "back")
async def view_back_month(call: CallbackQuery):
    in_data = dt.date(int(call.data.split("-")[1]), int(call.data.split("-")[2]), int(call.data.split("-")[3]))
    if dt.date.today() + dt.timedelta(days=14) < in_data:
        await call.message.edit_reply_markup(
            reply_markup=kb.kalendar((dt.date(in_data.year, in_data.month, in_data.day)-dt.timedelta(days=31))))
    else:
        await call.answer("Доступных дат больше нет")


@router_general.callback_query(Registration.DataStart, F.data.split == "month")
async def answer_month(call: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(call.id)
    await call.answer("Выберите дату в представленном месяце")


@router_general.callback_query(Registration.DataStartR, F.data.split("-")[0] == "setd")
async def save_date_start(call: CallbackQuery, state: FSMContext):
    update_data_start(call.from_user.id, ".".join(call.data.split("-")[1:]))
    await call.message.edit_text(f"Дата старта изменена на {'.'.join(call.data.split('-')[1:])}",
                                 reply_markup=None)
    await state.clear()

