########## IMPORT, DÙNG TCP ##########

#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

"""
Now, we break our task :
- accepting new connections,
- broadcasting messages
- handling particular clients.
"""



# NÓ SẼ CHẠY LIÊN TỤC ĐỂ NHẬN CÁC KẾT NỐI,
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()

        # Khi kết nối được thì sẽ in thông tin kết nối
        print("%s:%s has connected." % client_address)

        # Rồi gửi thông báo welcome tới client
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        
        # Lưu lại địa chỉ kết nối của client vào addresses
        addresses[client] = client_address


        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    # Lưu tên client vào biến name
    name = client.recv(BUFSIZ).decode("utf8")
    
    # Gửi thông báo hướng dẫn khác tới bên đó
    #          Welcome %s với s là biến nội suy name để ở cuối
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))


    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))

    # Lưu lại tên vào clients
    clients[client] = name

    while True:

        # Nhận tin nhắn từ client
        msg = client.recv(BUFSIZ)

        # Nếu mà đây là tin nhắn bình thường (ko có thoát)
        # thì sẽ gửi tin nhắn đó cho các client khác
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else: # Nếu ngta thoát
            # Thì gửi lại thông báo tương tự cho client để nó đóng ứng dụng bên đó
            client.send(bytes("{quit}", "utf8"))

            # Sau đó tới bên server đóng kết nối với client đó
            # và xóa thông tin ng đó đi
            client.close()
            del clients[client]

            # Và báo cho những ng khác là người này đã thoát
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

# DÙNG ĐỂ GỬI MESSAGE TỚI TẤT CẢ CLIENT
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


########## SET UP SOME CONSTANTS ##########
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# Finally, we put in some code for starting
# our server and listening for incoming connections
if __name__ == "__main__":

    # Listens for 5 connections at max.
    SERVER.listen(5)
    print("Waiting for connection...")

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    
    # Starts the infinite loop.
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
