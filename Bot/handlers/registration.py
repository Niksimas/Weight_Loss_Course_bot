import os
from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.filters import Command, CommandStart

from Bot.filters.filters import UserIsActive
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


@router.callback_query(F.data.split("_")[0] == "tz", Registration.TimeZone)
async def save_timezone(call: CallbackQuery, state: FSMContext):
    await state.set_data({"tz": call.data.split("_")[1]})
    await call.message.edit_text("Пожалуйста, введите ваши ФИО", reply_markup=None)
    await state.set_state(Registration.FullName)


@router.message(Registration.FullName)
async def save_full_name(mess: Message, state: FSMContext):
    await state.update_data({"full_name": mess.text})
    await mess.answer("Пожалуйста, введите вашу дату рождения в формате «ДД.ММ.ГГГГ», Пример: «07.08.1984»")
    await state.set_state(Registration.Birthday)


@router.message(Registration.Birthday)
async def save_birthday(mess: Message, state: FSMContext):
    if fun.check_data(mess.text):
        await state.update_data({"birthday": mess.text})
        await mess.answer("Пожалуйста, введите ваш рост цифрами")
        await state.set_state(Registration.Height)
    else:
        await mess.answer("Дата рождения указана неверно! \n"
                          "Пожалуйста, введите вашу дату рождения в формате «ДД.ММ.ГГГГ», Пример: «07.08.1984»")


@router.message(Registration.Height)
async def save_height(mess: Message, state: FSMContext):
    await state.update_data({"height": mess.text})
    await mess.answer("Пожалуйста, введите ваш вес цифрами")
    await state.set_state(Registration.Weight)


@router.message(Registration.Weight)
async def save_weight(mess: Message, state: FSMContext):
    await state.update_data({"weight": mess.text})
    await mess.answer("Пожалуйста, напишите Ваш адрес, чтобы мы могли отправить продукцию к курсу. "
                      "\nЖелательный формат: Область, Город, Улица, Дом, Квартира")
    await state.set_state(Registration.Address)


@router.message(Registration.Address)
async def save_address(mess: Message, state: FSMContext):
    await state.update_data({"address": mess.text})
    await mess.answer("Пожалуйста, напишите, свой email или нажмите на кнопку \"Поделиться контактом\", "
                      "чтобы мы могли уведомить Вас о поступлении товара", reply_markup=kb.share_number())
    await state.set_state(Registration.PhoneEmail)


@router.message(Registration.PhoneEmail)
async def save_phone(mess: Message, state: FSMContext):
    try:
        await state.update_data({"phone_email": mess.contact.phone_number})
    except AttributeError:
        await state.update_data({"phone_email": mess.text})
    await mess.answer(
        "Благодарим Вас за пройденный опрос.\n"
        "Для того, чтобы после прохождения курса вы смогли наглядно увидеть разницу до и после его прохождения, "
        "мы рекомендуем вам сделать фотографии 4 вашего тела (1 спереди, 1 сзади, 2 по бокам). "
        "\nПожалуйста сделайте их и отправьте последовательно в этот чат, "
        "чтобы по итогу прохождения получить коллаж «До/После»", reply_markup=kb.ReplyKeyboardRemove())
    await mess.answer("Ожидаю фотографию спереди!", reply_markup=kb.custom_button("Отказаться", "skip_photo"))
    await state.set_state(Registration.Photo1)


@router.message(F.photo, Registration.Photo1)
async def save_photo_front(mess: Message, state: FSMContext, bot: Bot):
    os.mkdir(f"{fun.home}/user_photo/{mess.from_user.id}")
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/{mess.from_user.id}/front.jpg")
    await state.update_data({"photo1": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию сзади!")
    await state.set_state(Registration.Photo2)


@router.message(F.photo, Registration.Photo2)
async def save_photo_behind(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/{mess.from_user.id}/behind.jpg")
    await state.update_data({"photo2": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию слева!")
    await state.set_state(Registration.Photo3)


@router.message(F.photo, Registration.Photo3)
async def save_photo_front_side_l(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/{mess.from_user.id}/side_l.jpg")
    await state.update_data({"photo1": mess.photo[-1].file_id})
    await mess.answer("Ожидаю фотографию справа!")
    await state.set_state(Registration.Photo4)


@router.message(F.photo, Registration.Photo4)
async def save_photo_side_r(mess: Message, state: FSMContext, bot: Bot):
    await bot.download(mess.photo[-1].file_id, destination=f"{fun.home}/{mess.from_user.id}/side_r.jpg")
    await state.update_data({"photo1": mess.photo[-1].file_id})
    await mess.answer("Отлично, все фотографии приняты!", reply_markup=kb.check())


@router.callback_query(Registration.Photo4, F.data == "restart_photo")
async def check_photo(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(Registration.Photo1)
    await call.message.answer("Ожидаю фотографию спереди!")


@router.callback_query(Registration.Photo4, F.data == "skip_photo")
@router.callback_query(Registration.Photo4, F.data == "next")
async def save_date_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("rfktylfhm", reply_markup=kb.kalendar())




