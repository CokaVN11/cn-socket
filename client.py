import socket
import re

IP = socket.gethostbyname(socket.gethostname())
PORT = 27276
ADDR = (IP, PORT)
BUFSIZ = 1024
FORMAT = "utf-8"
QUIT_MSG = "!quit"
SPEC_CHAR = re.compile("[@_!#$%^&*()<>?/\|}{~:]")


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


def isValidUsername(username: str):
    """Checking whether username is valid or not."""
    valid: bool = True
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
        elif SPEC_CHAR.search(username) or re.search("[A-Z]", username):
            valid = False
            break
        else:
            break
    return valid


def ShowMenu():
    print("\x1b[1;34;40m" + "------MENU------" + "\x1b[0m")
    task = ["Register", "Login", "Booking", "Look up", "Cancel"]
    for i in range(len(task)):
        print(f"{i+1}. {task[i]}")
    print("----------------")

def Register(client):
    username = input("Username: ")
    password = input("Password: ")
    bank = int(input("Bank number: "))
    while not isValidUsername(username):
        username = input("Pls type 'Username' again: ")
    while not len(password) >= 3:
        password = input("Pls type 'Password' again: ")
    while not 1000000000 <= bank <= 10000000000:
        bank = int(input("Pls type 'Bank number' again: "))
    send_s(client, username)
    send_s(client, password)
    send_s(client, str(bank))
    print("[CLIENT] Send finished")
    msg = recv_s(client)
    if msg == "Oke":
        print("[Client] Register successfully")
    else: print("[CLIENT] You are a dump shit")


def Login(client):
    username = input("Username: ")
    password = input("Password: ")
    while not isValidUsername(username):
        username = input("Please type 'Username' again: ")
    while not len(password) >= 3:
        password = input("Please type 'Password' again: ")

    send_s(client, username)
    send_s(client, password)
    print("[CLIENT] Send finished")
    msg = recv_s(client)
    if msg == "Oke": 
        print("[CLIENT] Login successfully")
    else:
        print("[CLIENT] You are a dump shit")


def Menu(client, choice):
    if type(choice) != int:
        choice = int(choice)
    if choice == 1:
        Register(client)
    elif choice == 2:
        Login(client)


def main():
    print("\x1b[1;32;40m" + "CLIENT SIDE" + "\x1b[0m")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connected = True
    while connected:
        ShowMenu()
        msg = input("> ")

        send_s(client, msg)

        if msg == QUIT_MSG:
            connected = False
        else:
            if msg.isdigit():
                Menu(client, msg)
            else: 
                msg = recv_s(client)
                print(f"[SERVER] {msg}")
    client.close()


if __name__ == "__main__":
    main()
