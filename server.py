import socket

HOST = "127.198.162.1"
PORT = 52314

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
s.bind(server_address)
s.listen(1) # 1 is number of client want to connect to server
print("Waiting for connection\n");

conn, addr = s.accept()

try:
    print(f"Connect by {addr}")
    while conn:
        data = conn.recv(1024)
        if data:
            print(data.decode("utf-8"))
except KeyboardInterrupt():
    conn.close()
finally:
    conn.close()