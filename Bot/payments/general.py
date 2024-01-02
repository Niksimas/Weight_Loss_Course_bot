from decouple import config

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery

import Bot.keyboard.general as kb
from Bot.handlers.registration import Registration
from Bot.BD.work_db import save_new_user, update_activity_user


router = Router()
pay_token = config("pay_token")


@router.callback_query(Registration.ChoiceGI, F.data == "individual")
async def start_not_active(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.delete()
    await state.set_state(Registration.Individual)
    msg = await bot.send_invoice(
        call.from_user.id,
        title="Оплата курса",
        description="Оформление подписки для индивидуального обучения!",
        payload="buy",
        provider_token=pay_token,
        currency="RUB",
        prices=[LabeledPrice(label="Подписка", amount=20000)]
    )
    await state.update_data({"del": msg.message_id})
    save_new_user(call.from_user.id, call.from_user.username)


@router.callback_query(Registration.ChoiceGI, F.data == "group")
async def start_not_active(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.delete()
    msg = await bot.send_invoice(
        call.from_user.id,
        title="Оплата курса",
        description="Оформление подписки для обучения в группе!",
        payload="buy",
        provider_token=pay_token,
        currency="RUB",
        prices=[LabeledPrice(label="Подписка", amount=10000)]
    )
    await state.set_state(Registration.Group)
    await state.update_data({"del": msg.message_id})
    save_new_user(call.from_user.id, call.from_user.username)


@router.pre_checkout_query(lambda query: True)
async def start_not_active(pre_checkout_query: PreCheckoutQuery):
    # Проверка на доступность товара, возврат True если все супер-пупер
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment, Registration.Individual)
async def process_successful_payment(mess: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.delete_message(mess.from_user.id, data["del"])
    await mess.answer("Спасибо за оплату!")
    update_activity_user(mess.from_user.id, 1)
    await state.set_state(Registration.DataStart)
    await state.update_data({"group_individual": "individual"})
    await mess.answer("Пожалуйста, выберите дату старта курса", reply_markup=kb.kalendar())