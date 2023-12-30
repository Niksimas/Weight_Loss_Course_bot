from decouple import config

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery

import Bot.keyboard.general as kb
from Bot.handlers.registration import Registration
from Bot.BD.work_db import save_new_user, update_activity_user


router = Router()
pay_token = config("pay_token")


@router.callback_query(Registration.GroupIndividual, F.data == "individual")
async def start_not_active(call: CallbackQuery, bot: Bot):
    await call.message.delete()
    msg = await bot.send_invoice(
        call.from_user.id,
        title="Оплата курса",
        description="Оформление подписки!",
        payload="buy",
        provider_token=pay_token,
        currency="RUB",
        prices=[LabeledPrice(label="Подписка", amount=10000)]
    )
    save_new_user(call.from_user.id, call.from_user.username)


@router.pre_checkout_query(lambda query: True)
async def start_not_active(pre_checkout_query: PreCheckoutQuery):
    # Проверка на доступность товара, возврат True если все супер-пупер
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(mess: Message, state: FSMContext, bot: Bot):
    await bot.delete_message(mess.from_user.id, mess.message_id-1)
    await mess.answer("Спасибо за оплату!")
    update_activity_user(mess.from_user.id)
    await state.set_state(Registration.DataStart)
    await state.update_data({"group_individual": "individual"})
    await mess.answer("Пожалуйста, выберите дату старта курса", reply_markup=kb.kalendar())