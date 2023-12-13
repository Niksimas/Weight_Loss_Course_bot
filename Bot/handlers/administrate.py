from aiogram.exceptions import *
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart, StateFilter

import Bot.keyboard as kb
from Bot.google_doc.googleSheets import get_active_user, get_admin, get_all_user

router = Router()
router.message.filter(F.from_user.id.in_([int(i) for i in get_admin()]))


class SendMessUser(StatesGroup):
    UserId = State()
    MessText = State()


class Notif(StatesGroup):
    Mess = State()


@router.message(Command("admin"), StateFilter(None))
async def start_is_active(mess: Message):
    await mess.answer("Выберите действие", reply_markup=kb.menu_admin())


@router.callback_query(F.data == "cancel_a")
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Выберите действие", reply_markup=kb.menu_admin())


# ################################ Создание сообщения ##################################### #
@router.callback_query(F.data == "send_mess_user")
async def set_mess_for_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(SendMessUser.UserId)
    await call.message.edit_text("Пожалуйста, отправьте id чата пользователя", reply_markup=None)


@router.message(SendMessUser.UserId)
async def check_user(mess: Message, state: FSMContext):
    if mess.text in get_active_user():
        await state.set_state(SendMessUser.MessText)
        await state.set_data({"user_id": mess.text})
        await mess.answer("Пожалуйста, введите сообщение")
    else:
        await mess.answer("Данного пользователя не существует, введите другой ID",
                          reply_markup=kb.custom_button("Отмена", "cancel_a"))


@router.message(SendMessUser.MessText)
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
@router.callback_query(F.data == "start_notif")
@router.callback_query(F.data == "restart_notif")
async def set_mess_notif(call: CallbackQuery, state: FSMContext):
    await state.set_state(Notif.Mess)
    await call.message.edit_text("Пожалуйста, отправьте информацию одним сообщением", reply_markup=None)


@router.message(F.text, Notif.Mess)
async def set_text(mess: Message, state: FSMContext):
    await state.set_data({"text": mess.text, "type": "text"})
    await mess.answer(f"Сообщение для рассылке: \n\n{mess.text}", reply_markup=kb.menu_notif("text"))


@router.message(F.photo, Notif.Mess)
async def set_photo(mess: Message, state: FSMContext):
    await state.update_data({"photo": mess.photo[-1].file_id, "text": mess.caption, "type": "photo"})
    await mess.answer("Сообщение для рассылки: ")
    await mess.answer_photo(mess.photo[-1].file_id, mess.caption, reply_markup=kb.menu_notif("photo"))


@router.message(F.document, Notif.Mess)
async def set_doc(mess: Message, state: FSMContext):
    await state.update_data({"doc": mess.document[-1].file_id, "text": mess.caption, "type": "doc"})
    await mess.answer("Сообщение для рассылки: ")
    await mess.answer_document(mess.document[-1].file_id, mess.caption, reply_markup=kb.menu_notif("doc"))


@router.message(F.video, Notif.Mess)
async def set_video(mess: Message, state: FSMContext):
    await state.update_data({"video": mess.video[-1].file_id, "text": mess.caption, "type": "video"})
    await mess.answer("Сообщение для рассылки: ")
    await mess.answer_video(mess.document[-1].file_id, mess.caption, reply_markup=kb.menu_notif("video"))


@router.callback_query(F.data == "yes_text")
async def processed_notif_text(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    data = await state.get_data()
    user_id = get_all_user()
    text = data["text"]
    for i in user_id:
        try:
            await bot.send_message(i, text)
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
    await state.clear()
    await call.message.answer("Рассылка успешно отправлена", reply_markup=kb.menu_admin())


@router.callback_query(F.data == "yes_photo")
async def processed_notif_photo(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    data = await state.get_data()
    user_id = get_all_user()
    text = data["text"]
    photo = data["photo"]
    for i in user_id:
        try:
            await bot.send_photo(i, photo, caption=text)
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
    await state.clear()
    await call.message.answer("Рассылка успешно отправлена", reply_markup=kb.menu_admin())


@router.callback_query(F.data == "yes_doc")
async def processed_notif_doc(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    data = await state.get_data()
    user_id = get_all_user()
    doc = data["doc"]
    text = data["text"]
    for i in user_id:
        try:
            await bot.send_document(i, doc, caption=text)
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
    await state.clear()
    await call.message.answer("Рассылка успешно отправлена", reply_markup=kb.menu_admin())


@router.callback_query(F.data == "yes_video")
async def processed_notif_video(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    data = await state.get_data()
    user_id = get_all_user()
    video = data["video"]
    text = data["text"]
    for i in user_id:
        try:
            await bot.send_video(i, video, caption=text)
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
    await state.clear()
    await call.message.answer("Рассылка успешно отправлена", reply_markup=kb.menu_admin())

