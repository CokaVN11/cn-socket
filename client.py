import socket
import re

HOST = "127.198.162.1"
PORT = 52314
BUZSIZE = 1024
special_char = re.compile("[@_!#$%^&*()<>?/\|}{~:]")

def ShowMenu():
    print("MENU")
    task = ["Register", "Login", "Booking", "Look up", "Cancel"]
    for i in range(len(task)):
        print(f"{i+1}. {task[i]}")



def isValidUsername(username: str):
    valid = True
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
        elif special_char.search(username) or re.search("[A-Z]", username):
            valid = False
            break
        else:
            break
    return valid


def Register():
    username = input("Username: ")
    password = input("Password: ")
    bank = int(input("Bank number: "))
    while not isValidUsername(username):
        username = input("Pls type 'Username' again: ")
    while not len(password) >= 3:
        password = input("Pls type 'Password' again: ")
    while not 1000000000 <= bank <= 10000000000:
        bank = int(input("Pls type 'Bank number' again: "))
    client.sendall(username.encode("utf-8"))
    client.recv(BUZSIZE)
    client.sendall(password.encode("utf-8"))
    client.recv(BUZSIZE)
    client.sendall(str(bank).encode("utf-8"))
    client.recv(BUZSIZE)
    print("Send finished")
    rep = client.recv(BUZSIZE).decode("utf-8")
    if rep == "Oke":
        return 1
    return 0
    # return (username, password, bank)

def Login():
    username = input("Username: ")
    password = input("Password: ")
    while not isValidUsername(username):
        username = input("Pls type 'Username' again: ")
    while not len(password) >= 3:
        password = input("Pls type 'Password' again: ")

    client.sendall(username.encode("utf-8"))
    client.recv(BUZSIZE)
    client.sendall(password.encode("utf-8"))
    client.recv(BUZSIZE)
    print("Send finished")
    rep = client.recv(BUZSIZE).decode("utf-8")
    return rep == "Oke"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print("CLIENT SIDE\n")
print(f"Connecting {server_address}")
client.connect(server_address)

try:
    ShowMenu()
    msg = ""
    while msg != "{quit}":
        msg = input("Client: ")
        if msg.isdigit():
            if int(msg) == 1:
                print("Registing")
                client.sendall(msg.encode("utf-8"))
                if Register() == 1:
                    print("Register successfully")
                else: print("Register fail")
            if int(msg) == 2:
                print("Logining")
                client.sendall(msg.encode("utf-8"))
                if Login() == 1:
                    print("Welcome to my show")
                else: print("Get out")
        else:
            client.sendall(bytes(msg, "utf-8"))
except KeyboardInterrupt:
    client.close()
finally:
    client.close()
