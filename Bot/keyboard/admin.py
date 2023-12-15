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
        [InlineKeyboardButton(text="Изменить информацию по дню", callback_data="edit_day_mess")],
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


def course_days() -> InlineKeyboardMarkup:
    buttons = []
    k = 1
    for i in range(5):
        line = []
        for j in range(7):
            line.append(InlineKeyboardButton(text=f"{k}", callback_data=f"{k}"))
            k += 1
            if k==32:
                break
        buttons.append(line)
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="cancel_a")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def time_mess(num_day: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Ночное сообщение (00:00)", callback_data=f"{num_day}_night")],
        [InlineKeyboardButton(text="Утреннее сообщение (05:00)", callback_data=f"{num_day}_morning")],
        [InlineKeyboardButton(text="Дневное сообщение (13:00)", callback_data=f"{num_day}_day")],
        [InlineKeyboardButton(text="Вечернее сообщение (21:00)", callback_data=f"{num_day}_evening")],
        [InlineKeyboardButton(text="Назад", callback_data="back_day")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def edit_mess(time: str, num_day):
    buttons = [
        [InlineKeyboardButton(text="Изменить", callback_data=f"edit_{time}_{num_day}")],
        [InlineKeyboardButton(text="Назад", callback_data=f"back_time_{num_day}")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
