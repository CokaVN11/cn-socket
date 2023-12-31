import socket
import sqlite3
import string
from threading import Thread

HOST = socket.gethostbyname(socket.gethostname())
PORT = 52314
BUFSIZE = 1024
FORMAT = "utf-8"
addr = {}
clients = {}

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
SERVER.bind(server_address)


def send_safe(conn: socket.socket(), msg):
    """Send msg to the host and receive the response

    Args:
        conn (socket.socket): socket to the host
        msg (str): message to send
    """
    if conn:
        conn.send(msg.encode(FORMAT))
        conn.recv(BUFSIZE)


def recv_safe(conn: socket.socket()):
    """Receive msg from the host and send back

    Args:
        conn (socket.socket): socket to the host

    Returns:
        str or None: message received
    """
    if conn:
        msg = conn.recv(BUFSIZE).decode(FORMAT)
        conn.send(msg.encode(FORMAT))
        return msg
    else:
        return None


def isExistTable(sqlConn: sqlite3.Connection, table: str):
    """
    It checks if a table exists in a database

    :param sqlConn: sqlite3.Connection
    :type sqlConn: sqlite3.Connection
    :param table: the name of the table you want to check
    :type table: str
    :return: A boolean value.
    """
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
    """
    It creates a table if it doesn't exist, then inserts a row into the table

    :param sqlConn: sqlite3.Connection
    :type sqlConn: sqlite3.Connection
    :param table: The name of the table you want to insert the user into
    :type table: str
    :param name: str
    :type name: str
    :param password: str
    :type password: str
    :param bank: int
    :type bank: int
    """
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
    """
    If the username is not in the table, add it to the table

    :param sqlConn: sqlite3.Connection
    :type sqlConn: sqlite3.Connection
    :param table: the table name
    :type table: str
    :param username: str
    :type username: str
    :param password: str
    :type password: str
    :param bank: int
    :type bank: int
    :return: A boolean value.
    """
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


def Register(socConn: socket.socket(), sqlConn: sqlite3.Connection):
    """
    It receives a username, password and bank from the client, and then checks if the user is new or
    not. If the user is new, it sends "Oke" to the client, otherwise it sends "Not oke".

    :param socConn: socket.socket()
    :type socConn: socket.socket()
    :param sqlConn: sqlite3.Connection
    :type sqlConn: sqlite3.Connection
    :return: The username, password, and bank.
    """
    username = recv_safe(conn)
    password = recv_safe(conn)
    bank = int(recv_safe(conn))

    print("alo")
    if username and password and bank:
        print("Received")
        if isNewUser(sqlConn, "USER", username, password, bank):
            conn.sendall("Oke".encode("utf-8"))
        else:
            conn.sendall("Not oke".encode("utf-8"))
    return (username, password, bank)


def Login(socConn: socket.socket(), sqlConn: sqlite3.Connection):
    """
    It receives a username and password from the client, checks if the username exists in the database,
    and if it does, it checks if the password is correct. If it is, it sends "Oke" to the client,
    otherwise it sends "Not oke".

    :param socConn: socket.socket()
    :type socConn: socket.socket()
    :param sqlConn: sqlite3.Connection
    :type sqlConn: sqlite3.Connection
    :return: The username and password of the user that is logged in.
    """
    username = recv_safe(conn)
    password = recv_safe(conn)
    if username and password:
        print("Received")
        cursor = sqlConn.cursor()
        query = "SELECT * FROM " + "USER" + " WHERE username LIKE '" + username + "'"
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) == 0:
            conn.sendall("Not oke".encode("utf-8"))
            return None, None
        for row in rows:
            print(row)
            if row[1] == password:
                conn.sendall("Oke".encode("utf-8"))
            else:
                conn.sendall("Not oke".encode("utf-8"))
                return None, None
        return (username, password)


def handle_client(client: socket.socket()):
    """Handles a single client connection"""
    name = recv_safe(client)

    welcome = f"Welcome {name}! If you ever want to quit, type '{quit}' to exit."
    send_safe(client,welcome)

    clients[client] = name
    with client:
        choice = None
        while choice != "{quit}":
            choice = recv_safe(client)
            if choice.isdigit():
                if int(choice) == 1:
                    print("Registing")
                    username, password, bank = Register(client, sqlConn)
                    print(username, password, bank)
                if int(choice) == 2:
                    print("Logining")
                    username, password = Login(client, sqlConn)
                    print(username, password)
            else:
                print(choice)
        client.close()
        del clients[client]


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_addr = SERVER.accept()
        print(f"{client_addr} has connected.")

        send_safe(client, "Welcome to my CAVE")
        addr[client] = client_addr

        Thread(target=handle_client, args=(client,)).start()


sqlConn = sqlite3.connect("sql.db")

# with sqlite3.connect("sql.db") as sqlConn:
if __name__ == "__main__":

    SERVER.listen(5)  # 5 is number of client want to connect to server
    print("Waiting for connection...")

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)

    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
