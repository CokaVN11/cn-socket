from cgitb import text
from tkinter import *
from turtle import left, window_height

# Base constants
windowWidth = 800
windowHeight = 500
entryWidth = 60

# Init window frame
window = Tk()
window.title('E-Booking')
window.geometry(str(windowWidth) + 'x' + str(windowHeight))

screenMode = 1

def clearScreen(self = window):
    for widget in self.place_slaves():
        widget.place_forget()

def changeMode(self):
    if self.text == "Sign up":
        return 2

def welcomeScreen():


    welcomeLabel = Label(window, font=(1), text="WELCOME !", height=6)
    welcomeLabel.place(anchor=CENTER, x = (windowWidth/2), y = ((windowHeight/2) - 80))

    loginButton = Button(window, text="Log in", font=(1), width=15, height=2, command=clearScreen)
    signupButton = Button(window, text="Sign up", font=(1), width=15, height=2)
    loginButton.place(anchor=E, x = ((windowWidth/2) - 30), y = (windowHeight/2))
    signupButton.place(anchor=W, x = ((windowWidth/2) + 30), y = (windowHeight/2))


def registerScreen():
    registerLabel = Label(window, font=(1), text="REGISTER", height=6)
    registerLabel.place(anchor=CENTER, x = (windowWidth/2), y = ((windowHeight/2) - 120))

    usernameLabel = Label(window, text="Username")
    usernameLabel.place(anchor=E, x = ((windowWidth/2) - (entryWidth*2)), y = ((windowHeight/2) - 100))
    usernameEntry = Entry(window, width=(entryWidth))
    usernameEntry.place(anchor=CENTER, x = (windowWidth/2), y = ((windowHeight/2) - 80))
    
    passwordLabel = Label(window, text="Password")
    passwordLabel.place(anchor=E, x = ((windowWidth/2) - (entryWidth*2) - 2), y = ((windowHeight/2) - 50))
    passwordEntry = Entry(window, width=(entryWidth))
    passwordEntry.place(anchor=CENTER, x = (windowWidth/2), y = ((windowHeight/2) - 30))

    bankAccountLabel = Label(window, text="Bank Account")
    bankAccountLabel.place(anchor=E, x = ((windowWidth/2) - (entryWidth*2) + 20), y = ((windowHeight/2) - 0))
    bankAccountEntry = Entry(window, width=(entryWidth))
    bankAccountEntry.place(anchor=CENTER, x = (windowWidth/2), y = ((windowHeight/2) + 20))


    submitButton = Button(window, text="Submit", font=(1), width=15, height=1)
    submitButton.place(anchor=CENTER, x = (windowWidth/2), y = ((windowHeight/2) + 70))



# while True:
#     if screenMode == 1:
#         welcomeScreen()
#     if screenMode == 2:
#         registerScreen()

registerScreen()









# #Tạo một Textbox
# txt = Entry(window,width=10)
# #Vị trí xuất hiện của Textbox
# txt.grid(column=1, row=0)

# #Đặt vị trí con trỏ tại Textbox
# txt.focus()

# #Hàm xử lý khi nút được nhấn
# def clicked():
#     res = "Welcome to " + txt.get()
#     lbl.configure(text= res)

# btn = Button(window, text="Click Me", command=clicked)
# btn.grid(column=1, row=2)




window.mainloop()


# - Cach tao placeholder cho messages_frame
