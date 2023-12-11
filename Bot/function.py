import os
import datetime as dt
home = os.path.dirname(__file__)  # Тут сохраняется путь до рабочей папки
admins = [1235360344]  # Список админов


def check_data(data_str: str) -> bool:
    try:
        data_list = [int(i) for i in data_str.split(".")]
        data = dt.date(data_list[-1], data_list[1], data_list[0])
        return True
    except (TypeError, ValueError):
        return False


def creat_list_calendar(in_data: dt.date) -> dict:
    today = dt.date.today()
    # today = dt.date(2023, 12, 22)
    stop_day = today + dt.timedelta(days=15)
    "✖️"
    result = {"days": [
                  "-", "-", "-", "-", "-", "-", "-",
                  "-", "-", "-", "-", "-", "-", "-",
                  "-", "-", "-", "-", "-", "-", "-",
                  "-", "-", "-", "-", "-", "-", "-",
                  "-", "-", "-", "-", "-", "-", "-"
              ],
              "back": "✖️✖️✖️",
              "next": "✖️✖️✖️"
              }
    day_start_month = dt.date(in_data.year, in_data.month, 1).weekday()
    k = 1
    for i in range(day_start_month, len(result["days"])):
        try:
            day = dt.date(in_data.year, in_data.month, k)
            if today < day and day < stop_day:
                result["days"][i] = str(k)
            k += 1
        except ValueError:
            continue
    if today.month < in_data.month:
        result["back"] = "<<<"
    if today.month > in_data.month:
        result["next"] = ">>>"
    return result
