import os
import datetime as dt
from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.filters import Command, CommandStart
from aiogram.utils.media_group import MediaGroupBuilder

from Bot.google_doc.googleSheets import save_data_user
import Bot.keyboard.general as kb
import Bot.function as fun

router = Router()


class Registration(StatesGroup):
    TimeZone = State()
    FullName = State()
    Birthday = State()
    Height = State()
    Weight = State()
    Address = State()
    PhoneEmail = State()
    Photo1 = State()
    Photo2 = State()
    Photo3 = State()
    Photo4 = State()
    DataStart = State()
    Check = State()


@router.callback_query(F.data.split("_")[0] == "tz", Registration.TimeZone)
async def save_timezone(call: CallbackQuery, state: FSMContext):
    await state.set_data({"tz": call.data.split("_")[1]})
    await call.message.edit_text("Пожалуйста, введите ваши ФИО", reply_markup=None)
    await state.set_state(Registration.FullName)


@router.message(Registration.FullName)
async def save_full_name(mess: Message, state: FSMContext):
    await state.update_data({"full_name": mess.text})
    await mess.answer("Пожалуйста, введите вашу дату рождения в формате «ДД.ММ.ГГГГ»\nПример: «07.08.1984»")
    await state.set_state(Registration.Birthday)


@router.message(Registration.Birthday)
async def save_birthday(mess: Message, state: FSMContext):
    if fun.check_data(mess.text):
        await state.update_data({"birthday": mess.text})
        await mess.answer("Пожалуйста, введите ваш рост цифрами (в см)")
        await state.set_state(Registration.Height)
    else:
        await mess.answer("Дата рождения указана неверно! \n"
                          "Пожалуйста, введите вашу дату рождения в формате «ДД.ММ.ГГГГ»\nПример: «07.08.1984»")


@router.message(Registration.Height)
async def save_height(mess: Message, state: FSMContext):
    try:
        height = int(mess.text)
        await state.update_data({"height": height})
        await mess.answer("Пожалуйста, введите ваш вес цифрами (в кг)")
        await state.set_state(Registration.Weight)
    except ValueError:
        await mess.answer("Введите только число!")


@router.message(Registration.Weight)
async def save_weight(mess: Message, state: FSMContext):
    try:
        weight = int(mess.text)
        await state.update_data({"weight": weight})
        await mess.answer("Пожалуйста, напишите Ваш адрес, чтобы мы могли отправить продукцию к курсу. "
                          "\nЖелательный формат: Область, Город, Улица, Дом, Квартира")
        await state.set_state(Registration.Address)
    except ValueError:
        await mess.answer("Введите только число!")


@router.message(Registration.Address)
async def save_address(mess: Message, state: FSMContext):
    await state.update_data({"address": mess.text})
    await mess.answer("Пожалуйста, напишите, свой email или нажмите на кнопку \"Поделиться контактом\", "
                      "чтобы мы могли уведомить Вас о поступлении товара", reply_markup=kb.share_number())
    await state.set_state(Registration.PhoneEmail)


@router.message(Registration.PhoneEmail)
async def save_phone(mess: Message, state: FSMContext):
    await state.update_data({"del": mess.message_id})
    try:
        await state.update_data({"phone_email": mess.contact.phone_number})
    except AttributeError:
        await state.update_data({"phone_email": mess.text})
    await mess.answer("Благодарим Вас за пройденный опрос.\n", reply_markup=kb.ReplyKeyboardRemove())
    await mess.answer(
        "Для того, чтобы после прохождения курса вы смогли наглядно увидеть разницу до и после его прохождения, "
        "мы рекомендуем вам сделать фотографии 4 вашего тела (1 спереди, 1 сзади, 2 по бокам). "
        "\nПожалуйста сделайте их и отправьте последовательно в этот чат, "
        "чтобы по итогу прохождения получить коллаж «До/После»\n\n"
        "Ожидаю фотографию спереди!", reply_markup=kb.custom_button("Отказаться", "skip_photo"))
    await state.set_state(Registration.Photo1)


@router.message(F.photo, Registration.Photo1)
async def save_photo_front(mess: Message, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(mess.from_user.id, mess.message_id-1, reply_markup=None)
    if not (os.path.isdir(f"{fun.home}/user_photo/{fun.admins[0]}")):
        os.mkdir(f"{fun.home}/user_photo/{fun.admins[0]}")
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/front.jpg")
    await state.update_data({"photo1": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию сзади!")
    await state.set_state(Registration.Photo2)


@router.message(F.photo, Registration.Photo2)
async def save_photo_behind(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/behind.jpg")
    await state.update_data({"photo2": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию слева!")
    await state.set_state(Registration.Photo3)


@router.message(F.photo, Registration.Photo3)
async def save_photo_front_side_l(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/side_l.jpg")
    await state.update_data({"photo3": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию справа!")
    await state.set_state(Registration.Photo4)


@router.message(F.photo, Registration.Photo4)
async def save_photo_side_r(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/user_photo/{mess.from_user.id}/side_r.jpg")
    await state.update_data({"photo4": mess.photo[-1].file_id})
    await mess.answer("Отлично, все фотографии приняты!", reply_markup=kb.check_photo())


@router.callback_query(Registration.Photo4, F.data == "restart_photo")
async def check_photo(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(Registration.Photo1)
    await call.message.answer("Ожидаю фотографию спереди!")


@router.callback_query(Registration.Photo1, F.data == "skip_photo")
@router.callback_query(Registration.Photo4, F.data == "next")
async def view_date_start(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state(Registration.DataStart)
    await call.message.answer("Пожалуйста, выберите дату старта курса", reply_markup=kb.kalendar())


@router.callback_query(Registration.DataStart, F.data.split("-")[0] == "next")
async def view_next_month(call: CallbackQuery, state: FSMContext):
    in_data = dt.date(int(call.data.split("-")[1]), int(call.data.split("-")[2]), int(call.data.split("-")[3]))
    if dt.date.today() + dt.timedelta(days=14) < in_data:
    # if dt.date(2023, 12, 22) + dt.timedelta(days=14) > in_data:
        await call.message.edit_reply_markup(
            reply_markup=kb.kalendar((dt.date(in_data.year, in_data.month, in_data.day)+dt.timedelta(days=31))))
    else:
        await call.answer("Доступных дат больше нет")


@router.callback_query(Registration.DataStart, F.data.split("-")[0] == "back")
async def view_back_month(call: CallbackQuery, state: FSMContext):
    in_data = dt.date(int(call.data.split("-")[1]), int(call.data.split("-")[2]), int(call.data.split("-")[3]))
    if dt.date.today() + dt.timedelta(days=14) < in_data:
    # if dt.date(2023, 12, 22) + dt.timedelta(days=14) < in_data:
        await call.message.edit_reply_markup(
            reply_markup=kb.kalendar((dt.date(in_data.year, in_data.month, in_data.day)-dt.timedelta(days=31))))
    else:
        await call.answer("Доступных дат больше нет")


@router.callback_query(Registration.DataStart, F.data.split == "month")
async def answer_month(call: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(call.id)
    await call.answer("Выберите дату в представленном месяце")


@router.callback_query(Registration.DataStart, F.data.split("-")[0] == "setd")
async def save_date_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    if call.data.split("-")[1] != "":
        await call.message.delete()
        await state.update_data({"data_start": f'{call.data.split("-")[1]}.{call.data.split("-")[2]}.{call.data.split("-")[3]}'})
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
                                  f"Часовой пояс: +{data['tz']}\n"
                                  f"Рост: {data['height']}\n"
                                  f"Вес: {data['weight']}\n"
                                  f"Адрес: {data['address']}\n"
                                  f"Контакт: {data['phone_email']}\n"
                                  f"Дата начала курса: {data['data_start']}\n", reply_markup=kb.check_form())
        await state.set_state(Registration.Check)
    else:
        await call.answer("Данная дата недоступна для начала курса.")


@router.callback_query(Registration.Check, F.data == "restart_form")
async def check_restart(call: CallbackQuery, state: FSMContext):
    await state.set_data({"rest": 0})
    await state.set_state(Registration.TimeZone)
    await call.message.answer("Пожалуйста, выберите свой часовой пояс", reply_markup=kb.time_zone())


@router.callback_query(Registration.Check, F.data == "next")
async def check_restart(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    save_data_user(call.from_user.id, data)
    await call.message.edit_text(
        f"Благодарим Вас за покупку курса. Ваш курс начинается <b>{data['data_start']}</b> в 05:00. "
        "Вы можете изменить дату старта не позднее чем за 5 часов перед началом")
    await state.clear()
