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


def creat_list_calendar(month: int) -> dict:
    today = dt.date.today()
    "✖️"
    result = {"today": today,
              "days": [
                  "-", "-", "-", "-", "-", "-", "-",
                  "-", "-", "-", "-", "-", "-", "-",
                  "-", "-", "-", "-", "-", "-", "-",
                  "-", "-", "-", "-", "-", "-", "-",
                  "-", "-", "-", "-", "-", "-", "-"
              ],
              "back": "✖️✖️✖️",
              "next": ">>>"
              }
    day_start = dt.date(today.year, month, 1).weekday()
    k = 1
    d = 0
    for i in range(day_start, len(result["days"])):
        if today.day <= k and d < 14:
            result["days"][i] = str(k)
            d += 1
        k += 1
    if today.month < month:
        result["back"] = "<<<"
    return result
