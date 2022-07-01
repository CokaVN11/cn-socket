import socket
import sqlite3

BUFSIZ = 1024
FORMAT = "utf-8"
QUIT_MSG = "!quit"
DB = "./database.db"

def send_s(conn: socket.socket(), msg: str):
    """Send a message and receive confirm"""
    if conn:
        conn.sendall(msg.encode(FORMAT))
        conn.recv(BUFSIZ)


def recv_s(conn: socket.socket()):
    """Receive a message and send confirm"""
    if conn:
        msg = conn.recv(BUFSIZ).decode(FORMAT)
        conn.sendall(msg.encode(FORMAT))
        return msg
    else:
        return None
    
def isExistTable(sqlConn: sqlite3.Connection, table: str):
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
    
def isNewUser(sqlConn: sqlite3.Connection, username: str, password: str, bank: int):
    if sqlConn:
        cx = sqlConn.cursor()
        # query = "SELECT * FROM " + table + " WHERE username LIKE '" + username + "'"
        query = f"select * from USER where USERNAME like '{username}'"
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
        insert_cmd = "INSERT INTO USER VALUES (?,?,?)"
        cx.execute(insert_cmd, data)
        sqlConn.commit()

        cx.close()