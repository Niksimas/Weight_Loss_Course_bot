from decouple import config

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

import Bot.keyboard.general as kb
from Bot.handlers.registration import Registration
from Bot.BD.work_db import save_new_user, update_activity_user


router = Router()
pay_token = config("pay_token")


@router.message(CommandStart())
async def start_not_active(mess: Message):
    await mess.answer_invoice(
        title="Оплата курса",
        description="Для доступа к курсу, необходимо оформить подписку!",
        payload="buy",
        provider_token=pay_token,
        currency="RUB",
        prices=[LabeledPrice(label="Подписка", amount=10000)]
    )
    save_new_user(mess.from_user.id, mess.from_user.username)


@router.pre_checkout_query(lambda query: True)
async def start_not_active(pre_checkout_query: PreCheckoutQuery):
    # Проверка на доступность товара, возврат True если все супер-пупер
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(mess: Message, state: FSMContext):
    await mess.answer("Спасибо за оплату!")
    update_activity_user(mess.from_user.id)
    await state.set_state(Registration.TimeZone)
    await mess.answer("Пожалуйста, выберите свой часовой пояс", reply_markup=kb.time_zone())
