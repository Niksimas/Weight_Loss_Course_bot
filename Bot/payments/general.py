from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.filters import Command, CommandStart

from Bot.google_doc.googleSheets import save_active_user
from Bot.handlers.registration import Registration
import Bot.keyboard.general as kb

router = Router()

"""
shopId 506751
shopArticleId 538350
Для оплаты используйте данные тестовой карты: 1111 1111 1111 1026, 12/22, CVC 000."""


@router.pre_checkout_query(lambda query: True)
async def start_not_active(pre_checkout_query: PreCheckoutQuery):
    # Проверка на доступность товара, возврат True если все супер-пупер
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(mess: Message, state: FSMContext):
    await mess.answer("Спасибо за оплату!")
    save_active_user(mess.from_user.id, mess.from_user.username)
    await state.set_state(Registration.TimeZone)
    await mess.answer("Пожалуйста, выберите свой часовой пояс", reply_markup=kb.time_zone())
