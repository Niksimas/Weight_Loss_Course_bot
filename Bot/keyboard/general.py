import datetime as dt
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup, WebAppInfo)
import Bot.function as fun
from Bot.BD.work_db import get_id_admin


# web_app=WebAppInfo(
def main_start(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='📄 Оферта', url="https://telegra.ph/Ofer-12-12")],
        [InlineKeyboardButton(text='⚠️ Перед тем как купить курс', url="https://telegra.ph/prilozhenie-12-12-2")],
        [InlineKeyboardButton(text='➡️ Перейти к курсу', callback_data="course")],
        [InlineKeyboardButton(text='💬 Обратная связь', url="https://t.me/Yugra13")],
    ]
    if user_id in get_id_admin():
        buttons.append([InlineKeyboardButton(text='Администратору', callback_data="admin")],)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def main_menu(edit_time: bool = False) -> InlineKeyboardMarkup:
    buttons = []
    if edit_time:
        buttons.append([InlineKeyboardButton(text='Изменить дату старта', callback_data="edit_data_start")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def time_zone() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='+2', callback_data="tz_2"),
            InlineKeyboardButton(text='+3', callback_data="tz_3"),
            InlineKeyboardButton(text='+4', callback_data="tz_4")
        ],
        [
            InlineKeyboardButton(text='+5', callback_data="tz_5"),
            InlineKeyboardButton(text='+6', callback_data="tz_6"),
            InlineKeyboardButton(text='+7', callback_data="tz_7"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def share_number() -> ReplyKeyboardMarkup:
    button = [[KeyboardButton(text='Поделиться контактом', request_contact=True)]]
    keyboard = ReplyKeyboardMarkup(keyboard=button, one_time_keyboard=True, resize_keyboard=True)
    return keyboard


def custom_button(text: str, callback_data: str) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=text, callback_data=callback_data)]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def check_custom(yes_text: str, no_text: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Отправить заново", callback_data="yes"),
            InlineKeyboardButton(text="Сохранить и продолжить", callback_data="no")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def check_photo() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Отправить заново", callback_data="restart_photo"),
            InlineKeyboardButton(text="Сохранить и продолжить", callback_data="next")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def check_form() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Заполнить заново", callback_data="restart_form"),
            InlineKeyboardButton(text="Все верно", callback_data="next")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def kalendar(in_data: dt.date = dt.date.today()) -> InlineKeyboardMarkup:
    data_fun = fun.creat_list_calendar(in_data)
    buttons = [
        [
            InlineKeyboardButton(text=f"{data_fun['back']}", callback_data=f"back-{in_data}"),
            InlineKeyboardButton(text=f"{in_data.month}.{in_data.year}", callback_data="month"),
            InlineKeyboardButton(text=f"{data_fun['next']}", callback_data=f"next-{in_data}")
        ],
        [
            InlineKeyboardButton(text=data_fun["days"][0], callback_data=f"setd-{data_fun['days'][0]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][1], callback_data=f"setd-{data_fun['days'][1]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][2], callback_data=f"setd-{data_fun['days'][2]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][3], callback_data=f"setd-{data_fun['days'][3]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][4], callback_data=f"setd-{data_fun['days'][4]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][5], callback_data=f"setd-{data_fun['days'][5]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][6], callback_data=f"setd-{data_fun['days'][6]}-{in_data.month}-{in_data.year}"),
        ],
        [
            InlineKeyboardButton(text=data_fun["days"][7], callback_data=f"setd-{data_fun['days'][7]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][8], callback_data=f"setd-{data_fun['days'][8]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][9], callback_data=f"setd-{data_fun['days'][9]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][10], callback_data=f"setd-{data_fun['days'][10]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][11], callback_data=f"setd-{data_fun['days'][11]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][12], callback_data=f"setd-{data_fun['days'][12]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][13], callback_data=f"setd-{data_fun['days'][13]}-{in_data.month}-{in_data.year}"),
        ],
        [
            InlineKeyboardButton(text=data_fun["days"][14], callback_data=f"setd-{data_fun['days'][14]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][15], callback_data=f"setd-{data_fun['days'][15]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][16], callback_data=f"setd-{data_fun['days'][16]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][17], callback_data=f"setd-{data_fun['days'][17]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][18], callback_data=f"setd-{data_fun['days'][18]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][19], callback_data=f"setd-{data_fun['days'][19]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][20], callback_data=f"setd-{data_fun['days'][20]}-{in_data.month}-{in_data.year}"),
        ],
        [
            InlineKeyboardButton(text=data_fun["days"][21], callback_data=f"setd-{data_fun['days'][21]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][22], callback_data=f"setd-{data_fun['days'][22]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][23], callback_data=f"setd-{data_fun['days'][23]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][24], callback_data=f"setd-{data_fun['days'][24]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][25], callback_data=f"setd-{data_fun['days'][25]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][26], callback_data=f"setd-{data_fun['days'][26]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][27], callback_data=f"setd-{data_fun['days'][27]}-{in_data.month}-{in_data.year}"),
        ],
        [
            InlineKeyboardButton(text=data_fun["days"][28], callback_data=f"setd-{data_fun['days'][28]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][29], callback_data=f"setd-{data_fun['days'][29]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][30], callback_data=f"setd-{data_fun['days'][30]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][31], callback_data=f"setd-{data_fun['days'][31]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][32], callback_data=f"setd-{data_fun['days'][32]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][33], callback_data=f"setd-{data_fun['days'][33]}-{in_data.month}-{in_data.year}"),
            InlineKeyboardButton(text=data_fun["days"][34], callback_data=f"setd-{data_fun['days'][34]}-{in_data.month}-{in_data.year}"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def end_form() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Супер! Спасибо", callback_data="menu"),
            InlineKeyboardButton(text="Изменить дату", callback_data="edit_time")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
