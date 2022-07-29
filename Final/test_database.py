import io
import sqlite3 as sql
import json
import faker
import random
import string
import re
from os import path
from PIL import Image

import datetime
import ciso8601
import sys

special_char = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
hotel_names = [
    "Lake Place", "Diamond", "Rubidi", "Samochy", "GoRo", "Hikoga",
    "Holly Good", "Raxle", "Ankani", "Wonder Koll"
]

# hotel_names = ["Mount Place", "Prism", "Hokaido", "Alaski", "Chill Home",
#                "Relax Spring", "Okaimi", "Rilax", "Glutami", "Amaze Koll", "Aquamarine Tower", "Northern Shrine", "Lord's Palms", "Emerald Lagoon", "Antique Legacy", "Prince's Bazaar", "Solar", "Amenity", "Grand", "Summit"]

DB = "./database.db"


def isExistTable(sqlConn: sql.Connection, table: str):
    if sqlConn:
        cx = sqlConn.cursor()
        # get name of table in database
        cx.execute("SELECT name FROM sqlite_master WHERE type = 'table';")

        rows = cx.fetchall()
        for row in rows:
            # convert tuple to string
            table_name = "".join(row)
            print(f"Table from SQL database: {table_name}")
            if table_name == table:
                return True
        return False
    else:
        return False


def deleteAll(table: str):
    try:
        sqlConn = sql.connect("sql.db")
        del_cmd = "DELETE FROM " + table + ";"
        cursor = sqlConn.cursor()

        cursor.execute(del_cmd)
        sqlConn.commit()
        sqlConn.close()
    except sql.Error as error:
        print(f"Error occured - {error}")
    finally:
        if sqlConn:
            sqlConn.close()
            print("SQLite connection closed")


def deleteTable(table: str):
    sqlConn = sql.connect(DB)
    cx = sqlConn.cursor()

    if isExistTable(sqlConn, table):
        del_cmd = "DROP TABLE " + table
        cx.execute(del_cmd)

    cx.close()
    sqlConn.commit()
    sqlConn.close()


def deleteUsernameInvalid(table: str):
    try:
        sqlConn = sql.connect(DB)
        cursor = sqlConn.cursor()
        cursor.execute("SELECT rowid, * FROM " + table)
        rows = cursor.fetchall()
        print(rows)
        for row in rows:
            if not isValidUsername(row[1]):
                print(row[0])
                del_cmd = "DELETE FROM " + table + \
                    " WHERE rowid = " + str(row[0])
                cursor.execute(del_cmd)
        sqlConn.commit()

    except sql.Error as error:
        print(f"Error occured - {error}")
    finally:
        if sqlConn:
            sqlConn.close()
            print("SQLite connection closed")


def insertIntoTable(name: str, password: str, bank: int):
    try:
        sqlConn = sql.connect("sql.db")

        cursor = sqlConn.cursor()
        print("Connect successfully")

        # cursor.execute(
        #     """CREATE TABLE test2(
        #     USERNAME TEXT,
        #     PASSWORD TEXT,
        #     BANK INTEGER
        # );"""
        # )
        data = (name, password, bank)
        insert_cmd = """INSERT INTO test
            VALUES (?, ?, ?);
        """
        cursor.execute(insert_cmd, data)
        # cursor.execute(
        #     """INSERT INTO test VALUES(
        #     'b','123','123456'
        # );"""
        # )
        sqlConn.commit()

        cursor.close()
    except sql.Error as error:
        print(f"Error occured - {error}")
    finally:
        if sqlConn:
            sqlConn.close()
            print("SQLite connection closed")


def isValidUsername(username: str):
    valid = True
    while valid:
        if len(username) < 5:
            valid = False
            break
        elif not re.search("[a-z]", username):
            valid = False
            break
        elif not re.search("[0-9]", username):
            valid = False
            break
        elif special_char.search(username) or re.search("[A-Z]", username):
            valid = False
            break
        else:
            break
    return valid
    # if (
    #     len(username) < 5
    #     or not re.search("[a-z]", username)
    #     or not re.search("[0-9]", username)
    # ):
    #     return False
    # return True


def genFakePassWord(length: int):
    characters = list(string.ascii_lowercase + string.digits)
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)


def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30, 38):
            s1 = ""
            for bg in range(40, 48):
                format = ";".join([str(style), str(fg), str(bg)])
                s1 += "\x1b[%sm %s \x1b[0m" % (format, format)
            print(s1)
        print("\n")


def get_all_data(table, json_str=False):
    conn = sql.connect(DB)
    conn.row_factory = sql.Row
    cx = conn.cursor()

    rows = cx.execute(f"SELECT * FROM {table}").fetchall()

    conn.commit()
    cx.close()

    if json_str:
        return json.dumps([dict(ix) for ix in rows])
    return rows


def insert_room(sqlConn: sql.Connection):
    cx = sqlConn.cursor()

    room_types = ["Single", "Double", "V.I.P"]
    descs = ["For 1 person", "For 2 people", "Best room"]

    vanc = 0
    price = 0
    pre_room_type = ""
    room_type = ""
    for i in range(10):
        pre_room_type = ""
        for _ in range(2):
            while room_type == pre_room_type:
                room_type = random.choice(room_types)

            vanc = random.randrange(10, 20, 1)
            if room_type == "Single":
                price = 100
                desc = descs[0]
            elif room_type == "Double":
                price = 200
                desc = descs[1]
            elif room_type == "V.I.P":
                price = 500
                desc = descs[2]
            room_data = (i + 1, room_type, desc, vanc, price)
            print(room_data)
            # print("a")
            insert_cmd = "INSERT INTO ROOM (HOTEL_ID, TYPE, DESC, VACANCIES, PRICE) VALUES (?,?,?,?,?)"
            cx.execute(insert_cmd, room_data)
            pre_room_type = room_type

    cx.close()
    sqlConn.commit()


def combine_room(sqlConn: sql.Connection):
    cx = sqlConn.cursor()

    for name in hotel_names:
        query = "select HOTEL.NAME, ROOM.* from HOTEL, ROOM where ROOM.HOTEL_ID = HOTEL.ID and HOTEL.NAME = '" + name + "'"
        cx.execute(query)
        rows = cx.fetchall()
        cx.execute(f"delete from ROOM where ID = '{rows[1][1]}'")
        rows_after = cx.fetchall()
        for row in rows:
            print(row)
        print("After")
        for row in rows_after:
            print(row)
        print("------")
    sqlConn.commit()
    cx.close()


# deleteAll()
# Generate data
# fake = faker.Faker()
# for i in range(1):
#     insertIntoTable(
#         fake.name(), genFakePassWord(5), random.randint(1000000000, 10000000000)
#     )
# -----------

# Manipulate data
# try:
#     sqlConn = sql.connect("sql.db")
#     sqlConn.row_factory = sql.Row

#     cursor = sqlConn.cursor()

#     cursor.execute("SELECT * FROM test WHERE USERNAME LIKE 'Melissa Williams'")
#     rows = cursor.fetchall()

#     for row in rows:
#         for i in row:
#             print(i)
#     sqlConn.commit()
# except sql.Error as error:
#     print(f"Error occured {error}")
# finally:
#     if sqlConn:
#         sqlConn.close()
#         print("SQLite connection closed")
# -----------

# Check table is exist or not
# try:
#     sqlConn = sql.connect("sql.db")
#     # sqlConn.row_factory = sql.Row
#     cursor = sqlConn.cursor()
#     cursor.execute("DROP TABLE test2")
#     cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
#     rows = cursor.fetchall()
#     print(rows)
#     for row in rows:
#             table_name = ''.join(row)
#             print(table_name)
# except sql.Error as error:
#     print(f"Error occured {error}")
# finally:
#     if sqlConn:
#         sqlConn.close()
#         print("SQLite connection closed")
# -----------

# deleteUsernameInvalid("USER")

try:
    sqlConn = sql.connect(DB)
    sqlConn.row_factory = sql.Row

    sqlConn.execute("PRAGMA foreign_keys=1")
    sqlConn.execute("PRAGMA auto_vacuum=1")

    cx = sqlConn.cursor()

    cx.execute("""CREATE TABLE IF NOT EXISTS USER
        (USERNAME TEXT PRIMARY KEY,
        PASSWORD TEXT NOT NULL,
        BANK INTEGER NOT NULL
        )
    """)

    # cx.execute("DROP TABLE HOTEL")
    cx.execute("""CREATE TABLE IF NOT EXISTS HOTEL
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        DESC TEXT,
        AVAILABLE INTEGER NOT NULL)
    """)

    # cx.execute("DROP TABLE ROOM")
    cx.execute("""CREATE TABLE IF NOT EXISTS ROOM
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        HOTEL_ID INTEGER NOT NULL,
        TYPE TEXT NOT NULL,
        DESC TEXT,
        VACANCIES INTEGER NOT NULL,
        PRICE INTEGER NOT NULL,
        FOREIGN KEY (HOTEL_ID) REFERENCES HOTEL(ID))
    """)

    cx.execute("""CREATE TABLE IF NOT EXISTS RESERVATION
        (TIMESTAMP TEXT NOT NULL,
        USERNAME TEXT NOT NULL,
        HOTEL_ID INTEGER NOT NULL,
        ROOM_ID INTEGER NOT NULL,
        QUALITY INTEGER NOT NULL,
        ARRIVAL TEXT NOT NULL,
        DEPARTURE TEXT NOT NULL,
        TOTAL INTEGER NOT NULL,
        FOREIGN KEY (USERNAME) REFERENCES USER(USERNAME),
        FOREIGN KEY (HOTEL_ID) REFERENCES HOTEL(ID),
        FOREIGN KEY (ROOM_ID) REFERENCES ROOM(ID)
        )
    """)

    # user = ("kn110", "123", "1234567890")
    # cx.execute("INSERT INTO USER VALUES (?, ?, ?)", user)

    # hotel = ("H1", "Hotel 1", "Normal", 10, 10, 100)
    # cx.execute("INSERT INTO HOTEL VALUES (?, ?, ?, ?, ?, ?)",  hotel)

    # str_today = datetime.datetime.now().replace(microsecond=0)
    # timestamp = datetime.datetime.timestamp(str_today)
    # # str_fromtimestamp = datetime.datetime.fromtimestamp(timestamp)
    # # print(str_today)
    # # print(timestamp)
    #
    # # insert_cmd = "INSERT INTO HOTEL (NAME, DESC, AVAILABLE) VALUES (?,?,?)"
    # # for name in hotel_names:
    # #     hotel = (name, "Choose me", 1)
    # #     cx.execute(insert_cmd, hotel)
    #
    # # insert_room(sqlConn)
    # # print("a")
    # # combine_room(sqlConn)
    #
    # # rows = cx.fetchall()
    # # for row in rows:
    # #     print(row)
    # insert_cmd = "insert into RESERVATION values (?, ?, ?, ?, ?, ?, ?, ?)"
    # arrival = "15/07/2022"
    # arrival_ts = datetime.datetime.strptime(arrival, "%d/%m/%Y").timestamp()
    # departure = "16/07/2022"
    # departure_ts = datetime.datetime.strptime(departure, "%d/%m/%Y").timestamp()
    # username = "kn110"
    # hotel_id = "2"
    # room_id = "3"
    # quality = 2
    # room = cx.execute(f"select * from ROOM where HOTEL_ID = {hotel_id} and ID = {room_id}").fetchone()
    # # #
    # # # update_cmd = f"""update ROOM
    # # # set VACANCIES = {room['VACANCIES'] - quality}
    # # # where HOTEL_ID = 1 and ID = 1
    # # # """
    # # # cx.execute(update_cmd)
    # # #
    # total = quality * room['PRICE']
    # reservation = (timestamp, username, hotel_id, room_id, quality, arrival_ts, departure_ts, total)
    # print(reservation)
    # cx.execute(insert_cmd, reservation)
    # cx.execute("""update ROOM set VACANCIES = 2 where ID = 1""")
    # print(arrival_ts, departure_ts)
    # cx.execute(f"""update RESERVATION set DEPARTURE = {str(departure_ts)} where TOTAL = 200""")

    # cx.execute("""alter table HOTEL
    # add column IMG blob;""")

    # for i in range(1, 11):
    #     path_img = f"./server/hotel{i} (Small).jpg"
    #     size_img = path.getsize(path_img)
    #     img = open(path_img, "rb")
    #     data = img.read(size_img)
    #     cx.execute(f"update HOTEL set IMG = (?) where ID = {i}", (data, ))
    #     print(path_img)
    #     img.close()
    # images = cx.execute("""select IMG from HOTEL""").fetchall()
    # for img in images:
    #     image = Image.open(io.BytesIO(img[0]))
    #     image.show()
    #     # input("Wait: ")

    # cx.execute("""alter table ROOM add column IMG blob;""")

    # for i in range(1, 22):
    #     path_img = f"./server/{i} (Small).jpg"
    #     size_img = path.getsize(path_img)
    #     img = open(path_img, "rb")
    #     data = img.read(size_img)
    #     cx.execute(f"update ROOM set IMG = (?) where ID = {i}", (data, ))
    #     img.close()

    # cx.execute(
    #     """update HOTEL
    #            set DESC = (?) where rowid = 10""",
    #     ("Wondel Koll, welcomes you in a real cosmopolitan, pulsing milieu, at the same time offering peace and intimate retirement, just in the heart of the city centre. Timeless elegance tailored for the demands of our time.",
    #      ))

    # cx.execute("""alter table RESERVATION add column NOTE text""")
    cx.execute("VACUUM")
    sqlConn.commit()
    cx.close()

except sql.Error as error:
    print(f"Error occurred {error}")
finally:
    if sqlConn:
        sqlConn.close()
        print("SQLite connection closed")
