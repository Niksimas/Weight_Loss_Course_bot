from typing import Union
import datetime as dt
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
import Bot.function as fun


def share_number() -> ReplyKeyboardMarkup:
    button = [[KeyboardButton(text='Поделиться контактом', request_contact=True)]]
    keyboard = ReplyKeyboardMarkup(keyboard=button, one_time_keyboard=True, resize_keyboard=True)
    return keyboard


def menu_admin() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Изменить информацию по дню", callback_data="edit_day")],
        [InlineKeyboardButton(text="Запустить рассылку", callback_data="start_notif")],
        [InlineKeyboardButton(text="Отправить личное сообщение", callback_data="send_mess_user")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def menu_notif(types: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Подтвердить", callback_data=f"yes_{types}")],
        [InlineKeyboardButton(text="Изменить", callback_data="restart_notif")],
        [InlineKeyboardButton(text="Отменить", callback_data="cancel_a")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard