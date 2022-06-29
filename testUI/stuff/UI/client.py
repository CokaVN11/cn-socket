
from tkinter import *
from tkinter import messagebox


window = Tk()

window.geometry("800x500")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 500,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

#==================== Constants Declaration ====================#
EntryHeight = 36
EntryDiscrepancy = 8   # Độ chênh lệch cần cộng vào y sau khi render


#==================== Image Declaration ====================#
# Tên biến : [Screen]_{Name}{Number}{Purpose}
Login_Background = PhotoImage(file = "./assets/Login_Background.png")
Login_Entry = PhotoImage(file = "./assets/Login_Entry.png")
Login_LoginButton = PhotoImage(file = "./assets/Login_LoginButton.png")
Login_SignupButton = PhotoImage(file = "./assets/Login_SignupButton.png")

Signup_Background = PhotoImage(file = "./assets/Signup_Background.png")
Signup_BackButton = PhotoImage(file = "./assets/Signup_BackButton.png")
Signup_SubmitButton = PhotoImage(file = "./assets/Signup_SubmitButton.png")
Signup_Entry = PhotoImage(file = "./assets/Signup_Entry.png")


#==================== Implement Function ====================#
    
def clearScreen(self = window):
    for widget in self.place_slaves():
        widget.place_forget()


def LoginScreen():
    clearScreen()

    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 500,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    # Background
    LoginBackground = canvas.create_image(
        365.0, 250.0,
        image=Login_Background
    )

    #---------- Entry Username
    LoginEntry1Background = canvas.create_image(
        600.0, 166.0,
        image = Login_Entry
    )

    LoginEntry1 = Entry(
        bd = 0,
        bg = "#ffffff",
        highlightthickness = 0,
        font=("20")
    )
    LoginEntry1.place(
        x = 458.0, y = 141 + EntryDiscrepancy,
        width = 284.0,
        height = EntryHeight
    )

    #---------- Entry Password
    LoginEntry2Background = canvas.create_image(
        600.0, 260.0,
        image = Login_Entry
    )

    LoginEntry2 = Entry(
        bd = 0,
        bg = "#ffffff",
        highlightthickness = 0,
        font=("20")
    )
    LoginEntry2.place(
        x = 458.0, y = 235 + EntryDiscrepancy,
        width = 284.0,
        height = EntryHeight
    )

    def submitLogin():
        usernameInput = LoginEntry1.get()
        passwordInput = LoginEntry2.get()
        print(usernameInput, passwordInput)

    #---------- BUTTON "Log in"
    LoginLoginButton = Button(
        image = Login_LoginButton,
        borderwidth = 0,
        highlightthickness = 0,
        command = submitLogin,
        relief = "flat"
    ).place(
        x = 450, y = 326,
        width = 300,
        height = 50
    )

    #---------- BUTTON "Create one"
    LoginSignupButton = Button(
        image = Login_SignupButton,
        borderwidth = 0,
        highlightthickness = 0,
        command = SignupScreen,
        relief = "flat"
    ).place(
        x = 666, y = 443,
        width = 96,
        height = 34
    )



def SignupScreen():
    clearScreen()

    # Background
    SignupBackground = canvas.create_image(
        390.0, 178.5,
        image=Signup_Background
    )

    #---------- BUTTON "Back"
    SignupBackButton = Button(
        image = Signup_BackButton,
        borderwidth = 0,
        highlightthickness = 0,
        command = LoginScreen,
        relief = "flat"
    ).place(
        x = 19, y = 13,
        width = 85,
        height = 34
    )

    #---------- Entry Username
    SignupEntry1Background = canvas.create_image(
        400.0, 148.0,
        image = Signup_Entry
    )

    SignupEntry1 = Entry(
        bd = 0,
        bg = "#ffffff",
        highlightthickness = 0,
        font=("20")
    )
    SignupEntry1.place(
        x = 258.0, y = 123 + EntryDiscrepancy,
        width = 284.0,
        height = EntryHeight
    )

    #---------- Entry Password
    SignupEntry2Background = canvas.create_image(
        400.0, 242.0,
        image = Signup_Entry
    )

    SignupEntry2 = Entry(
        bd = 0,
        bg = "#ffffff",
        highlightthickness = 0,
        font=("20")
    )
    SignupEntry2.place(
        x = 258.0, y = 217 + EntryDiscrepancy,
        width = 284.0,
        height = EntryHeight
    )

    #---------- Entry Bank Account
    SignupEntry3Background = canvas.create_image(
        400.0, 336.0,
        image = Signup_Entry
    )

    SignupEntry3 = Entry(
        bd = 0,
        bg = "#ffffff",
        highlightthickness = 0,
        font=("20")
    )
    SignupEntry3.place(
        x = 258.0, y = 311 + EntryDiscrepancy,
        width = 284.0,
        height = EntryHeight
    )

    def checkFieldValid(typeCheck, userInput):
        if typeCheck == "username":
            if len(userInput) < 5:
                messagebox.showinfo("Invalid input", "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)")
                return False
            elif (all(c.isnumeric() or c.islower() for c in userInput)) == False:
                messagebox.showinfo("Invalid input", "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)")
                return False

        elif typeCheck == "password":
            if len(userInput) < 3:
                messagebox.showinfo("Invalid input", "Password must have at least 3 characters")
                return False

        elif typeCheck == "bank":
            if len(userInput) != 10:
                messagebox.showinfo("Invalid input", "Bank account must have 10 characters and contain numbers (0-9)")
                return False
            elif userInput.isnumeric() == False:
                messagebox.showinfo("Invalid input", "Bank account must have 10 characters and contain numbers (0-9)")
                return False
        
    def submitForm():
        usernameInput = SignupEntry1.get()
        passwordInput = SignupEntry2.get()
        bankInput = SignupEntry3.get()
        print (usernameInput, passwordInput, bankInput)
        if checkFieldValid("username", usernameInput) == False:
            return
        if checkFieldValid("password", passwordInput) == False:
            return
        if checkFieldValid("bank", bankInput) == False:
            return

        print("Submitted !")

    #---------- BUTTON "Submit"
    SignupSubmitButton = Button(
        image = Signup_SubmitButton,
        borderwidth = 0,
        highlightthickness = 0,
        command = submitForm,
        relief = "flat"
    ).place(
        x = 292, y = 395,
        width = 216,
        height = 50
    )

LoginScreen()


window.resizable(False, False)
window.mainloop()
