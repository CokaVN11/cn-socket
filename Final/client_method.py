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


def checkFieldValid(typeCheck, userInput):
    valid = True
    pop_up = ""
    if typeCheck == "username":
        if len(userInput) < 5:
            pop_up = "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)"
            valid = False
        elif not re.search("[a-z]", userInput):
            pop_up = "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)"
            valid = False
        elif not re.search("[0-9]", userInput):
            pop_up = "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)"
            valid = False
        elif not SPEC_CHAR.search(userInput) or re.search("[A-Z]", userInput):
            pop_up = "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)"
            valid = False
    elif typeCheck == "password":
        if len(userInput) < 3:
            pop_up = "Password must have at least 3 characters"
            valid = False

    elif typeCheck == "bank":
        if len(userInput) != 10:
            pop_up = "Bank account must have 10 characters and contain numbers (0-9)"
            valid = False
        elif not userInput.isnumeric():
            pop_up = "Bank account must have 10 characters and contain numbers (0-9)"
            valid = False
    return valid, pop_up


def Register(client, username, password, bank):
    send_s(client, "1")
    valid = True
    pop_up = ""
    input_dict = {'username': username, 'password': password, 'bank': bank}
    for field, userInput in input_dict.items():
        valid, tmp = checkFieldValid(field, userInput)
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
    send_s(client, "2")
    valid = True
    pop_up = ""
    valid_username = None
    # valid, pop_up = checkFieldValid("username", username)
    # valid, tmp = checkFieldValid("password", password)
    # pop_up += "\n" + tmp

    input_dict = {'username': username, 'password': password}
    for field, userInput in input_dict.items():
        valid, tmp = checkFieldValid(field, userInput)
        if pop_up != "":
            pop_up += "\n"
        pop_up += tmp

    if valid:
        send_s(client, username)
        send_s(client, password)
        print("[CLIENT] Send finished")
        msg = recv_s(client)
        if msg == "Oke":
            print("[CLIENT] Login successfully")
            valid_username = username
            pop_up = "Successfully"
        else:
            print("[CLIENT] You are a dump shit")
            pop_up = "Fail"

    return valid, pop_up, valid_username
