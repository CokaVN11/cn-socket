import sqlite3 as sql
import json
import faker
import random
import string


def deleteAll():
    try:
        sqlConn = sql.connect("sql.db")
        del_cmd = """DELETE FROM test;"""
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


def genFakePassWord(length: int):
    characters = list(string.ascii_lowercase + string.digits)
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)


# deleteAll()
# Generate data
fake = faker.Faker()
for i in range(1):
    insertIntoTable(
        fake.name(), genFakePassWord(5), random.randint(1000000000, 10000000000)
    )
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
try:
    sqlConn = sql.connect("sql.db")
    # sqlConn.row_factory = sql.Row
    cursor = sqlConn.cursor()
    cursor.execute("DROP TABLE test2")
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    rows = cursor.fetchall()
    print(rows)
    for row in rows:
            table_name = ''.join(row)
            print(table_name)
except sql.Error as error:
    print(f"Error occured {error}")
finally:
    if sqlConn:
        sqlConn.close()
        print("SQLite connection closed")
# -----------