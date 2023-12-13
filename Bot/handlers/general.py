from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from .registration import Registration
from Bot.filters.filters import UserIsActive
from Bot.google_doc.googleSheets import save_new_user
import Bot.keyboard.general as kb
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


@router.message(CommandStart(), UserIsActive(True))
async def start_not_active(mess: Message):
    await mess.answer_invoice(
        title="Оплата курса",
        description="Для доступа к курсу, необходимо оформить подписку!",
        payload="buy",
        provider_token="381764678:TEST:73067",
        currency="RUB",
        prices=[LabeledPrice(label="Подписка", amount=120000)]
    )
    save_new_user(mess.from_user.id)


@router.message(CommandStart(), UserIsActive(False))
async def start_is_active(mess: Message, state: FSMContext):
    await state.set_state(Registration.TimeZone)
    await mess.answer("У вас есть действующая подписка! Поздравляю!\n"
                      "Пожалуйста, выберите свой часовой пояс", reply_markup=kb.time_zone())
    save_new_user(mess.from_user.id)


@router.callback_query(F.data == "menu", StateFilter(None))
async def main_menu(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Тут будет главное меню!")
