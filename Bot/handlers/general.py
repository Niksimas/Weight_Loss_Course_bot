import os
import datetime as dt
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile

import Bot.keyboard as kb
import Bot.function as fun
from .registration import Registration
from Bot.filters.filters import UserIsActive
from Bot.BD.work_db import update_data_start, get_data_user, get_actual_mess, update_mess_id_user

router_general = Router()


@router_general.message(CommandStart())
async def start_main(mess: Message, state: FSMContext, bot: Bot):
    await mess.answer("👋 Привет!)\n"
                      "Я - личный ассистент Марии, твой "
                      "помощник по прохождению обучения \"Голодание\"",
                      reply_markup=kb.main_start(mess.from_user.id))
    if await state.get_state() is not None:
        date = await state.get_data()
        try:
            await bot.edit_message_reply_markup(mess.from_user.id, date["del"])
        except:
            pass


@router_general.callback_query(F.data == "menu", StateFilter(None))
async def main_menu_call(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.edit_text("👋 Привет!)\n"
                                     "Я - личный ассистент Марии, твой "
                                     "помощник по прохождению обучения \"Голодание\"",
                                     reply_markup=kb.main_start(call.from_user.id))
    except:
        await call.message.answer("👋 Привет!)\n"
                                  "Я - личный ассистент Марии, твой "
                                  "помощник по прохождению обучения \"Голодание\"",
                                  reply_markup=kb.main_start(call.from_user.id))


@router_general.callback_query(F.data == "course", UserIsActive())
async def start_is_active(call: CallbackQuery, bot: Bot):
    await call.message.delete()
    data_user = get_data_user(call.from_user.id)
    if data_user["course_day"] == 0:
        if data_user['group_individual'] == "group":
            passing = "в группе"
            edit_date = False
        else:
            passing = "индивидуально"
            edit_date = True
        await call.message.answer(f"ФИО: {data_user['full_name']}\n"
                                  f"Адрес: {data_user['address']}\n"
                                  f"Контакт: {data_user['phone']}\n"
                                  f"Email: {data_user['email']}\n"
                                  f"Прохождение: {passing}\n"
                                  f"Дата старта: {data_user['data_start']}\n",
                                  reply_markup=kb.main_menu(edit_date))
    else:
        data_mess = get_actual_mess(data_user["course_day"], data_user["timezone"])
        if data_mess['type'] == "text":
            msg = await call.message.answer(
                f"Идет {data_mess['num_day']} день курса\n\n" +
                data_mess['text'],
                reply_markup=kb.main_menu()
            )
        elif data_mess['type'] == "photo":
            await bot.send_chat_action(call.from_user.id, "upload_photo")
            msg = await call.message.answer_photo(
                FSInputFile(f"{fun.home}/file_mess_notif/{data_mess['num_day']}/photo.jpg"),
                caption=data_mess['text'],
                reply_markup=kb.main_menu()
            )
        elif data_mess['type'] == "doc":
            await bot.send_chat_action(call.message.from_user.id, "upload_document")
            file = os.listdir(f"{fun.home}/file_mess_notif/{data_mess['num_day']}")
            for i in file:
                if i.split(".")[0] == "file":
                    file = i
                    break
            msg = await call.message.answer_document(
                FSInputFile(f"{fun.home}/file_mess_notif/{data_mess['num_day']}/{file}"),
                caption=data_mess['text'],
                reply_markup=kb.main_menu()
            )
        elif data_mess['type'] == "video":
            await bot.send_chat_action(call.from_user.id, "upload_video")
            msg = await call.message.answer_video(
                FSInputFile(f"{fun.home}/file_mess_notif/{data_mess['num_day']}/video.mp4"),
                caption=data_mess['text'],
                reply_markup=kb.main_menu()
            )
        update_mess_id_user(call.from_user.id, data_user["mess_id"] + str(msg.message_id) + "\n")


@router_general.callback_query(F.data == "edit_data_start", StateFilter(None))
async def edit_data_start(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = get_data_user(call.from_user.id)
    if data["course_day"] == 0:
        await state.set_state(Registration.DataStartR)
        await call.message.answer("Пожалуйста, выберите дату старта курса",
                                  reply_markup=kb.kalendar(
                                      (dt.datetime.now(fun.tz[f'tz{data["timezone"]}'])+dt.timedelta(days=1)).date())
                                  )
    else:
        await call.message.answer("Курс начнется меньше, чем через 5 часов. Дату старта нельзя изменить!")


@router_general.callback_query(Registration.DataStartR, F.data.split("-")[0] == "setd")
async def save_date_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    if call.data.split("-")[1] == "":
        await call.answer("Дата недоступна для выбора!")
        await bot.answer_callback_query(call.id)
        return
    if int(call.data.split("-")[2]) < 10:
        month = f'0{call.data.split("-")[2]}'
    else:
        month = call.data.split("-")[2]
    if int(call.data.split("-")[1]) < 10:
        day = f'0{call.data.split("-")[1]}'
    else:
        day = call.data.split("-")[1]
    update_data_start(call.from_user.id, f'{day}.{month}.{call.data.split("-")[3]}')
    await call.message.edit_text(f"Дата старта изменена на {day}.{month}.{call.data.split('-')[3]}",
                                 reply_markup=kb.custom_button("В меню", "menu"))
    await state.clear()


@router_general.message(StateFilter(None))
async def default_answer(mess: Message):
    await mess.answer("Я не знаю такой команды", reply_markup=kb.custom_button("В меню", "menu"))
