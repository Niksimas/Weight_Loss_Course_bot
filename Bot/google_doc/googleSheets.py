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


def get_all_user() -> list[str]:
    """:return: список id всех пользователей"""
    worksheet = sheet.worksheet("all_user")
    values_list = worksheet.col_values(1)
    return values_list


def save_new_user(id_user) -> int:
    worksheet = sheet.worksheet("all_user")
    num_record = len(worksheet.get_all_values())
    worksheet.append_row([id_user])
    return num_record


def get_admin() -> list[str]:
    """:return: список id администраторов"""
    worksheet = sheet.worksheet("admins")
    values_list = worksheet.col_values(2)
    return values_list[1:]


def save_active_user(id_user, link_user) -> int:
    worksheet = sheet.worksheet("active_user")
    num_record = len(worksheet.get_all_values())
    list_row = [num_record, link_user, id_user]
    worksheet.append_row(list_row)
    return num_record


def save_data_user(id_user, data: dict) -> int:
    worksheet = sheet.worksheet("data_user")
    num_record = len(worksheet.get_all_values())
    try:
        #     №	id_user	full name	birthday	timezone	Height	weight	Address	PhoneEmail	photo front	photo behind	side l	side r	DataStart
        list_row = [num_record, id_user, data["full_name"], data["birthday"],
                    data["tz"], data["height"], data["weight"], data["address"], data["phone_email"],
                    data["photo1"], data["photo2"], data["photo3"], data["photo4"],
                    data["data_start"]]
    except KeyError:
        list_row = [num_record, id_user, data["full_name"], data["birthday"],
                    data["tz"], data["height"], data["weight"], data["address"], data["phone_email"],
                    "", "", "", "", data["data_start"]]
    worksheet.append_row(list_row)
    return num_record
