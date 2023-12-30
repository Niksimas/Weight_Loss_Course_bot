from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)


def menu_admin() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Изменить информацию по дню", callback_data="edit_day_mess")],
        [InlineKeyboardButton(text="Запустить рассылку", callback_data="start_notif")],
        [InlineKeyboardButton(text="Отправить личное сообщение", callback_data="send_mess_user")],
        [InlineKeyboardButton(text="Просмотреть фотографии пользователя", callback_data="view_photo")],
        [InlineKeyboardButton(text="Изменить информацию групп. обучения", callback_data="edit_group_info")],
        [InlineKeyboardButton(text="В меню", callback_data="menu")]
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
        [InlineKeyboardButton(text="Утреннее сообщение (05:00)", callback_data=f"{num_day}_morning")],
        [InlineKeyboardButton(text="Дневное сообщение (13:00)", callback_data=f"{num_day}_day")],
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


def edit_info_group():
    buttons = [
        [InlineKeyboardButton(text="Ссылку", callback_data=f"edit_link")],
        [InlineKeyboardButton(text="Дату начала", callback_data=f"edit_date")],
        [InlineKeyboardButton(text="Назад", callback_data="cancel_a")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
