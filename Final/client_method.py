import datetime
import socket
import re
import json

IP = socket.gethostbyname(socket.gethostname())
PORT = 27278
ADDR = (IP, PORT)
BUFSIZ = 1024
FORMAT = "utf-8"
QUIT_MSG = "!quit"
SPEC_CHAR = re.compile("[@_!#$%^&*()<>?/|}{~:]")
OPTIONS = {
    "register": "1",
    "login": "2",
    "hotel_list": "3",
    "reservation": "4",
    "lookup": "5",
    "booking": "6"
}


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


def checkFieldValid(type_check, user_input):
    valid = True
    pop_up = ""
    if type_check == "username":
        if len(user_input) < 5:
            pop_up = "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)"
            valid = False
        elif not re.search('[a-z]', user_input):
            pop_up = "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)"
            valid = False
        elif not re.search('[0-9]', user_input):
            pop_up = "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)"
            valid = False
        elif SPEC_CHAR.search(user_input) or re.search('[A-Z]', user_input):
            # print("special char")
            pop_up = "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)"
            valid = False
    elif type_check == "password":
        if len(user_input) < 3:
            pop_up = "Password must have at least 3 characters"
            valid = False

    elif type_check == "bank":
        if len(user_input) != 10:
            pop_up = "Bank account must have 10 characters and contain numbers (0-9)"
            valid = False
        elif not user_input.isnumeric():
            pop_up = "Bank account must have 10 characters and contain numbers (0-9)"
            valid = False
    # print(valid, pop_up)
    return valid, pop_up


def Register(client, username, password, bank):
    send_s(client, OPTIONS["register"])
    valid = True
    # cur_valid = True
    pop_up = ""

    input_dict = {"username": username, "password": password, "bank": bank}
    for field, userInput in input_dict.items():
        cur_valid, tmp = checkFieldValid(field, userInput)
        if not cur_valid:
            valid = cur_valid
        if pop_up != "":
            pop_up += "\n"
        pop_up += tmp
    if valid:
        send_s(client, username)
        send_s(client, password)
        send_s(client, str(bank))
        print("[CLIENT] Send finished")
        msg = recv_s(client)
        if msg == "Oke":
            print("[CLIENT] Register successfully")
            pop_up = "Successfully"
        else:
            print("[CLIENT] You are a dump shit")
            pop_up = "Fail"
    return valid, pop_up


def Login(client, username, password):
    send_s(client, OPTIONS["login"])
    valid = True
    pop_up = ""
    valid_username = None

    input_dict = {"username": username, "password": password}
    for field, userInput in input_dict.items():
        cur_valid, tmp = checkFieldValid(field, userInput)
        if not cur_valid:
            valid = cur_valid
        if pop_up != "":
            pop_up += "\n"
        pop_up += tmp

    bank = ""
    if valid:
        send_s(client, username)
        send_s(client, password)
        print("[CLIENT] Send finished")
        msg = recv_s(client)
        if msg == "Oke":
            print("[CLIENT] Login successfully")
            valid_username = username
            bank = recv_s(client)
            pop_up = "Successfully"
        else:
            print("[CLIENT] You are a dump shit")
            pop_up = "Fail"

    return valid, pop_up, valid_username, bank


def ShowHotelList(client):
    send_s(client, OPTIONS['hotel_list'])
    len_data = int(recv_s(client))
    data = client.recv(len_data)
    if data == b'empty':
        return
    hotels = json.loads(data)
    # first = True
    # for hotel in hotels:
    #     if not first:
    #         print("-" * 10)
    #     else:
    #         first = False
    #     print(f"ID: {hotel['ID']}")
    #     print(f"Name: {hotel['NAME']}")
    #     print(f"Description: {hotel['DESC']}")
    #     print(f"Is available: {hotel['AVAILABLE']}")
    return hotels


def ShowBooked(client, username):
    send_s(client, OPTIONS['reservation'])
    send_s(client, username)
    len_data = int(recv_s(client))
    data = client.recv(len_data)
    if data == b'empty':
        print("empty")
        return
    reservations = json.loads(data)
    # first = True
    # for reserve in reservations:
    #     if not first:
    #         print("-"*10)
    #     else:
    #         first = False
    #     print(f"Time: {reserve['TIMESTAMP']}")
    #     print(f"Hotel: {reserve['NAME']}")
    #     print(f"Room type: {reserve['TYPE']}")
    #     print(f"Arrival day: {reserve['ARRIVAL']}")
    #     print(f"Departure day: {reserve['DEPARTURE']}")
    #     print(f"Quantity: {reserve['QUALITY']}")
    #     print(f"Price: {reserve['PRICE']}")
    #     print(f"Total price: {reserve['TOTAL']}")
    return reservations


def LookUpRoom(client, hotel_name, arrival_date, depart_date):
    if arrival_date is None and depart_date is None:
        return None
    send_s(client, OPTIONS['lookup'])
    send_s(client, hotel_name)
    send_s(client, arrival_date)
    send_s(client, depart_date)

    len_data = int(recv_s(client))
    data = client.recv(len_data)
    if data == b'empty':
        print("empty")
        return []
    rooms = json.loads(data)

    return rooms


def GetMoneyStaying(arrival: str, depart: str, price: int):
    arrival = datetime.datetime.strptime(arrival, "%d/%m/%Y")
    depart = datetime.datetime.strptime(depart, "%d/%m/%Y")
    delta = depart - arrival
    return delta.days * price


def CanCancel(time_to_check: str):
    time_to_check = datetime.datetime.strptime(time_to_check, "%d/%m/%Y %H:%M:%S")
    time_now = datetime.datetime.now()
    delta = time_now - time_to_check
    if delta.days <= 1:
        return True
    return False


def Booking(client, username, room_id, quantity, arrival, departure, total):
    send_s(client, OPTIONS['booking'])
    send_s(client, username)
    send_s(client, str(room_id))
    send_s(client, str(quantity))
    send_s(client, arrival)  # send a str of %d/%m/%Y
    send_s(client, departure)  # send a str of %d/%m/%Y
    send_s(client, str(total))

    # receive a message inform booking finish or fail
    msg = recv_s(client)
    return msg == "Finish"


def GetStrNow():
    time_now = datetime.datetime.now().replace(microsecond=0).strftime("%d/%m/%Y %H:%M:%S")
    return time_now
