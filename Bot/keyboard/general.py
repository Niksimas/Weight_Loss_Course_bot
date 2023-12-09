from typing import Union
import datetime as dt
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
import Bot.function as fun


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


def check() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Отправить заново", callback_data="restart_photo"),
            InlineKeyboardButton(text="Отправить", callback_data="next")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
"✖️"


def kalendar(month: int = dt.date.today().month) -> InlineKeyboardMarkup:
    data = fun.creat_list_calendar(month)
    buttons = [
        [
            InlineKeyboardButton(text="<<<", callback_data=f"back_{month}"),
            InlineKeyboardButton(text=f"47", callback_data="month"),
            InlineKeyboardButton(text=">>>", callback_data=f"next_{month}")
        ],
        [
            InlineKeyboardButton(text=data["days"][0], callback_data=f"day_{data['days'][0]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][1], callback_data=f"day_{data['days'][1]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][2], callback_data=f"day_{data['days'][2]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][3], callback_data=f"day_{data['days'][3]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][4], callback_data=f"day_{data['days'][4]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][5], callback_data=f"day_{data['days'][5]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][6], callback_data=f"day_{data['days'][6]}_mon_{month}"),
        ],
        [
            InlineKeyboardButton(text=data["days"][7], callback_data=f"day_{data['days'][7]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][8], callback_data=f"day_{data['days'][8]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][9], callback_data=f"day_{data['days'][9]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][10], callback_data=f"day_{data['days'][10]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][11], callback_data=f"day_{data['days'][11]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][12], callback_data=f"day_{data['days'][12]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][13], callback_data=f"day_{data['days'][13]}_mon_{month}"),
        ],
        [
            InlineKeyboardButton(text=data["days"][14], callback_data=f"day_{data['days'][14]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][15], callback_data=f"day_{data['days'][15]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][16], callback_data=f"day_{data['days'][16]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][17], callback_data=f"day_{data['days'][17]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][18], callback_data=f"day_{data['days'][18]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][19], callback_data=f"day_{data['days'][19]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][20], callback_data=f"day_{data['days'][20]}_mon_{month}"),
        ],
        [
            InlineKeyboardButton(text=data["days"][21], callback_data=f"day_{data['days'][21]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][22], callback_data=f"day_{data['days'][22]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][23], callback_data=f"day_{data['days'][23]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][24], callback_data=f"day_{data['days'][24]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][25], callback_data=f"day_{data['days'][25]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][26], callback_data=f"day_{data['days'][26]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][27], callback_data=f"day_{data['days'][27]}_mon_{month}"),
        ],
        [
            InlineKeyboardButton(text=data["days"][28], callback_data=f"day_{data['days'][28]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][29], callback_data=f"day_{data['days'][29]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][30], callback_data=f"day_{data['days'][30]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][31], callback_data=f"day_{data['days'][31]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][32], callback_data=f"day_{data['days'][32]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][33], callback_data=f"day_{data['days'][33]}_mon_{month}"),
            InlineKeyboardButton(text=data["days"][34], callback_data=f"day_{data['days'][34]}_mon_{month}"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard