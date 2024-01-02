import sqlite3
import datetime as dt
import Bot.function as fun
from Bot.google_doc.googleSheets import save_data_user_sheet
today = dt.date.today()
'%Y-%m-%d %H:%M:%S.%f'
tomorrow = dt.datetime.strftime(dt.datetime.now() + dt.timedelta(days=1), '%d.%m.%Y')


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
    try:
        with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
            data = [user_id, link]
            cursor = connect.cursor()
            cursor.execute('SELECT EXISTS(SELECT * FROM all_user where user_id = $1)', [user_id])
            if bool(cursor.fetchall()[0][0]):
                return
            cursor.execute('INSERT INTO main.all_user (user_id, link) VALUES(?, ?);', data)
    except:
        pass


def save_data_user(user_id: int, data_dict: dict, user_name: str):
    save_data_user_sheet(user_name, data_dict)
    try:
        with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
            data = [user_id, data_dict["full_name"], data_dict["birthday"], data_dict["timezone"],
                    data_dict["height"], data_dict["weight"], data_dict["address"],
                    data_dict["phone"], data_dict["email"], data_dict["data_start"],
                    data_dict["photo"], data_dict["group_individual"]]
            cursor = connect.cursor()
            cursor.execute('INSERT INTO main.data_user '
                           '(user_id, full_name, birthday, timezone, height, weight, address, phone, email, '
                           'data_start, photo, group_individual) '
                           'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', data)
    except sqlite3.IntegrityError:
        data = [data_dict["full_name"], data_dict["birthday"], data_dict["timezone"],
                data_dict["height"], data_dict["weight"], data_dict["address"],
                data_dict["phone"], data_dict["email"], data_dict["data_start"],
                data_dict["photo"], data_dict["group_individual"], user_id]
        cursor.execute('UPDATE main.data_user '
                       'SET full_name=$1, birthday=$2, '
                       'timezone=$3, height=$4, weight=$5, '
                       'address=$6, phone=$7, email=$8, '
                       'data_start=$9, photo=$10, group_individual=$11 '
                       'WHERE user_id=$12', data)


def get_id_all_user() -> list[int]:
    """:return: список id всех пользователей"""
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM main.all_user')
        list_id = cursor.fetchall()
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


def get_notif_mess(time: str, num_day: int) -> list:
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'select {time}, type_file_{time} from main.notif_mess '
                       f'where num_day={num_day}')
        data = [i for i in cursor.fetchall()[0]]
        if data[0] == "":
            data[0] = None
        return data


def get_data_user(user_id: int) -> dict:
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'select * from main.data_user where user_id=$1', [user_id])
        data_list = cursor.fetchall()[0]
        data_dict = {
            "user_id": data_list[0], "full_name": data_list[1], "birthday": data_list[2],
            "timezone": data_list[3], "height": data_list[4], "weight": data_list[5],
            "address": data_list[6], "phone": data_list[7], "email": data_list[8],
            "data_start": data_list[9], "course_day": data_list[10], "mess_id": data_list[11],
            "photo": data_list[12], "group_individual": data_list[13]
        }
        return data_dict


def get_actual_mess(num_day: int):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'select * from main.notif_mess where num_day=$1',
                       [num_day])
        data_list = cursor.fetchall()[0]
        data_dict = {
            "num_day": data_list[0], "morning": data_list[1],
            "day": data_list[2], "type_file_morning": data_list[3],
            "type_file_day": data_list[4]
        }
        now_time = dt.datetime.today().time()
        if dt.time(13, 0, 0) > now_time:
            result = {"num_day": data_dict["num_day"], "text": data_dict["morning"], "type": data_dict["type_file_morning"]}
        elif dt.time(21, 00, 00) > now_time:
            result = {"num_day": data_dict["num_day"], "text": data_dict["day"], "type": data_dict["type_file_day"]}
        else:
            result = {"num_day": data_dict["num_day"],
                      "text": "Мы желаем Вам доброй ночи. Для лучшего прохождения курса рекомендуем Вам"
                "<a href='https://apps.apple.com/ru/app/%D0%BC%D0%BE-%D0%BC%D0%B5%D0%B4%D0%B8%D1%82%D0%B0%D1%86%D0%B8%D1%8F-%D0%B8-%D1%81%D0%BE%D0%BD/id1460803131'>"
                " скачать приложение </a>", "type": "text"}
        return result


def get_timezone_user(timezone: int) -> list:
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'select user_id from main.data_user where timezone=$1',
                       [timezone])
        data_list = [int(i) for i in cursor.fetchall()[0]]
        return data_list


def get_course_day_user(user_id: int) -> int:
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'select course_day from main.data_user where user_id=$1',
                       [user_id])
        data = cursor.fetchall()[0][0]
        return data


def get_activity_user() -> list:
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'select user_id from main.all_user where activity=2 or activity=1')
        data = [i[0] for i in cursor.fetchall()]
        return data


def update_mess_notif(time: str, num_day: int, text: str, type_file: str):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        data = [text, type_file]
        cursor.execute(f'UPDATE main.notif_mess SET {time}=$1, type_file_{time}=$2 '
                       f'WHERE num_day={num_day}', data)


def update_activity_user(user_id: int, state: int):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'UPDATE main.all_user SET activity=$1 '
                       f'WHERE user_id=$2', [state, user_id])


def update_data_start(user_id: int, new_data: str):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'UPDATE main.data_user SET data_start=$1 '
                       f'WHERE user_id=$2', [new_data, user_id])


def update_course_day(user_id: int, new_num_day: int):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'UPDATE main.data_user SET course_day=$1 '
                       f'WHERE user_id=$2', [new_num_day, user_id])


def update_mess_id_user(user_id: int, new_mess_id: str):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'UPDATE main.data_user SET mess_id=$1 '
                       f'WHERE user_id=$2', [new_mess_id, user_id])


def update_height_user(user_id: int, height: int):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'UPDATE main.data_user SET height=$1 '
                       f'WHERE user_id=$2', [height, user_id])


def update_weight_user(user_id: int, weight: int):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'UPDATE main.data_user SET weight=$1 '
                       f'WHERE user_id=$2', [weight, user_id])


def update_photo_user(user_id: int):
    with sqlite3.connect(f"{fun.home}/BD/main_data.db") as connect:
        cursor = connect.cursor()
        cursor.execute(f'UPDATE main.data_user SET photo=$1 '
                       f'WHERE user_id=$2', [1, user_id])
