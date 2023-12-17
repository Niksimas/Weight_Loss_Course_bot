import os

from aiogram.exceptions import *
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter

import Bot.keyboard as kb
import Bot.function as fun
from Bot.BD.work_db import get_id_admin, get_id_all_user, get_notif_mess, update_mess_notif


router_admin = Router()
router_admin.message.filter(F.from_user.id.in_(get_id_admin()))


class SendMessUser(StatesGroup):
    UserId = State()
    MessText = State()


@router_admin.message(Command("admin"), StateFilter(None))
async def start_is_active(mess: Message):
    await mess.answer("Выберите действие", reply_markup=kb.menu_admin())


@router_admin.callback_query(F.data == "cancel_a")
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Выберите действие", reply_markup=kb.menu_admin())


# ################################ Создание сообщения ##################################### #
@router_admin.callback_query(F.data == "send_mess_user")
async def set_mess_for_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(SendMessUser.UserId)
    await call.message.edit_text("Пожалуйста, отправьте id чата пользователя", reply_markup=None)


@router_admin.message(SendMessUser.UserId)
async def check_user(mess: Message, state: FSMContext):
    if mess.text in get_id_all_user():
        await state.set_state(SendMessUser.MessText)
        await state.set_data({"user_id": mess.text})
        await mess.answer("Пожалуйста, введите сообщение")
    else:
        await mess.answer("Данного пользователя не существует, введите другой ID",
                          reply_markup=kb.custom_button("Отмена", "cancel_a"))


@router_admin.message(SendMessUser.MessText)
async def send_mess(mess: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    text = mess.text
    try:
        await bot.send_message(data["user_id"], text)
        await mess.answer("Сообщение доставлено!")
    except (TelegramForbiddenError, TelegramBadRequest):
        await mess.answer("Сообщение не доставлено!")
    await state.clear()


# ################################ Создание рассылки ##################################### #
class Notif(StatesGroup):
    Mess = State()


@router_admin.callback_query(F.data == "start_notif")
@router_admin.callback_query(F.data == "restart_notif")
async def set_mess_notif(call: CallbackQuery, state: FSMContext):
    await state.set_state(Notif.Mess)
    await call.message.edit_text("Пожалуйста, отправьте информацию одним сообщением", reply_markup=None)


@router_admin.message(F.text, Notif.Mess)
async def set_text(mess: Message, state: FSMContext):
    await state.set_data({"text": mess.text, "type": "text"})
    await mess.answer(f"Сообщение для рассылке: \n\n{mess.text}", reply_markup=kb.menu_notif("text"))


@router_admin.message(F.photo, Notif.Mess)
async def set_photo(mess: Message, state: FSMContext):
    await state.update_data({"photo": mess.photo[-1].file_id, "text": mess.caption, "type": "photo"})
    await mess.answer("Сообщение для рассылки: ")
    await mess.answer_photo(mess.photo[-1].file_id, mess.caption, reply_markup=kb.menu_notif("photo"))


@router_admin.message(F.document, Notif.Mess)
async def set_doc(mess: Message, state: FSMContext):
    await state.update_data({"doc": mess.document[-1].file_id, "text": mess.caption, "type": "doc"})
    await mess.answer("Сообщение для рассылки: ")
    await mess.answer_document(mess.document[-1].file_id, mess.caption, reply_markup=kb.menu_notif("doc"))


@router_admin.message(F.video, Notif.Mess)
async def set_video(mess: Message, state: FSMContext):
    await state.update_data({"video": mess.video[-1].file_id, "text": mess.caption, "type": "video"})
    await mess.answer("Сообщение для рассылки: ")
    await mess.answer_video(mess.document[-1].file_id, mess.caption, reply_markup=kb.menu_notif("video"))


@router_admin.callback_query(Notif.Mess, F.data == "yes_text")
async def processed_notif_text(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    data = await state.get_data()
    user_id = get_id_all_user()
    text = data["text"]
    for i in user_id:
        try:
            await bot.send_message(i, text)
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
    await state.clear()
    await call.message.answer("Рассылка успешно отправлена", reply_markup=kb.menu_admin())


@router_admin.callback_query(Notif.Mess, F.data == "yes_photo")
async def processed_notif_photo(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    data = await state.get_data()
    user_id = get_id_all_user()
    text = data["text"]
    photo = data["photo"]
    for i in user_id:
        try:
            await bot.send_photo(i, photo, caption=text)
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
    await state.clear()
    await call.message.answer("Рассылка успешно отправлена", reply_markup=kb.menu_admin())


@router_admin.callback_query(Notif.Mess, F.data == "yes_doc")
async def processed_notif_doc(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    data = await state.get_data()
    user_id = get_id_all_user()
    doc = data["doc"]
    text = data["text"]
    for i in user_id:
        try:
            await bot.send_document(i, doc, caption=text)
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
    await state.clear()
    await call.message.answer("Рассылка успешно отправлена", reply_markup=kb.menu_admin())


@router_admin.callback_query(Notif.Mess, F.data == "yes_video")
async def processed_notif_video(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    data = await state.get_data()
    user_id = get_id_all_user()
    video = data["video"]
    text = data["text"]
    for i in user_id:
        try:
            await bot.send_video(i, video, caption=text)
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
    await state.clear()
    await call.message.answer("Рассылка успешно отправлена", reply_markup=kb.menu_admin())


# ################################ Редактирование сообщений рассылки ##################################### #
class EditMessDay(StatesGroup):
    Day = State()
    Time = State()
    Check = State()
    SetMess = State()
    Verify = State()


@router_admin.callback_query(EditMessDay.Time, F.data == "back_day")
@router_admin.callback_query(F.data == "edit_day_mess")
async def choice_day_mess(call: CallbackQuery, state: FSMContext):
    await state.set_state(EditMessDay.Day)
    await call.message.edit_text("Пожалуйста, выберите день курса для изменения:",
                                 reply_markup=kb.course_days())


@router_admin.callback_query(EditMessDay.Check, F.data.split("_")[0] == "back")
@router_admin.callback_query(EditMessDay.Day)
async def choice_time_day(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(EditMessDay.Time)
    num_day = call.data.split("_")[-1]
    await call.message.delete()
    await call.message.answer(f"Пожалуйста, выберите сообщение {num_day} дня: ",
                                 reply_markup=kb.time_mess(num_day))


@router_admin.callback_query(EditMessDay.Time)
async def view_mess_time_day(call: CallbackQuery, state: FSMContext, bot: Bot):
    """показывает сообщение выбранного дня"""
    mess_data = get_notif_mess(call.data.split("_")[-1], int(call.data.split("_")[0]))
    await state.set_state(EditMessDay.Check)
    await call.message.delete()
    if mess_data[1] == "text":
        await call.message.answer(
            mess_data[0],
            reply_markup=kb.edit_mess(call.data.split("_")[-1], int(call.data.split("_")[0]))
        )
    elif mess_data[1] == "photo":
        await bot.send_chat_action(call.from_user.id, "upload_photo")
        await call.message.answer_photo(
            FSInputFile(f"{fun.home}/file_mess_notif/{call.data.split('_')[0]}/photo.jpg"),
            caption=mess_data[0],
            reply_markup=kb.edit_mess(call.data.split("_")[-1], int(call.data.split("_")[0]))
        )
    elif mess_data[1] == "doc":
        await bot.send_chat_action(call.from_user.id, "upload_document")
        file = os.listdir(f"{fun.home}/file_mess_notif/{call.data.split('_')[0]}")
        for i in file:
            if i.split(".")[0] == "file":
                file = i
                break
        await call.message.answer_document(
            FSInputFile(f"{fun.home}/file_mess_notif/{call.data.split('_')[0]}/{file}"),
            caption=mess_data[0],
            reply_markup=kb.edit_mess(call.data.split("_")[-1], int(call.data.split("_")[0]))
        )
    elif mess_data[1] == "video":
        await bot.send_chat_action(call.from_user.id, "upload_video")
        await call.message.answer_video(
            FSInputFile(f"{fun.home}/file_mess_notif/{call.data.split('_')[0]}/video.mp4"),
            caption=mess_data[0],
            reply_markup=kb.edit_mess(call.data.split("_")[-1], int(call.data.split("_")[0]))
        )


@router_admin.callback_query(EditMessDay.Verify, F.data == "restart_notif")
@router_admin.callback_query(EditMessDay.Check, F.data.split("_")[0] == "edit")
async def edit_mess_notif(call: CallbackQuery, state: FSMContext):
    await state.set_state(EditMessDay.SetMess)
    if call.data.split("_")[0] == "edit":
        await state.set_data({"num_day": int(call.data.split("_")[-1]), "time": call.data.split("_")[1]})
    await call.message.edit_text("Пожалуйста, отправьте информацию одним сообщением",
                                 reply_markup=None)


@router_admin.message(F.text, EditMessDay.SetMess)
async def set_text_notif(mess: Message, state: FSMContext):
    await state.set_state(EditMessDay.Verify)
    await state.update_data({"text": mess.text, "type": "text"})
    await mess.answer("Новое сообщения для рассылки: ")
    await mess.answer(f"{mess.text}", reply_markup=kb.menu_notif("text"))


@router_admin.message(F.photo, EditMessDay.SetMess)
async def set_photo_notif(mess: Message, state: FSMContext, bot: Bot):
    await state.set_state(EditMessDay.Verify)
    data = await state.get_data()
    await bot.download(mess.photo[-1].file_id,
                       destination=f"{fun.home}/file_mess_notif/{data['num_day']}/photo.jpg")
    await state.update_data({"text": mess.caption, "type": "photo"})
    await mess.answer("Новое сообщения для рассылки: ")
    await mess.answer_photo(mess.photo[-1].file_id, mess.caption, reply_markup=kb.menu_notif("photo"))


@router_admin.message(F.document, EditMessDay.SetMess)
async def set_doc_notif(mess: Message, state: FSMContext, bot: Bot):
    await state.set_state(EditMessDay.Verify)
    data = await state.get_data()
    await bot.download(mess.document.file_id,
                       destination=f"{fun.home}/file_mess_notif/{data['num_day']}/"
                                   f"file.{mess.document.file_name.split('.')[-1]}")
    await state.update_data({"text": mess.caption, "type": "doc"})
    await mess.answer("Новое сообщения для рассылки: ")
    await mess.answer_document(mess.document.file_id, caption=mess.caption, reply_markup=kb.menu_notif("doc"))


@router_admin.message(F.video, EditMessDay.SetMess)
async def set_video_notif(mess: Message, state: FSMContext, bot: Bot):
    await state.set_state(EditMessDay.Verify)
    data = await state.get_data()
    await bot.download(mess.video.file_id,
                       destination=f"{fun.home}/file_mess_notif/{data['num_day']}/video.mp4")
    await state.update_data({"text": mess.caption, "type": "video"})
    await mess.answer("Новое сообщения для рассылки: ")
    await mess.answer_video(mess.video.file_id, caption=mess.caption, reply_markup=kb.menu_notif("video"))


@router_admin.callback_query(EditMessDay.Verify, F.data.split("_")[0] == "yes")
async def set_mess_for_user(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    update_mess_notif(data["time"], data["num_day"], data["text"], data["type"])
    await call.message.delete()
    await call.message.answer("Данные успешно изменены!", reply_markup=kb.menu_admin())
    await state.clear()


@router_admin.message(Command("test"), StateFilter(None))
async def start_is_active(mess: Message, bot):
    await mess.answer("test", reply_markup=kb.custom_button("test", "test"))

