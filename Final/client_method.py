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
    "booking": "6",
    "cancel": "7"
}


def send_s(conn: socket.socket(), msg: str):
    if conn:
        conn.sendall(msg.encode(FORMAT))
        conn.recv(BUFSIZ)


def recv_s(conn: socket.socket()):
    if conn:
        msg = conn.recv(BUFSIZ)
        # print(msg)
        msg = msg.decode(FORMAT)
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

    for hotel in hotels:
        len_data = int(recv_s(client))
        hotel['IMG'] = client.recv(len_data)
        len_recv = len(hotel['IMG'])
        send_s(client, str(len_recv))

        while (len_recv != len_data):
            len_data = int(recv_s(client))
            hotel['IMG'] = client.recv(len_data)
            len_recv = len(hotel['IMG'])
            send_s(client, str(len_recv))

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

    for reserve in reservations:
        len_data = int(recv_s(client))
        reserve['IMG'] = client.recv(len_data)
        len_recv = len(reserve['IMG'])
        send_s(client, str(len_recv))

        while (len_recv != len_data):
            len_data = int(recv_s(client))
            reserve['IMG'] = client.recv(len_data)
            len_recv = len(reserve['IMG'])
            send_s(client, str(len_recv))
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

    for room in rooms:
        len_data = int(recv_s(client))
        room['IMG'] = client.recv(len_data)
        len_recv = len(room['IMG'])
        send_s(client, str(len_recv))

        while (len_recv != len_data):
            len_data = int(recv_s(client))
            room['IMG'] = client.recv(len_data)
            len_recv = len(room['IMG'])
            send_s(client, str(len_recv))

    return rooms


def GetMoneyStaying(arrival: str, depart: str, price: int):
    arrival = datetime.datetime.strptime(arrival, "%d/%m/%Y")
    depart = datetime.datetime.strptime(depart, "%d/%m/%Y")
    delta = depart - arrival
    return delta.days * price


def CanCancel(time_to_check: str):
    time_to_check = datetime.datetime.strptime(time_to_check,
                                               "%d/%m/%Y %H:%M:%S")
    time_now = datetime.datetime.now()
    delta = time_now - time_to_check
    if delta.days <= 1:
        return True
    return False


def Booking(client, username, booking_list, note_input):
    send_s(client, OPTIONS['booking'])
    send_s(client, username)
    rows = []

    for booking_room in booking_list:
        booking_room['Total'] = booking_room['Quantity'] * GetMoneyStaying(
            booking_room['Arrival'], booking_room['Depart'],
            booking_room['Price'])
        rows.append({
            "ID": booking_room['ID'],
            "Hotel Name": booking_room['Hotel Name'],
            "Room type": booking_room['Room type'],
            "Arrival": booking_room['Arrival'],
            "Depart": booking_room['Depart'],
            "Price": booking_room['Price'],
            "Quantity": booking_room['Quantity'],
            "Max": booking_room['Max'],
            "Total": booking_room['Total'],
            "Note": note_input
        })

    data = json.dumps(rows)
    send_s(client, str(len(data)))
    client.sendall(data.encode(FORMAT))

    # receive a message inform booking finish or fail
    msg = recv_s(client)
    return msg == "Finish"


def CancelReservation(client, username, hotel_id, room_id, time_stamp,
                      arrival_date, depart_date):
    send_s(client, OPTIONS['cancel'])
    send_s(client, username)
    send_s(client, str(hotel_id))
    send_s(client, str(room_id))
    send_s(client, time_stamp)
    send_s(client, arrival_date)
    send_s(client, depart_date)

    msg = recv_s(client)
    return msg == "Finish"


def GetStrNow():
    time_now = datetime.datetime.now().replace(
        microsecond=0).strftime("%d/%m/%Y %H:%M:%S")
    return time_now
