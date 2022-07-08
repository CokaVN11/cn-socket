import socket
import sqlite3
import threading
import json
import datetime

IP = socket.gethostbyname(socket.gethostname())
PORT = 27278
ADDR = (IP, PORT)
BUFSIZ = 1024
FORMAT = "utf-8"
QUIT_MSG = "!quit"
DB = "./database.db"
OPTIONS = {
    "register": "1",
    "login": "2",
    "hotel_list": "3",
    "reservation": "4",
    "lookup": "5",
    "booking": "6",
    "cancel": "7"
}


def send_s(conn: socket.socket(), msg: str):
    if conn:
        conn.sendall(msg.encode(FORMAT))
        conn.recv(BUFSIZ)


def recv_s(conn: socket.socket()):
    if conn:
        msg = conn.recv(BUFSIZ).decode(FORMAT)
        print(msg)
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

    param sqlConn: sqlite3.Connection
    type sqlConn: sqlite3.Connection
    param table: the name of the table you want to check
    type table: str
    return: A boolean value.
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


def isNewUser(sqlConn: sqlite3.Connection, table: str, username: str):
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


def insertUserIntoTable(
        sqlConn: sqlite3.Connection, name: str, password: str, bank: int
):
    if sqlConn:
        cx = sqlConn.cursor()
        create_table = """CREATE TABLE IF NOT EXISTS USER
        (USERNAME TEXT PRIMARY KEY,
        PASSWORD TEXT NOT NULL,
        BANK INTEGER NOT NULL)"""

        cx.execute(create_table)

        data = (name, password, bank)
        insert_cmd = "INSERT INTO USER VALUES (?,?,?)"
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
        # query = "SELECT * FROM " + "USER" + " WHERE username LIKE '" + username + "'"
        query = f"select * from USER where username like '{username}'"
        cx.execute(query)
        rows = cx.fetchall()
        if len(rows) == 0:
            send_s(conn, "Not oke")
        for row in rows:
            if row[1] == password:
                send_s(conn, "Oke")
                send_s(conn, str(row[2]))
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
                f"[{addr}] username = {username}, password = {password}, bank number = {bank}"
            )
            if isNewUser(sqlConn, "USER", username):
                insertUserIntoTable(sqlConn, username, password, bank)
                send_s(conn, "Oke")
            else:
                send_s(conn, "Not oke")


def SendHotelList(conn, addr, sqlConn: sqlite3.Connection):
    if conn:
        print(f"{addr} Get Hotel List")
        sqlConn.row_factory = sqlite3.Row
        cx = sqlConn.cursor()

        cx.execute("select * from HOTEL")

        rows = []
        images = []

        for row in cx:
            rows.append(dict(ID=row['ID'], NAME=row['NAME'], DESC=row['DESC'], AVAILABLE=row['AVAILABLE']))
            images.append(row['IMG'])

        # print(type(rows))

        if len(rows) != 0:
            data = json.dumps([dict(ix) for ix in rows])
            print(f"Length of data sent: {len(data)}")
            send_s(conn, str(len(data)))
            conn.sendall(data.encode(FORMAT))
            for img in images:
                len_data = len(img)
                print(len_data)
                send_s(conn, str(len_data))
                conn.sendall(img)
            # conn.sendall(data)
        else:
            data = "empty"
            send_s(conn, str(len(data)))
            conn.sendall(data.encode(FORMAT))

        cx.close()


def SendBookedList(conn, addr, sqlConn: sqlite3.Connection):
    if conn:
        print(f"{addr} Get reservations")
        username = recv_s(conn)
        sqlConn.row_factory = sqlite3.Row
        cx = sqlConn.cursor()

        cx.execute(
            f"""select RESERVATION.TIMESTAMP, HOTEL.NAME, RESERVATION.HOTEL_ID, RESERVATION.ROOM_ID, ROOM.TYPE, ROOM.PRICE, ROOM.VACANCIES, ROOM.IMG,
            RESERVATION.QUALITY, RESERVATION.ARRIVAL, RESERVATION.DEPARTURE, RESERVATION.TOTAL 
            from RESERVATION, HOTEL, ROOM 
            where RESERVATION.USERNAME = '{username}' and 
            RESERVATION.HOTEL_ID = HOTEL.ID and
            RESERVATION.ROOM_ID = ROOM.ID"""
        )

        rows = []
        images = []

        for row in cx:
            rows.append(dict(TIMESTAMP=row['TIMESTAMP'], NAME=row['NAME'], HOTEL_ID=row['HOTEL_ID'], ROOM_ID=row['ROOM_ID'],
                             TYPE=row['TYPE'], PRICE=row['PRICE'], VACANCIES=row['VACANCIES'],
                             QUANTITY=row['QUALITY'], ARRIVAL=row['ARRIVAL'], DEPARTURE=row['DEPARTURE'], TOTAL=row['TOTAL']))
            images.append(row['IMG'])

        # print(rows)

        if len(rows) != 0:
            for row in rows:
                # print(type(row['ARRIVAL']))
                row["TIMESTAMP"] = datetime.datetime.fromtimestamp(
                    float(row["TIMESTAMP"])
                ).strftime("%d/%m/%Y %H:%M:%S")
                row["ARRIVAL"] = datetime.datetime.fromtimestamp(
                    float(row["ARRIVAL"])
                ).strftime("%d/%m/%Y")
                row["DEPARTURE"] = datetime.datetime.fromtimestamp(
                    float(row["DEPARTURE"])
                ).strftime("%d/%m/%Y")
                # print(type(row['ARRIVAL']))
                # print(row)
            data = json.dumps([dict(ix) for ix in rows])
            send_s(conn, str(len(data)))
            conn.sendall(data.encode(FORMAT))

            for img in images:
                len_data = len(img)
                send_s(conn, str(len_data))
                conn.sendall(img)

        else:
            data = "empty"
            send_s(conn, str(len(data)))
            conn.sendall(data.encode(FORMAT))

        cx.close()


def isNotInOtherDatetime(arrival: datetime.datetime, departure: datetime.datetime,
                         arrival_check: datetime.datetime, departure_check: datetime.datetime):
    if departure < arrival_check < departure_check:
        return True
    if arrival > departure_check > arrival_check:
        return True

    return False


def SendRoomList(conn, addr, sqlConn: sqlite3.Connection):
    if conn:
        print(f"{addr} Look up room list")
        sqlConn.row_factory = sqlite3.Row
        cx = sqlConn.cursor()

        hotel_name = recv_s(conn)
        arrival_date = recv_s(conn)
        depart_date = recv_s(conn)

        # ---Convert to datetime---
        arrival_date = datetime.datetime.strptime(arrival_date, "%d/%m/%Y")
        depart_date = datetime.datetime.strptime(depart_date, "%d/%m/%Y")

        # print(hotel_name, type(arrival_date), depart_date)
        cx.execute(f"""select ROOM.ID, ROOM.TYPE, ROOM.DESC, ROOM.VACANCIES, ROOM.PRICE, ROOM.BED, ROOM.AREA, ROOM.GUEST, ROOM.IMG
                      from HOTEL, ROOM
                      where HOTEL.NAME = '{hotel_name}' and HOTEL.ID = ROOM.HOTEL_ID""")
        rooms = []
        images = []

        for row in cx:
            rooms.append(dict(ID=row['ID'], TYPE=row['TYPE'], DESC=row['DESC'], VACANCIES=row['VACANCIES'],
                         PRICE=row['PRICE'], BED=row['BED'], AREA=row['AREA'], GUEST=row['GUEST']))
            images.append(row['IMG'])

        cx.execute("""select RESERVATION.ROOM_ID, RESERVATION.QUALITY, RESERVATION.ARRIVAL, RESERVATION.DEPARTURE
                      from RESERVATION, HOTEL
                      where RESERVATION.HOTEL_ID = HOTEL.ID""")
        reservations = [dict(row) for row in cx]

        if len(rooms) == 0:
            data = "empty"
            send_s(conn, str(len(data)))
            conn.sendall(data.encode(FORMAT))
        else:
            for reserve in reservations:
                reserve['ARRIVAL'] = datetime.datetime.fromtimestamp(float(reserve['ARRIVAL']))
                reserve['DEPARTURE'] = datetime.datetime.fromtimestamp(float(reserve['DEPARTURE']))
                # print(reserve['ARRIVAL'], reserve['DEPARTURE'])

            for room, reserve in zip(rooms, reservations):
                if room['ID'] == reserve['ROOM_ID']:
                    if not isNotInOtherDatetime(reserve['ARRIVAL'], reserve['DEPARTURE'], arrival_date, depart_date):
                        room['VACANCIES'] -= reserve['QUALITY']

            # print(rooms)
            # print(reservations)
            data = json.dumps([dict(ix) for ix in rooms])
            send_s(conn, str(len(data)))
            conn.sendall(data.encode(FORMAT))
            for img in images:
                send_s(conn, str(len(img)))
                conn.sendall(img)
        cx.close()


def BookingRoom(conn, sqlConn: sqlite3.Connection):
    if conn:
        sqlConn.row_factory = sqlite3.Row
        cx = sqlConn.cursor()

        username = recv_s(conn)
        len_data = int(recv_s(conn))
        data = conn.recv(len_data)
        booking_list = json.loads(data)

        timestamp = datetime.datetime.now().replace(microsecond=0).timestamp()
        insert_cmd = "insert into RESERVATION values (?, ?, ?, ?, ?, ?, ?, ?)"
        for booking in booking_list:
            booking["Arrival"] = datetime.datetime.strptime(booking["Arrival"], "%d/%m/%Y").timestamp()
            booking["Depart"] = datetime.datetime.strptime(booking["Depart"], "%d/%m/%Y").timestamp()

            hotel_id = cx.execute(f"select HOTEL_ID from ROOM where ID = {booking['ID']}").fetchone()
            if hotel_id is None:
                send_s(conn, "Fail")
                cx.close()
                return
            else:
                hotel_id = hotel_id['HOTEL_ID']

            cx.execute(insert_cmd, (timestamp, username, hotel_id, booking['ID'], booking['Quantity'],
                                    booking['Arrival'], booking['Depart'], booking['Total']))

        sqlConn.commit()
        send_s(conn, "Finish")
        cx.close()


def CancelReservation(conn, sqlConn: sqlite3.Connection):
    if conn:
        username = recv_s(conn)
        hotel_id = recv_s(conn)
        room_id = recv_s(conn)
        timestamp = recv_s(conn)
        arrival_date = recv_s(conn)
        depart_date = recv_s(conn)

        timestamp = datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S").timestamp()
        arrival_date = datetime.datetime.strptime(arrival_date, "%d/%m/%Y").timestamp()
        depart_date = datetime.datetime.strptime(depart_date, "%d/%m/%Y").timestamp()

        cx = sqlConn.cursor()

        query = f"""select rowid, * from RESERVATION where TIMESTAMP = '{timestamp}'
        and USERNAME = '{username}'
        and ROOM_ID = {room_id}
        and HOTEL_ID = {hotel_id}
        and ARRIVAL = '{arrival_date}'
        and DEPARTURE = '{depart_date}'"""

        reservation = cx.execute(query).fetchone()

        if reservation is None:
            send_s(conn, "Fail")
            cx.close()
            return
        cx.execute(f"delete from RESERVATION where rowid = {reservation['rowid']}")

        send_s(conn, "Finish")
        sqlConn.commit()

        cx.close()


def NavigateChoice(conn, addr, sqlConn: sqlite3.Connection, choice):
    if choice == OPTIONS["register"]:
        print(f"[{addr}] Registering")
        Register(conn, addr, sqlConn)
    elif choice == OPTIONS["login"]:
        print(f"[{addr}] Logining")
        Login(conn, addr, sqlConn)
    elif choice == OPTIONS["hotel_list"]:
        print(f"[{addr}] Want to get hotel list")
        SendHotelList(conn, addr, sqlConn)
    elif choice == OPTIONS["reservation"]:
        print(f"[{addr}] Want to get booked room")
        SendBookedList(conn, addr, sqlConn)
    elif choice == OPTIONS["lookup"]:
        # print(f"[{addr}] Booking guide")
        SendRoomList(conn, addr, sqlConn)
    elif choice == OPTIONS["booking"]:
        print(f"[{addr}] Booking room")
        BookingRoom(conn, sqlConn)
    elif choice == OPTIONS["cancel"]:
        print(f"[{addr}] Cancel reservation")
        CancelReservation(conn, sqlConn)


def handle_client(conn, addr, sqlConn: sqlite3.Connection):
    """
    It handles client

    param conn: The connection object
    param addr: The address of the client
    param sqlConn: The connection to sql database
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
                NavigateChoice(conn, addr, sqlConn, msg)
            else:
                print(f"[{addr}] sent {msg}")
                send_s(conn, msg)

    conn.close()


def accept_incoming_connection(server):
    """
    It accepts incoming connections and creates a new thread for each connection

    param server: The server object
    """
    while True:
        conn, addr = server.accept()
        sqlConn = sqlite3.connect(DB, check_same_thread=False)
        thread = threading.Thread(target=handle_client, args=(conn, addr, sqlConn))

        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    accept_thread = threading.Thread(target=accept_incoming_connection, args=(server,))

    accept_thread.start()
    accept_thread.join()  # prevent another thread start when it is not finished
    server.close()


if __name__ == "__main__":
    main()
