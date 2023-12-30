import os
import datetime as dt
home = os.path.dirname(__file__)


def check_data(data_str: str) -> bool:
    try:
        data_list = [int(i) for i in data_str.split(".")]
        data = dt.date(data_list[-1], data_list[1], data_list[0])
        if data <= dt.date.today()-dt.timedelta(5110):
            return True
        return False
    except:
        return False


def creat_list_calendar(in_data: dt.date) -> dict:
    today = dt.date.today()+dt.timedelta(days=1)
    stop_day = today + dt.timedelta(days=30)
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
            if today <= day and day < stop_day:
                result["days"][i] = str(k)
            k += 1
        except ValueError:
            continue
    if in_data >= stop_day:
        result["back"] = "<<<"
    if in_data < stop_day:
        result["next"] = ">>>"
    return result


def adding_month(input_date: dt.date) -> dt.date:
    try:
        new_data = dt.date(input_date.year, input_date.month+1, 1)
    except ValueError:
        new_data = dt.date(input_date.year+1, 1, 1)
    return new_data


def subtracting_month(input_date: dt.date) -> dt.date:
    try:
        new_data = dt.date(input_date.year, input_date.month-1, 1)
    except ValueError:
        new_data = dt.date(input_date.year-1, 12, 1)
    return new_data
