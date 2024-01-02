import gspread
from google.oauth2.service_account import Credentials

from Bot.function import home

scope = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(f'{home}/google_doc/cred.json')
client = gspread.authorize(credentials.with_scopes(scope))
# Открытие таблицы
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1ak1yng-lThA3RZ9886wKl6qRBZ-bp32MdtRf4TtT4l8/edit?usp=sharing')


# №	id_user	full_name	birthdate	timezone	Height	weight	Address	PhoneEmail	front	behind	side_l	side_r	DataStart
def save_data_user_sheet(user_name, data: dict) -> int:
    worksheet = sheet.worksheet("users")
    num_record = len(worksheet.get_all_values())
    if data["photo"]:
        photo = "Загружены"
    else:
        photo = "Не загружены"
    try:
        list_row = [num_record, user_name, data['user_id'], data["full_name"], data["birthday"],
                    data["timezone"], data["height"], data["weight"], data["address"], data["phone"],
                    data["email"], data["data_start"], photo, data["group_individual"]]
    except KeyError:
        list_row = [num_record, user_name, data['user_id'], data["full_name"], data["birthday"],
                    data["timezone"], data["height"], data["weight"], data["address"], data["phone"],
                    data["email"], data["data_start"], photo, data["group_individual"]]
    worksheet.append_row(list_row)
    return num_record
