import gspread
from google.oauth2.service_account import Credentials
from Bot.function import home

scope = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(f'{home}/google_doc/cred.json')
client = gspread.authorize(credentials.with_scopes(scope))
# Открытие таблицы
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1_NhE6p260SB2P0Zo66sNuAvPsWD2GhGT1uqAM7HNOZc')


# №	id_user	full_name	birthdate	timezone	Height	weight	Address	PhoneEmail	front	behind	side_l	side_r	DataStart
def get_active_user() -> list[str]:
    """:return: список id активных пользователей"""
    worksheet = sheet.worksheet("active_user")
    values_list = worksheet.col_values(3)
    return values_list[1:]


def save_active_user(id_user, link_user) -> int:
    worksheet = sheet.worksheet("active_user")
    num_record = len(worksheet.get_all_values())
    list_row = [num_record, link_user, id_user]
    worksheet.append_row(list_row)
    return num_record





def get_id_responsible() -> list:
    worksheet = sheet.worksheet("responsible")
    values_list = worksheet.get_all_values()
    return values_list[1:]


def get_id_chat() -> list:
    worksheet = sheet.worksheet("chat")
    values_list = worksheet.get_all_values()
    return values_list[1:]


def get_record(num_record: int, name_list: str) -> list:
    worksheet = sheet.worksheet(name_list)
    data = worksheet.get_all_values()
    return data[num_record]


def save_tz(data: dict) -> int:
    worksheet = sheet.worksheet("TZ")
    num_record = len(worksheet.get_all_values())
    chats = " ".join([i[0] for i in data["chat"]])
    list_row = [num_record, data["id_photo"], data["text"], data["response"][0], data["response"][1], data["data"], chats]
    worksheet.append_row(list_row)
    return num_record

get_active_user()