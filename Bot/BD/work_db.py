import sqlite3
import datetime as dt

import Bot.function as fun


today = dt.date.today()
'%Y-%m-%d %H:%M:%S.%f'
tomorrow = dt.datetime.strftime(dt.datetime.now() + dt.timedelta(days=1), '%d.%m.%Y')


def get_id_all_user() -> list[int]:
    """:return: список id всех пользователей"""
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM main.all_user')
        list_id = cursor.fetchall()
        print(list_id)
        result = [i[0] for i in list_id]
    return result


def get_id_admin() -> list[int]:
    """:return: список id администраторов"""
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM main.admin')
        list_id = cursor.fetchall()
        result = [i[0] for i in list_id]
    return result


def check_activity_user(user_id: str) -> bool:
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM main.all_user')
        list_id = cursor.fetchall()
        dict_id = {}
        for i in list_id:
            dict_id[f'{i[0]}'] = i[2]
    try:
        return bool(dict_id[user_id])

    except KeyError:
        return False


def save_new_user(user_id: int, link: str):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        data = [user_id, link]
        cursor = connect.cursor()
        cursor.execute('SELECT EXISTS(SELECT * FROM all_user where user_id = $1)', [user_id])
        if bool(cursor.fetchall()[0][0]):
            return
        cursor.execute('INSERT INTO main.all_user (user_id, link) VALUES(?, ?);', data)


def get_notif_mess(time: str, num_day: int) -> list:
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'select {time}, type_file_{time} from main.notif_mess '
                       f'where num_day={num_day}')
        data = [i for i in cursor.fetchall()[0]]
        if data[0] == "":
            data[0] = None
        return data


def update_mess_notif(time: str, num_day: int, text: str, type_file: str):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        data = [text, type_file]
        cursor.execute(f'UPDATE main.notif_mess SET {time}=$1, type_file_{time}=$2 '
                       f'WHERE num_day={num_day}', data)


def update_activity_user(user_id: int):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'UPDATE main.all_user SET activity=1 '
                       f'WHERE user_id=$1', [user_id])


def save_data_user(user_id: int, data_dict: dict):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        data = [user_id, data_dict["full_name"], data_dict["birthday"], data_dict["timezone"],
                data_dict["height"], data_dict["weight"], data_dict["address"],
                data_dict["phone_email"], data_dict["data_start"]]
        cursor = connect.cursor()
        cursor.execute('INSERT INTO main.data_user '
                       '(user_id, full_name, birthday, timezone, height, weight, address, phone_email, data_start) '
                       'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);', data)


def get_data_user(user_id: int) -> dict:
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'select * from main.data_user where user_id=$1', [user_id])
        data_list = cursor.fetchall()[0]
        data_dict = {
            "user_id": data_list[0], "full_name": data_list[1], "birthday": data_list[2],
            "timezone": data_list[3], "height": data_list[4], "weight": data_list[5],
            "address": data_list[6], "phone_email": data_list[7], "data_start": data_list[8],
            "course_day": data_list[9]
        }
        return data_dict


def get_actual_mess(num_day: int):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'select * from main.notif_mess where num_day=$1',
                       [num_day])
        data_list = cursor.fetchall()[0]
        data_dict = {
            "num_day": data_list[0], "night": data_list[1], "morning": data_list[2],
            "day": data_list[3], "evening": data_list[4], "type_file_night": data_list[5],
            "type_file_morning": data_list[6], "type_file_day": data_list[7],
            "type_file_evening": data_list[8]
        }
        now_time = dt.datetime.today().time()
        if dt.time(5, 0, 0) > now_time:
            result = {"num_day": data_dict["num_day"], "text": data_dict["night"], "type": data_dict["type_file_night"]}
        elif dt.time(13, 0, 0) > now_time:
            result = {"num_day": data_dict["num_day"], "text": data_dict["morning"], "type": data_dict["type_file_morning"]}
        elif dt.time(21, 00, 00) > now_time:
            result = {"num_day": data_dict["num_day"], "text": data_dict["day"], "type": data_dict["type_file_day"]}
        else:
            result = {"num_day": data_dict["num_day"], "text": data_dict["evening"], "type": data_dict["type_file_evening"]}
        return result


def update_data_start(user_id: int, new_data: str):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'UPDATE main.data_user SET data_start=$1 '
                       f'WHERE user_id=$2', [new_data, user_id])
