import socket

HOST = "127.198.162.1"
PORT = 52314

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print(f"Connecting {server_address}")
client.connect(server_address)

try:
    while True:
        msg = input('Client: ')
        client.sendall(bytes(msg, "utf-8"))
except KeyboardInterrupt:
    client.close()
finally:
    client.close()