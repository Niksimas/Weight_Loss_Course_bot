import os
from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

import Bot.function as fun
from Bot.BD.work_db import *
import Bot.keyboard.general as kb

router_ff = Router()


class RegistrationF(StatesGroup):
    Height = State()
    Weight = State()
    Photo1 = State()
    Photo2 = State()
    Photo3 = State()
    Photo4 = State()


@router_ff.message(RegistrationF.Height)
async def save_height(mess: Message, state: FSMContext):
    try:
        height = int(mess.text)
        await state.update_data({"height": height})
        await mess.answer("Пожалуйста, введите ваш вес цифрами (в кг)")
        await state.set_state(RegistrationF.Weight)
    except ValueError:
        await mess.answer("Пожалуйста, введите ваш рост цифрами, без обозначения единиц измерения!")


@router_ff.message(RegistrationF.Weight)
async def save_weight(mess: Message, state: FSMContext):
    try:
        weight = int(mess.text)
        await state.update_data({"weight": weight})
        data = get_data_user(mess.from_user.id)
        if bool(data["photo"]):
            await mess.answer(
                "В начале курса вы загрузили 4 фотографии своего тела."
                "\nПожалуйста сделайте новые фотографии и отправьте последовательно в этот чат\n\n"
                "Ожидаю фотографию спереди!", reply_markup=kb.custom_button("Отказаться", "skip_photo"))
            await state.set_state(RegistrationF.Photo1)
        else:
            weight_old = data["weight"]
            update_weight_user(mess.from_user.id, weight_old + "_" + weight)
            await mess.answer(f"Ваш вес в начале курса: {weight_old}\n"
                              f"Ваш вес в конце курса: {weight}\n")
            await state.clear()
    except ValueError:
        await mess.answer("Пожалуйста, введите ваш вес цифрами, без обозначения единиц измерения!")


@router_ff.message(F.photo, RegistrationF.Photo1)
async def save_photo_front(mess: Message, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(mess.from_user.id, mess.message_id-1, reply_markup=None)
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/new_front.jpg")
    await state.update_data({"photo1": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию сзади!")
    await state.set_state(RegistrationF.Photo2)


@router_ff.message(F.photo, RegistrationF.Photo2)
async def save_photo_behind(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/new_behind.jpg")
    await state.update_data({"photo2": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию слева!")
    await state.set_state(RegistrationF.Photo3)


@router_ff.message(F.photo, RegistrationF.Photo3)
async def save_photo_front_side_l(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/new_side_l.jpg")
    await state.update_data({"photo3": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию справа!")
    await state.set_state(RegistrationF.Photo4)


@router_ff.message(F.photo, RegistrationF.Photo4)
async def save_photo_side_r(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/new_side_r.jpg")
    await state.update_data({"photo4": mess.photo[-1].file_id})
    await mess.answer("Отлично, все фотографии приняты!", reply_markup=kb.check_photo())


@router_ff.callback_query(RegistrationF.Photo4, F.data == "restart_photo")
async def check_photo(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(RegistrationF.Photo1)
    await call.message.answer("Ожидаю фотографию спереди!")


@router_ff.callback_query(RegistrationF.Photo1, F.data == "skip_photo")
@router_ff.callback_query(RegistrationF.Photo4, F.data == "next")
async def view_date_start(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data_old = get_data_user(call.message.from_user.id)
    update_height_user(call.from_user.id, data_old["height"]+"_"+data["height"])
    update_weight_user(call.from_user.id, data_old["weight"]+"_"+data["weight"])
    media_group = MediaGroupBuilder()
    path_dir = f"{fun.home}/user_photo/{call.from_user.id}"
    media_group.add_photo(media=FSInputFile(f"{path_dir}/front.jpg"))
    media_group.add_photo(media=FSInputFile(f"{path_dir}/new_front.jpg"))
    media_group.add_photo(media=FSInputFile(f"{path_dir}/behind.jpg"))
    media_group.add_photo(media=FSInputFile(f"{path_dir}/new_behind.jpg"))
    media_group.add_photo(media=FSInputFile(f"{path_dir}/side_l.jpg"))
    media_group.add_photo(media=FSInputFile(f"{path_dir}/new_side_l.jpg"))
    media_group.add_photo(media=FSInputFile(f"{path_dir}/side_r.jpg"))
    media_group.add_photo(media=FSInputFile(f"{path_dir}/new_side_r.jpg"))
    await call.message.answer_media_group(media=media_group.build())
    await call.message.answer(f"Ваш вес в начале курса: {data_old['weight']}\n"
                              f"Ваш вес в конце курса: {data['weight']}\n")
    await state.clear()
