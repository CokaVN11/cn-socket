import socket
import sqlite3
import string

HOST = "127.198.162.1"
PORT = 52314
BUZSIZE = 1024


def isExistTable(sqlConn: sqlite3.Connection, table: str):
    with sqlConn:
        cursor = sqlConn.cursor()
        # get name of table in database
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")

        rows = cursor.fetchall()
        for row in rows:
            # convert tuple to string
            table_name = "".join(row)
            print(table_name)
            if table_name == table:
                return True
        return False


def insertUserIntoTable(
    sqlConn: sqlite3.Connection, table: str, name: str, password: str, bank: int
):
    with sqlConn:
        cursor = sqlConn.cursor()
        print("Connect successfully")
        create_table = (
            "CREATE TABLE IF NOT EXISTS "
            + table
            + "(username TEXT, password TEXT, bank INTEGER)"
        )
        cursor.execute(create_table)

        data = (name, password, bank)
        insert_cmd = "INSERT INTO " + table + " VALUES (?, ?, ?)"
        cursor.execute(insert_cmd, data)
        sqlConn.commit()

        cursor.close()


def isNewUser(
    sqlConn: sqlite3.Connection, table: str, username: str, password: str, bank: int
):
    with sqlConn:
        cursor = sqlConn.cursor()
        query = "SELECT * FROM " + table + " WHERE username LIKE '" + username + "'"
        cursor.execute(query)
        rows = cursor.fetchall()
        row_count = len(rows)
        if row_count:
            return False
        insertUserIntoTable(sqlConn, table, username, password, bank)
        return True
        # print(rows)


def Register(socConn: socket.socket()):
    username = socConn.recv(BUZSIZE)
    socConn.sendall(username)
    password = socConn.recv(BUZSIZE)
    socConn.sendall(password)
    bank = socConn.recv(BUZSIZE)
    socConn.sendall(bank)
    username = username.decode("utf-8")
    password = password.decode("utf-8")
    bank = int(bank.decode("utf-8"))
    print("alo")
    if username and password and bank:
        print("Received")
        with sqlite3.connect("sql.db") as sqlConn:
            if isNewUser(sqlConn, "USER", username, password, bank):
                conn.sendall("Oke".encode("utf-8"))
            else:
                conn.sendall("Not oke".encode("utf-8"))
    return (username, password, bank)


# with sqlite3.connect("sql.db") as sqlConn:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
s.bind(server_address)
s.listen(1)  # 1 is number of client want to connect to server
print("Waiting for connection")
try:
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    choice = None
    while choice != "{quit}":
        choice = conn.recv(1024).decode("utf-8")
        if choice.isdigit():
            if int(choice) == 1:
                print("Registing")
                username, password, bank = Register(conn)
                print(username, password, bank)
        else:
            print(choice)
except KeyboardInterrupt:
    conn.close()
finally:
    conn.close()
