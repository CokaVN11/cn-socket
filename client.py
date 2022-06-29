import socket
import re
import pickle
import json

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


def ShowLoginPage():
    print("------MENU------")
    task = ["Register", "Login"]
    for i in range(len(task)):
        print(f"{i+1}. {task[i]}")
    print("----------------")


def ShowMenu():
    print("------MENU------")
    task = ["Show hotel", "Show had booked", "Booking guide", "Logout"]
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
    else:
        print("[CLIENT] You are a dump shit")


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
        return username
    else:
        print("[CLIENT] You are a dump shit")
        return None


def ShowHotelList(client):
    len_data = int(recv_s(client))
    data = client.recv(len_data)
    if data == b'empty':
        return
    hotels = json.loads(data)
    first = True
    for hotel in hotels:
        if not first:
            print("-"*10)
        else:
            first = False
        print(f"ID: {hotel['ID']}")
        print(f"Name: {hotel['NAME']}")
        print(f"Description: {hotel['DESC']}")
        print(f"Is available: {hotel['AVAILABLE']}")


def ShowBooked(client, username):
    send_s(client, username)
    len_data = int(recv_s(client))
    data = client.recv(len_data)
    if data == b'empty':
        print("empty")
        return
    reservations = json.loads(data)
    first = True
    for reserv in reservations:
        if not first:
            print("-"*10)
        else: first = False
        print(f"Hotel: {reserv['NAME']}")
        print(f"Room type: {reserv['TYPE']}")
        print(f"Arrival day: {reserv['ARRIVAL']}")
        print(f"Departure day: {reserv['DEPARTURE']}")
        print(f"Quantity: {reserv['QUALITY']}")
        print(f"Total price: {reserv['TOTAL']}")


def LoginPage(client, choice):
    if type(choice) != int:
        choice = int(choice)
    send_s(client, str(choice))
    if choice == 1:
        Register(client)
        return False, None
    elif choice == 2:
        return True, Login(client)


def Menu(client, choice, username):
    if type(choice) != int:
        choice = int(choice)
    send_s(client, str(choice + 2))
    if choice == 1:
        print("Show hotel list")
        ShowHotelList(client)
        return True
    elif choice == 2:
        print("Do you book me")
        ShowBooked(client, username)
        return True
    elif choice == 3:
        print("How to book me")
        return True
    elif choice == 4:
        print("You are so amazing")
        return False


def main():
    print("CLIENT SIDE")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connected = True
    logined = False
    username = None
    while connected:
        if not logined:
            ShowLoginPage()
        else:
            ShowMenu()
        msg = input("> ")
        if msg == QUIT_MSG:
            send_s(client, msg)
            connected = False
        else:
            if msg.isdigit():
                if not logined:
                    logined, username = LoginPage(client, msg)
                else:
                    logined = Menu(client, msg, username)
                    # username = None
            else:
                send_s(client, msg)
                msg = recv_s(client)
                print(f"[SERVER] {msg}")
    client.close()


if __name__ == "__main__":
    main()
