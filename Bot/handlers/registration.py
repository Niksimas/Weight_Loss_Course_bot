import os
import json
import datetime as dt

from aiogram import Bot, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import Bot.function as fun
import Bot.keyboard.general as kb
from Bot.BD.work_db import save_data_user, update_activity_user

router_reg = Router()


class Registration(StatesGroup):
    Confirmation = State()
    TimeZone = State()
    FullName = State()
    Birthday = State()
    Height = State()
    Weight = State()
    Address = State()
    Phone = State()
    Email = State()
    Photo1 = State()
    Photo2 = State()
    Photo3 = State()
    Photo4 = State()
    ChoiceGI = State()
    Group = State()
    Individual = State()
    DataStart = State()
    DataStartR = State()
    Check = State()


@router_reg.callback_query(F.data == "course", StateFilter(None))
async def call_course(call: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.Confirmation)
    msg = await call.message.edit_text("Прочитайте Пользовательское соглашение и Политику Конфиденциальности",
                                       reply_markup=kb.policy_confirmation())
    await state.update_data({"del": msg.message_id})


@router_reg.callback_query(F.data == "yes", StateFilter(Registration.Confirmation))
async def call_course(call: CallbackQuery, state: FSMContext, bot:Bot):
    await state.set_state(Registration.TimeZone)
    msg = await call.message.edit_text("Пожалуйста, выберите свой часовой пояс относительно 0 пояса\n"
                                 "(Москва - UTC+3)", reply_markup=kb.time_zone())
    await state.update_data({"del": msg.message_id})
    await bot.send_message(1074482794, "Пользователь согласился с пользовательским соглашением:\n"
                                       f"Дата и время: {dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S.%f')}\n"
                                       f"ID: {call.from_user.id}\n"
                                       f"Имя: [{call.from_user.first_name}](tg://user?id={call.from_user.id})\n"
                                       f"Ссылка: @{call.from_user.username}\n\n", parse_mode="Markdown")


@router_reg.callback_query(F.data.split("_")[0] == "tz", Registration.TimeZone)
async def save_timezone(call: CallbackQuery, state: FSMContext):
    await state.set_data({"timezone": call.data.split("_")[1], "user_id": call.from_user.id, "photo": 0})
    await call.message.edit_text("Пожалуйста, введите ваши ФИО", reply_markup=None)
    await state.set_state(Registration.FullName)


@router_reg.callback_query(F.data == "course", Registration.FullName)
async def save_full_name(call: CallbackQuery):
    msg = await call.message.edit_text("Пожалуйста, введите ваши ФИО", reply_markup=None)


@router_reg.message(Registration.FullName)
async def save_full_name(mess: Message, state: FSMContext):
    await state.update_data({"full_name": mess.text})
    await mess.answer("Пожалуйста, введите вашу дату рождения в формате «ДД.ММ.ГГГГ»\nПример: «07.08.1984»")
    await state.set_state(Registration.Birthday)


@router_reg.callback_query(F.data == "course", Registration.Birthday)
async def save_full_name(call: CallbackQuery):
    await call.message.edit_text("Пожалуйста, введите вашу дату рождения в формате «ДД.ММ.ГГГГ»\nПример: «07.08.1984»",
                                 reply_markup=None)


@router_reg.message(Registration.Birthday)
async def save_birthday(mess: Message, state: FSMContext):
    if fun.check_data(mess.text):
        await state.update_data({"birthday": mess.text})
        await mess.answer("Пожалуйста, введите ваш рост цифрами (в см)")
        await state.set_state(Registration.Height)
    else:
        await mess.answer("Дата рождения указана неверно! \n"
                          "Пожалуйста, введите вашу дату рождения в формате «ДД.ММ.ГГГГ»\nПример: «07.08.1984»")


@router_reg.callback_query(F.data == "course", Registration.Height)
async def save_full_name(call: CallbackQuery):
    await call.message.edit_text("Пожалуйста, введите ваш рост цифрами (в см)",
                                 reply_markup=None)


@router_reg.message(Registration.Height)
async def save_height(mess: Message, state: FSMContext):
    try:
        height = int(mess.text)
        await state.update_data({"height": str(height)})
        await mess.answer("Пожалуйста, введите ваш вес цифрами (в кг)")
        await state.set_state(Registration.Weight)
    except ValueError:
        await mess.answer("Введите только число!")


@router_reg.callback_query(F.data == "course", Registration.Weight)
async def save_full_name(call: CallbackQuery):
    await call.message.edit_text("Пожалуйста, введите ваш вес цифрами (в кг)",
                                 reply_markup=None)


@router_reg.message(Registration.Weight)
async def save_weight(mess: Message, state: FSMContext):
    try:
        weight = int(mess.text)
        await state.update_data({"weight": str(weight)})
        await mess.answer("Пожалуйста укажите адрес пункта выдачи СДЭК, для отправки сбора трав.\n"
                          "Формат адреса: город (поселок/область), улица, дом, офис.")
        await state.set_state(Registration.Address)
    except ValueError:
        await mess.answer("Введите только число!")


@router_reg.callback_query(F.data == "course", Registration.Address)
async def save_full_name(call: CallbackQuery):
    await call.message.edit_text("Пожалуйста укажите адрес пункта выдачи СДЭК, для отправки сбора трав.\n"
                                 "Формат адреса: город (поселок/область), улица, дом, офис.",
                                 reply_markup=None)


@router_reg.message(Registration.Address)
async def save_address(mess: Message, state: FSMContext):
    await state.update_data({"address": mess.text})
    await mess.answer("Пожалуйста, напишите, свой номер телефона или нажмите на кнопку \"Поделиться контактом\", "
                      "чтобы мы могли уведомить Вас о поступлении товара", reply_markup=kb.share_number())
    await state.set_state(Registration.Phone)


@router_reg.callback_query(F.data == "course", Registration.Phone)
async def save_full_name(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Пожалуйста, напишите, свой номер телефона или нажмите на кнопку "
                                 "\"Поделиться контактом\", чтобы мы могли уведомить Вас о поступлении товара",
                                 reply_markup=kb.share_number())


@router_reg.message(Registration.Phone)
async def save_phone(mess: Message, state: FSMContext):
    try:
        await state.update_data({"phone": mess.contact.phone_number})
    except AttributeError:
        await state.update_data({"phone": mess.text})
    await mess.answer("Пожалуйста, напишите email и ник Instagram", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.Email)


@router_reg.callback_query(F.data == "course", Registration.Email)
async def save_full_name(call: CallbackQuery):
    await call.message.edit_text("Пожалуйста, напишите email и ник Instagram", reply_markup=None)


@router_reg.message(Registration.Email)
async def save_phone(mess: Message, state: FSMContext):
    msg = await mess.answer(
        "Благодарим Вас за пройденный опрос.\n"
        "Для того, чтобы после прохождения курса вы смогли наглядно увидеть разницу до и после его прохождения, "
        "я рекомендую вам сделать фотографии 4 вашего тела (1 спереди, 1 сзади, 2 по бокам). "
        "\nПожалуйста сделайте их и отправьте последовательно в этот чат, "
        "чтобы по итогу прохождения получить коллаж «До/После»\n\n"
        "Если не хотите делиться фото, сделайте его для себя и сохраните, для того, "
        "чтобы наглядно увидеть результат по прохождению курса\n\n"
        "Ожидаю фотографию спереди!", reply_markup=kb.custom_button("Отказаться", "skip_photo"))
    await state.update_data({"del": msg.message_id, "email": mess.text})
    await state.set_state(Registration.Photo1)


@router_reg.callback_query(F.data == "course", Registration.Photo1)
async def save_full_name(call: CallbackQuery):
    await call.message.edit_text(
        "Благодарим Вас за пройденный опрос.\n"
        "Для того, чтобы после прохождения курса вы смогли наглядно увидеть разницу до и после его прохождения, "
        "я рекомендую вам сделать фотографии 4 вашего тела (1 спереди, 1 сзади, 2 по бокам). "
        "\nПожалуйста сделайте их и отправьте последовательно в этот чат, "
        "чтобы по итогу прохождения получить коллаж «До/После»\n\n"
        "Если не хотите делиться фото, сделайте его для себя и сохраните, для того, "
        "чтобы наглядно увидеть результат по прохождению курса\n\n"
        "Ожидаю фотографию спереди!",
        reply_markup=kb.custom_button("Отказаться", "skip_photo"))


@router_reg.message(F.media_group_id, Registration.Photo1)
@router_reg.message(F.media_group_id, Registration.Photo2)
@router_reg.message(F.media_group_id, Registration.Photo3)
@router_reg.message(F.media_group_id, Registration.Photo4)
async def save_photo_front(mess: Message, state: FSMContext):
    data = await state.get_data()
    try:
        b = data["group_id"]
    except KeyError:
        await state.update_data({"group_id": mess.media_group_id})
        await mess.answer("Фотографии надо отправлять поочереди")


@router_reg.message(F.photo, Registration.Photo1)
async def save_photo_front(mess: Message, state: FSMContext, bot: Bot):
    try:
        await bot.edit_message_reply_markup(mess.from_user.id, mess.message_id-1, reply_markup=None)
    except:
        pass
    if not (os.path.isdir(f"{fun.home}/user_photo/{mess.from_user.id}")):
        os.mkdir(f"{fun.home}/user_photo/{mess.from_user.id}")
    await state.update_data({"photo": 1})
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/front.jpg")
    await state.update_data({"photo1": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию сзади!")
    await state.set_state(Registration.Photo2)


@router_reg.callback_query(F.data == "course", Registration.Photo2)
async def save_full_name(call: CallbackQuery):
    await call.message.edit_text("Ожидаю фотографию сзади!", reply_markup=None)


@router_reg.message(F.photo, Registration.Photo2)
async def save_photo_behind(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/behind.jpg")
    await state.update_data({"photo2": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию слева!")
    await state.set_state(Registration.Photo3)


@router_reg.callback_query(F.data == "course", Registration.Photo3)
async def save_full_name(call: CallbackQuery):
    await call.message.edit_text("Ожидаю фотографию слева!", reply_markup=None)


@router_reg.message(F.photo, Registration.Photo3)
async def save_photo_front_side_l(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/side_l.jpg")
    await state.update_data({"photo3": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию справа!")
    await state.set_state(Registration.Photo4)


@router_reg.callback_query(F.data == "course", Registration.Photo4)
async def save_full_name(call: CallbackQuery):
    await call.message.edit_text("Ожидаю фотографию справа!", reply_markup=None)


@router_reg.message(F.photo, Registration.Photo4)
async def save_photo_side_r(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/side_r.jpg")
    await state.update_data({"photo4": mess.photo[-1].file_id})
    await mess.answer("Отлично, все фотографии приняты!", reply_markup=kb.check_photo())


@router_reg.message(StateFilter(Registration.Photo1, Registration.Photo2, Registration.Photo3, Registration.Photo4))
async def answer_text_in_foto(mess: Message):
    await mess.answer("Необходимо отправить фотографию!")


@router_reg.callback_query(Registration.Photo4, F.data == "restart_photo")
async def check_photo(call: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.Photo1)
    await call.message.answer("Ожидаю фотографию спереди!")


@router_reg.callback_query(F.data == "course", StateFilter(Registration.ChoiceGI, Registration.Group, Registration.Individual))
@router_reg.callback_query(Registration.Photo1, F.data == "skip_photo")
@router_reg.callback_query(Registration.Photo4, F.data == "next")
async def view_date_start(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state(Registration.ChoiceGI)
    await call.message.answer("Выберите как вы будите проходить курс: ",
                              reply_markup=kb.group_individual())


@router_reg.message(Registration.Group, F.successful_payment)
async def view_next_month(mess: Message, state: FSMContext, bot: Bot):
    with open(f"{fun.home}/file_mess_notif/group_info.json") as f:
        data = json.load(f)
    await mess.answer(f"Перейдите по ссылке в беседу вашей группы: {data['link']}.\n"
                      f"Обучение начнется {data['date']}",
                      reply_markup=kb.custom_button("В меню", "menu"))
    await state.update_data({"group_individual": "group", "data_start": data['date']})
    data_user = await state.get_data()
    await bot.delete_message(mess.from_user.id, data_user["del"])
    save_data_user(mess.from_user.id, data_user, mess.from_user.username)
    update_activity_user(mess.from_user.id, 2)
    await state.clear()


@router_reg.callback_query(Registration.DataStartR, F.data.split("-")[0] == "next")
@router_reg.callback_query(Registration.DataStart, F.data.split("-")[0] == "next")
async def view_next_month(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    in_data = dt.date(int(call.data.split("-")[1]), int(call.data.split("-")[2]), int(call.data.split("-")[3]))
    stop_day = dt.datetime.now(fun.tz[f"tz{data['timezone']}"]).date() + dt.timedelta(days=30)
    if dt.date(stop_day.year, stop_day.month, 1) > in_data:
        await call.message.edit_reply_markup(
            reply_markup=kb.kalendar(fun.adding_month(in_data)))
    else:
        await call.answer("Доступных дат больше нет")


@router_reg.callback_query(Registration.DataStartR, F.data.split("-")[0] == "back")
@router_reg.callback_query(Registration.DataStart, F.data.split("-")[0] == "back")
async def view_back_month(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    in_data = dt.date(int(call.data.split("-")[1]), int(call.data.split("-")[2]), int(call.data.split("-")[3]))
    stop_day = dt.datetime.now(fun.tz[f"tz{data['timezone']}"]).date() + dt.timedelta(days=1)
    if dt.date(stop_day.year, stop_day.month, 1) < in_data:
        await call.message.edit_reply_markup(
            reply_markup=kb.kalendar(fun.subtracting_month(in_data)))
    else:
        await call.answer("Доступных дат больше нет")


@router_reg.callback_query(Registration.DataStartR, F.data == "month")
@router_reg.callback_query(Registration.DataStart, F.data == "month")
async def answer_month(call: CallbackQuery):
    await call.answer("Выберите дату в представленном месяце")


@router_reg.callback_query(Registration.DataStart, F.data.split("-")[0] == "setd")
async def save_date_start(call: CallbackQuery, state: FSMContext):
    if call.data.split("-")[1] != "":
        await call.message.delete()
        if int(call.data.split("-")[2]) < 10:
            month = f'0{call.data.split("-")[2]}'
        else:
            month = call.data.split("-")[2]
        if int(call.data.split("-")[1]) < 10:
            day = f'0{call.data.split("-")[1]}'
        else:
            day = call.data.split("-")[1]
        await state.update_data({"data_start": f'{day}.{month}.{call.data.split("-")[3]}'})
        data = await state.get_data()
        try:
            media_group = MediaGroupBuilder()
            media_group.add_photo(media=data['photo1'])
            media_group.add_photo(media=data['photo2'])
            media_group.add_photo(media=data['photo3'])
            media_group.add_photo(media=data['photo4'])
            await call.message.answer_media_group(media=media_group.build())
        except KeyError:
            pass
        await call.message.answer("Проверьте правильность введенных данных:\n"
                                  f"ФИО: {data['full_name']}\n"
                                  f"Дата рождения: {data['birthday']}\n"
                                  f"Часовой пояс: +{data['timezone']}\n"
                                  f"Рост: {data['height']}\n"
                                  f"Вес: {data['weight']}\n"
                                  f"Адрес: {data['address']}\n"
                                  f"Контакт: {data['phone']}\n"
                                  f"Email: {data['email']}\n"
                                  f"Дата начала курса: {data['data_start']}\n", reply_markup=kb.check_form())
        await state.set_state(Registration.Check)
    else:
        await call.answer("Данная дата недоступна для начала курса.")


@router_reg.callback_query(Registration.Check, F.data == "restart_form")
async def check_restart(call: CallbackQuery, state: FSMContext):
    await state.set_data({})
    await state.set_state(Registration.TimeZone)
    await call.message.edit_text("Пожалуйста, выберите свой часовой пояс", reply_markup=kb.time_zone())


@router_reg.callback_query(Registration.Check, F.data == "next")
async def check_end(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    save_data_user(call.from_user.id, data, call.from_user.username)
    await call.message.edit_text(
        f"Благодарим Вас за покупку курса. Ваш курс начинается <b>{data['data_start']}</b> в 05:00. "
        "Вы можете изменить дату старта не позднее чем за 5 часов перед началом",
        reply_markup=kb.end_form())
    await state.clear()

