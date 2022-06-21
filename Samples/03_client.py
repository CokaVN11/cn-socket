

#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
#https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            # Nhận tin về từ socket và decode ra luôn
            msg = client_socket.recv(BUFSIZ).decode("utf8")

            # Khi nhận được msg thì thêm vào danh sách msg
            # msg_list is basically a Tkinter feature
            # for displaying the list of messages on the screen.
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

# Lấy event làm đối số vì nó được Tkinter chuyển
# một cách ngầm định khi nhấn nút send trên GUI.
def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""

    # my_msg is the input field on the GUI
    # Lấy dữ liệu từ cái input field
    msg = my_msg.get()

    # Clears input field.
    my_msg.set("")

    # Gửi tin nhắn tới server
    # (Bên server sẽ boardcast tới các client khác)
    client_socket.send(bytes(msg, "utf8"))

    # Nếu cú pháp là thoát
    if msg == "{quit}":
        # thì đóng cổng
        client_socket.close()
        # và đóng GUI
        top.quit()

# This function will be called when we choose to close the GUI window
def on_closing(event=None):

    # Chỉnh cái input field thành {quit}
    my_msg.set("{quit}")
    # Rồi gửi
    send()


# Now we start building the GUI
top = tkinter.Tk()

# We start by defining the top-level widget and set its title
top.title("Chatter")

# Tạo cái frame chứa danh sách các tin nhắn
messages_frame = tkinter.Frame(top)

# Tạo biến my_msg là chuỗi để chứa dữ liệu trong input field
my_msg = tkinter.StringVar()  # For the messages to be sent.

# placeholder
my_msg.set("Type your messages here.")

# Tạo thanh cuộn để cuộ qua khung thông báo
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.


# Following will contain the messages.
# Danh sách tin nhắn sẽ lưu trong khung messages_frame
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)

# Rồi pack những các thành phần vào đúng vị trí
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

# Tạo cái input field để người nhập dữ liệu
# và gán dữ liệu đó cho biết my_msg đã tạo ở trên
entry_field = tkinter.Entry(top, textvariable=my_msg)
# We also bind it to the send() function so that
# whenever the user presses return, the message is sent to the server.
entry_field.bind("<Return>", send)
entry_field.pack()

# Tạo nút gửi - cũng bind với hàm send()
# khi ng dùng bấm vào thì gửi
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

# Khi người dùng muốn đóng cửa số GUI thì sẽ chạy hàm on_closing()
top.protocol("WM_DELETE_WINDOW", on_closing)


#----Now comes the sockets part----
# Hỏi cái Host với Port của người dùng
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000 # Default value
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
