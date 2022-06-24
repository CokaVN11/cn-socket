import sqlite3 as sql
import json
import faker
import random
import string
import re

special_char = re.compile("[@_!#$%^&*()<>?/\|}{~:]")


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


def deleteUsernameInvalid(table: str):
    try:
        sqlConn = sql.connect("sql.db")
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

# username = "Kn123"
# print(re.search("[a-z]", username))
# print(re.search("[0-9]", username))
# print(special_char.search(username))
# print(isValidUsername(username))
deleteAll("USER")
# print_format_table()
