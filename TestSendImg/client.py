import socket
import os

HOST = "127.0.0.1"  # IP adress server
PORT = 65432  # port is used by the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)

print("Client connect to server with port: " + str(PORT))
client.connect(server_address)

try:
    # msg = input("Client: ")
    size_img = os.path.getsize("Doggie_2.png")
    print(size_img)
    client.sendall(str(size_img).encode("utf-8"))
    f = open("Doggie_2.png", "rb") 
    data = f.read(size_img)
    print("Sending")
    client.sendall(data)
    print("Send finished")
    f.close()
    # client.sendall(b"This is the message from client")
except KeyboardInterrupt:
    client.close()
finally:
    client.close()

# Bat terminal -> Chay server -> Split code -> Chay client
