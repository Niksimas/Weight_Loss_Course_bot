import os
import json
import datetime as dt
from aiogram.exceptions import *
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import Message, CallbackQuery, FSInputFile

import Bot.keyboard as kb
import Bot.function as fun
from Bot.BD.work_db import get_id_admin, get_id_all_user, get_notif_mess, update_mess_notif


router_admin = Router()
router_admin.message.filter(F.from_user.id.in_(get_id_admin()))



@router_admin.message(Command("admin"), StateFilter(None))
async def start_is_active(mess: Message):
    await mess.answer("Выберите действие", reply_markup=kb.menu_admin())


@router_admin.callback_query(F.data == "cancel_a")
@router_admin.callback_query(F.data == "admin")
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Выберите действие", reply_markup=kb.menu_admin())


# ################################ Создание сообщения ##################################### #
class SendMessUser(StatesGroup):
    UserId = State()
    MessText = State()
    Check = State()


@router_admin.callback_query(F.data == "send_mess_user")
async def set_mess_for_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(SendMessUser.UserId)
    await call.message.edit_text("Пожалуйста, отправьте id чата пользователя",
                                 reply_markup=kb.custom_button("Отмена", "cancel_a"))


@router_admin.message(SendMessUser.UserId)
async def check_user(mess: Message, state: FSMContext, bot: Bot):
    try:
        await bot.edit_message_reply_markup(mess.from_user.id, mess.message_id - 1, reply_markup=None)
    except:
        pass
    if int(mess.text) in get_id_all_user():
        await state.set_state(SendMessUser.MessText)
        await state.set_data({"user_id": mess.text})
        await mess.answer("Пожалуйста, введите сообщение",
                          reply_markup=kb.custom_button("Отмена", "cancel_a"))
    else:
        await mess.answer("Данного пользователя не существует, введите другой ID",
                          reply_markup=kb.custom_button("Отмена", "cancel_a"))


@router_admin.message(SendMessUser.MessText)
async def send_mess(mess: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    text = mess.text
    try:
        await bot.edit_message_reply_markup(mess.from_user.id, mess.message_id - 1, reply_markup=None)
    except:
        pass
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
    await call.message.edit_text("Пожалуйста, отправьте информацию одним сообщением",
                                 reply_markup=kb.custom_button("Отмена", "cancel_a"))


@router_admin.message(F.text, Notif.Mess)
async def set_text(mess: Message, state: FSMContext, bot: Bot):
    try:
        await bot.edit_message_reply_markup(mess.from_user.id, mess.message_id - 1, reply_markup=None)
    except:
        pass
    await state.set_data({"text": mess.text, "type": "text"})
    await mess.answer(f"Сообщение для рассылки: \n\n{mess.text}", reply_markup=kb.menu_notif("text"))


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
                                 reply_markup=kb.custom_button("Отмена", "cancel_a"))


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
async def set_mess_for_user(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    update_mess_notif(data["time"], data["num_day"], data["text"], data["type"])
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id-1)
    except:
        pass
    await call.message.delete()
    await call.message.answer("Данные успешно изменены!", reply_markup=kb.menu_admin())
    await state.clear()


# ################################ Просмотр фотографий пользователя ##################################### #

class ViewPhoto(StatesGroup):
    SetUserId = State()


@router_admin.callback_query(F.data == "view_photo")
async def choice_day_mess(call: CallbackQuery, state: FSMContext):
    await state.set_state(ViewPhoto.SetUserId)
    await call.message.edit_text("Пожалуйста, введите ID пользователя:",
                                 reply_markup=kb.custom_button("Отмена", "cancel_a"))


@router_admin.message(ViewPhoto.SetUserId)
async def check_user(mess: Message, state: FSMContext, bot: Bot):
    try:
        await bot.edit_message_reply_markup(mess.from_user.id, mess.message_id - 1, reply_markup=None)
    except:
        pass
    if not (int(mess.text) in get_id_all_user()):
        await mess.answer("Данного пользователя нет в базе данных! Введите другой ID",
                          reply_markup=kb.custom_button("Отмена", "cancel_a"))
        return
    if os.path.exists(f"{fun.home}/user_photo/{mess.text}"):
        await state.clear()
        await bot.send_chat_action(mess.from_user.id, "upload_photo")
        media_group = MediaGroupBuilder()
        media_group.add_photo(media=FSInputFile(f"{fun.home}/user_photo/{mess.text}/behind.jpg"))
        media_group.add_photo(media=FSInputFile(f"{fun.home}/user_photo/{mess.text}/front.jpg"))
        media_group.add_photo(media=FSInputFile(f"{fun.home}/user_photo/{mess.text}/side_l.jpg"))
        media_group.add_photo(media=FSInputFile(f"{fun.home}/user_photo/{mess.text}/side_r.jpg"))
        await mess.answer_media_group(media=media_group.build(),
                                      reply_markup=kb.custom_button("В меню", "menu"))
    else:
        await mess.answer("У данного пользователя нет загруженных фотографий, введите другой ID",
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


# ################################ Просмотр фотографий пользователя ##################################### #
class EditGroupInfo(StatesGroup):
    Choice = State()
    Link = State()
    Date = State()


@router_admin.callback_query(F.data == "edit_group_info")
async def choice_day_mess(call: CallbackQuery, state: FSMContext):
    with open(f"{fun.home}/file_mess_notif/group_info.json") as f:
        data = json.load(f)
    await state.set_state(EditGroupInfo.Choice)
    await state.set_data(data)
    await call.message.edit_text(f"Ссылка: {data['link']}\n"
                                 f"Дата: {data['date']}"
                                 "\n\nЧто будем редактировать?:",
                                 reply_markup=kb.edit_info_group())


@router_admin.callback_query(F.data == "edit_link")
async def choice_day_mess(call: CallbackQuery, state: FSMContext):
    await state.set_state(EditGroupInfo.Link)
    await call.message.edit_text("Отправьте новую ссылку:",
                                 reply_markup=kb.custom_button("Отмена", "cancel_a"))


@router_admin.message(EditGroupInfo.Link)
async def send_mess(mess: Message, state: FSMContext):
    text = mess.text
    date = await state.get_data()
    date["link"] = text
    with open(f"{fun.home}/file_mess_notif/group_info.json", "w", encoding="utf-8") as f:
        json.dump(date, f)
    await mess.answer("Новая ссылка установлена!",
                      reply_markup=kb.custom_button("В меню", "menu"))
    await state.clear()


@router_admin.callback_query(F.data == "edit_date")
async def choice_day_mess(call: CallbackQuery, state: FSMContext):
    await state.set_state(EditGroupInfo.Date)
    await call.message.edit_text("Отправьте новую дату старта в формате ДД.ММ.ГГГГ",
                                 reply_markup=kb.custom_button("Отмена", "cancel_a"))


@router_admin.message(EditGroupInfo.Date)
async def send_mess(mess: Message, state: FSMContext):
    try:
        text = mess.text
        data_list = [int(i) for i in text.split(".")]
        data = dt.date(data_list[-1], data_list[1], data_list[0])
        if data < dt.date.today():
            await mess.answer("В веденной дате ошибка. Напишите дату через \".\" в формате ДД.ММ.ГГГГ",
                              reply_markup=kb.custom_button("Отмена", "cancel_a"))
            return
        date = await state.get_data()
        date["date"] = text
        with open(f"{fun.home}/file_mess_notif/group_info.json", "w", encoding="utf-8") as f:
            json.dump(date, f)
        await mess.answer("Новая дата установлена!",
                          reply_markup=kb.custom_button("В меню", "menu"))
        await state.clear()
    except:
        await mess.answer("В веденной дате ошибка. Напишите дату через \".\" в формате ДД.ММ.ГГГГ",
                          reply_markup=kb.custom_button("Отмена", "cancel_a"))


# ################################ Редактирование цен ##################################### #
class EditAmount(StatesGroup):
    Choice = State()
    SetAmount = State()


@router_admin.callback_query(F.data == "edit_amount")
async def choice_day_mess(call: CallbackQuery, state: FSMContext):
    with open(f"{fun.home}/payments/amount.json") as f:
        data = json.load(f)
    await state.set_state(EditAmount.Choice)
    await state.set_data(data)
    await call.message.edit_text(f"Прохождение в группе: {data['group']/100} руб.\n"
                                 f"Прохождение индивидуально: {data['individual']/100} руб.\n"
                                 "Что будем редактировать?",
                                 reply_markup=kb.edit_amount())


@router_admin.callback_query(EditAmount.Choice)
async def choice_day_mess(call: CallbackQuery, state: FSMContext):
    await state.set_state(EditAmount.SetAmount)
    type_amount = call.data.split("_")[1]
    await state.set_data({"type_amount": type_amount})
    if type_amount == "group":
        type_amount_text = "группового"
    else:
        type_amount_text = "индивидуального"
    msg = await call.message.edit_text(f"Введите цену для {type_amount_text} прохождения в рублях: ",
                                 reply_markup=kb.custom_button("Отмена", "cancel_a"))
    await state.update_data({"del": msg.message_id})


@router_admin.message(EditAmount.SetAmount)
async def send_mess(mess: Message, state: FSMContext, bot: Bot):
        data = await state.get_data()
        await bot.edit_message_reply_markup(mess.from_user.id, data['del'])
        try:
            new_amount = int(mess.text) * 100
            with open(f"{fun.home}/payments/amount.json", "r", encoding="utf-8") as f:
                data_file = json.load(f)
            data_file[data['type_amount']] = new_amount
            with open(f"{fun.home}/payments/amount.json", "w", encoding="utf-8") as f:
                json.dump(data_file, f)
            await mess.answer("Новая стоимость установлена!",
                              reply_markup=kb.custom_button("В меню", "menu"))
            await state.clear()
        except ValueError:
            msg = await mess.answer("Введенные данные не являются числом. Попробуйте ещё раз!",
                                    reply_markup=kb.custom_button("Отмена", "cancel_a"))
            await state.update_data({"del": msg.message_id})
