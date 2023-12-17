from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.filters import Command, CommandStart, StateFilter

import Bot.keyboard.general as kb

from Bot.BD.work_db import save_new_user, update_activity_user

from Bot.handlers.registration import Registration

router = Router()

"""
shopId 506751
shopArticleId 538350
Для оплаты используйте данные тестовой карты: 1111 1111 1111 1026, 12/22, CVC 000."""


"""
- PayMaster Test: 1744374395:TEST:ee3bb77727f8477fc5ef 
- ПСБ Test: 1832575495:TEST:48b12b055e29c8d3ebd2b6b96d709521390d517b163a12be585cbb4c2178e9d1
- ЮKassa Test: 381764678:TEST:73067

"""


@router.message(CommandStart())
async def start_not_active(mess: Message):
    await mess.answer_invoice(
        title="Оплата курса",
        description="Для доступа к курсу, необходимо оформить подписку!",
        payload="buy",
        provider_token="390540012:LIVE:43966",
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
