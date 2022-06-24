import socket
import re

HOST = "127.198.162.1"
PORT = 52314
BUFSIZE = 1024
FORMAT = "utf-8"
special_char = re.compile("[@_!#$%^&*()<>?/\|}{~:]")

def send_safe(conn: socket.socket(), msg):
    """
    If the connection is valid, send the message and wait for a response
    
    :param conn: socket.socket()
    :type conn: socket.socket()
    :param msg: the message to send
    """
    if conn:
        conn.send(msg.encode(FORMAT))
        conn.recv(BUFSIZE)

def recv_safe(conn: socket.socket()):
    """
    It receives a message from the client, sends it back to the client, and returns the message
    
    :param conn: socket.socket()
    :type conn: socket.socket()
    :return: The message that was sent to the server.
    """
    if conn:
        msg = conn.recv(BUFSIZE).decode(FORMAT)
        conn.send(msg.encode(FORMAT))
        return msg
    else: return None

def ShowMenu():
    print("MENU")
    task = ["Register", "Login", "Booking", "Look up", "Cancel"]
    for i in range(len(task)):
        print(f"{i+1}. {task[i]}")

def isValidUsername(username: str):
    """ Checking whether username is valid or not."""
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
        elif special_char.search(username) or re.search("[A-Z]", username):
            valid = False
            break
        else:
            break
    return valid


def Register():
    """
    It asks for a username, password and bank number, then it checks if the username, password, bank number is valid
    If all of these are true, it sends the username, password and bank number to the server.
    :return: a boolean value
    """
    username = input("Username: ")
    password = input("Password: ")
    bank = int(input("Bank number: "))
    isValidUsername(username)
    while not isValidUsername(username):
        username = input("Pls type 'Username' again: ")
    while not len(password) >= 3:
        password = input("Pls type 'Password' again: ")
    while not 1000000000 <= bank <= 10000000000:
        bank = int(input("Pls type 'Bank number' again: "))
    send_safe(client, username)
    send_safe(client, password)
    send_safe(client, str(bank))
    print("Send finished")
    rep = recv_safe(client)
    if rep == "Oke":
        return 1
    return 0
    # return (username, password, bank)

def Login():
    """
    It asks for a username and password, and then sends them to the server
    :return: A boolean value
    """
    username = input("Username: ")
    password = input("Password: ")
    while not isValidUsername(username):
        username = input("Pls type 'Username' again: ")
    while not len(password) >= 3:
        password = input("Pls type 'Password' again: ")

    send_safe(client, username)
    send_safe(client, password)
    print("Send finished")
    rep = client.recv(BUFSIZE).decode("utf-8")
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
                # client.sendall(msg.encode(FORMAT))
                send_safe(client, msg)
                if Register() == 1:
                    print("Register successfully")
                else: print("Register fail")
            if int(msg) == 2:
                print("Logining")
                # client.sendall(msg.encode(FORMAT))
                send_safe(client, msg)
                if Login() == 1:
                    print("Welcome to my show")
                else: print("Get out")
        else:
            # client.sendall(bytes(msg, FORMAT))
            send_safe(client, msg)
except KeyboardInterrupt:
    client.close()
finally:
    client.close()
