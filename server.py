import socket
import sqlite3
import string
import threading
import json
import sys
import datetime

IP = socket.gethostbyname(socket.gethostname())
PORT = 27276
ADDR = (IP, PORT)
BUFSIZ = 1024
FORMAT = "utf-8"
QUIT_MSG = "!quit"
DB = "./database.db"


def send_s(conn: socket.socket(), msg: str):
    if conn:
        conn.sendall(msg.encode(FORMAT))
        conn.recv(BUFSIZ)


def recv_s(conn: socket.socket()):
    if conn:
        msg = conn.recv(BUFSIZ).decode(FORMAT)
        conn.sendall(msg.encode(FORMAT))
        return msg
    else:
        return None

# def send_list(conn: socket.socket(), msgs: list):
#     for msg in msgs:
#         packet = pickle.dumps(msg)
#         conn.sendall(packet)


def isExistTable(sqlConn: sqlite3.Connection, table: str):
    """
    It checks if a table exists in a database

    :param sqlConn: sqlite3.Connection
    :type sqlConn: sqlite3.Connection
    :param table: the name of the table you want to check
    :type table: str
    :return: A boolean value.
    """
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


def isNewUser(sqlConn: sqlite3.Connection, table: str, username: str, password: str, bank: int):
    if sqlConn:
        cx = sqlConn.cursor()
        query = "SELECT * FROM " + table + " WHERE username LIKE '" + username + "'"
        cx.execute(query)
        rows = cx.fetchall()
        row_count = len(rows)
        if row_count:
            return False
        return True
    else:
        return None


def insertUserIntoTable(sqlConn: sqlite3.Connection, name: str, password: str, bank: int):
    if sqlConn:
        cx = sqlConn.cursor()
        create_table = """CREATE TABLE IF NOT EXISTS USER
        (USERNAME TEXT PRIMARY KEY,
        PASSWORD TEXT NOT NULL,
        BANK INTEGER NOT NULL)"""

        cx.execute(create_table)

        data = (name, password, bank)
        insert_cmd = "INSERT INTO " + table + " VALUES (?,?,?)"
        cx.execute(insert_cmd, data)
        sqlConn.commit()

        cx.close()


def Login(conn, addr, sqlConn: sqlite3.Connection):
    if conn:
        username = recv_s(conn)
        password = recv_s(conn)
        if username and password:
            print(f"[SERVER] Received from {addr}")
            print(f"[{addr}] username = {username}, password = {password}")
        cx = sqlConn.cursor()
        query = "SELECT * FROM " + "USER" + " WHERE username LIKE '" + username + "'"
        cx.execute(query)
        rows = cx.fetchall()
        if len(rows) == 0:
            send_s(conn, "Not oke")
        for row in rows:
            if row[1] == password:
                send_s(conn, "Oke")
            else:
                send_s(conn, "Not oke")
        cx.close()
        return username, password


def Register(conn, addr, sqlConn: sqlite3.Connection):
    if conn:
        username = recv_s(conn)
        password = recv_s(conn)
        bank = int(recv_s(conn))
        if username and password and bank:
            print(f"[SERVER] Received from {addr}")
            print(
                f"[{addr}] username = {username}, password = {password}, bank number = {bank}")
            if isNewUser(sqlConn, "USER", username, password, bank):
                insertUserIntoTable(sqlConn, "USER", username, password, bank)
                send_s(conn, "Oke")
            else:
                send_s(conn, "Not oke")


def SendHotelList(conn, addr, sqlConn: sqlite3.Connection):
    if conn:
        sqlConn.row_factory = sqlite3.Row
        cx = sqlConn.cursor()

        rows = cx.execute("select * from HOTEL").fetchall()

        # print(type(rows))

        if len(rows) != 0:
            data = json.dumps([dict(ix) for ix in rows])
            print(f"Length of data sent: {len(data)}")
            send_s(conn, str(len(data)))
            conn.sendall(data.encode(FORMAT))
            # conn.sendall(data)
        else:
            data = "empty"
            send_s(conn, str(len(data)))
            conn.sendall(data.encode(FORMAT))

        cx.close()


def SendBookedList(conn, addr, sqlConn: sqlite3.Connection):
    if conn:
        username = recv_s(conn)
        sqlConn.row_factory = sqlite3.Row
        cx = sqlConn.cursor()

        cx.execute(
            f"""select HOTEL.NAME, ROOM.TYPE, RESERVATION.QUALITY, RESERVATION.ARRIVAL, RESERVATION.DEPARTURE, RESERVATION.TOTAL 
            from RESERVATION, HOTEL, ROOM 
            where RESERVATION.USERNAME = '{username}' and 
            RESERVATION.HOTEL_ID = HOTEL.ID and
            RESERVATION.ROOM_ID = ROOM.ID""")

        rows = [dict(row) for row in cx]

        # print(rows)

        if len(rows) != 0:
            for row in rows:
                # print(type(row['ARRIVAL']))
                row['ARRIVAL'] = datetime.datetime.fromtimestamp(
                    float(row['ARRIVAL'])).strftime("%d/%m/%Y")
                row['DEPARTURE'] = datetime.datetime.fromtimestamp(
                    float(row['DEPARTURE'])).strftime("%d/%m/%Y")
                # print(type(row['ARRIVAL']))
                # print(row)
            data = json.dumps([dict(ix) for ix in rows])
            send_s(conn, str(len(data)))
            conn.sendall(data.encode(FORMAT))

        else:
            data = "empty"
            send_s(conn, str(len(data)))
            conn.sendall(data.encode(FORMAT))

        cx.close()


def NavigateChoice(conn, addr, sqlConn: sqlite3.Connection, choice):
    if type(choice) != int:
        choice = int(choice)
    if choice == 1:
        print(f"[{addr}] Registing")
        Register(conn, addr, sqlConn)
    elif choice == 2:
        print(f"[{addr}] Loginning")
        Login(conn, addr, sqlConn)
    elif choice == 3:
        print(f"[{addr}] Want to get hotel list")
        SendHotelList(conn, addr, sqlConn)

    elif choice == 4:
        print(f"[{addr}] Want to get booked room")
        SendBookedList(conn, addr, sqlConn)
    elif choice == 5:
        print(f"[{addr}] Booking guide")
    elif choice == 6:
        print(f"[{addr}] Logouting")


def handle_client(conn, addr, sqlConn: sqlite3.Connection):
    """
    It handle client

    :param conn: The connection object
    :param addr: The address of the client
    """
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = recv_s(conn)
        if msg == QUIT_MSG:
            print(f"[{addr}] Getting out of server")
            connected = False
        else:
            if msg.isdigit():
                NavigateChoice(conn, addr, sqlConn, int(msg))
            else:
                print(f"[{addr}] sent {msg}")
                send_s(conn, msg)

    conn.close()


def accept_incoming_connection(server):
    """
    It accepts incoming connections and creates a new thread for each connection

    :param server: The server object
    """
    while True:
        conn, addr = server.accept()
        sqlConn = sqlite3.connect(DB, check_same_thread=False)
        thread = threading.Thread(
            target=handle_client, args=(conn, addr, sqlConn))

        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    accept_thread = threading.Thread(
        target=accept_incoming_connection, args=(server,))

    accept_thread.start()
    accept_thread.join()  # prevent another thread start when it not finished
    server.close()


if __name__ == "__main__":
    main()
