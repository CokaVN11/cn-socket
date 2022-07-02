import socket

# Khai bao IP va Port
HOST = "127.0.0.1"
PORT = 65432

# AF_INET cho phép giao tiếp giữa các tiến trình trên những
# máy tính khác nhau trên mạng.
# SOCK_STREAM -> TCP
# SOCK_DGRAM -> UDP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)


print("Waiting for Client")
conn, addr = s.accept()

try:
    print("Connected by ", addr)
    
    # data = conn.recv(1024)
    # # if data == "":
    # #     print("Detect client close")
    # #     break
    # if len(data)> 0:
    #     print("Server recv: " + data.decode("utf8"))
    f = open("server_img.JPG", "wb")
    size_img = int(conn.recv(8).decode("utf-8"))
    print(size_img)

    data = None
    # while True:
    #     print("Receiving")
    #     tmp = conn.recv(1024)
    #     data = tmp
    #     while tmp:
    #         tmp = conn.recv(1024)
    #         data += tmp
    #     break
    print("Receiving")
    data = conn.recv(size_img)
    print("Received")
    f.write(data)
    f.close()
except KeyboardInterrupt:
    conn.close()
    # s.close()
finally:
    conn.close()
    # s.close()
