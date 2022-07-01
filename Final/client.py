from tkinter import *
from tkinter import messagebox
from math import floor
from PIL import Image, ImageTk

global Login_Background
global Login_Entry
global Login_LoginButton
global Login_SignupButton
global Signup_Background
global Signup_Entry
global Signup_BackButton
global Signup_SubmitButton


# ====================== Convert Function =======================#
def btn_clicked():
    print("Button Clicked")


def convertSize(originalSize):
    frameWidth = window.winfo_screenwidth() * scaleRate
    return floor((frameWidth * originalSize) / 1600)


# originalWidth & originalHeight are the Width and Height on Figma
def convertImage(path, originalWidth, originalHeight):
    originalImage = Image.open(path)
    resizedImage = originalImage.resize(
        (convertSize(originalWidth), convertSize(originalHeight)))
    convertedImage = ImageTk.PhotoImage(resizedImage)
    return convertedImage


# ================================================================


def clearScreen():
    for widget in window.place_slaves():
        widget.place_forget()


def LoginScreen():
    clearScreen()

    Login_Background = convertImage("./assets/Login_Background.png", 1448, 900)
    Login_Entry = convertImage("./assets/Login_Entry.png", 510, 84)
    Login_LoginButton = convertImage("./assets/Login_LoginButton.png", 510, 84)
    Login_SignupButton = convertImage("./assets/Login_SignupButton.png", 129, 38)

    canvas = Canvas(
        window,
        bg="#ffffff",
        height=frameHeight,
        width=frameWidth,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )
    canvas.place(x=0, y=0)

    # Background
    LoginBackground = canvas.create_image(convertSize(724.0),
                                          convertSize(450.0),
                                          image=Login_Background)

    # ---------- Entry Username
    LoginEntry1Background = canvas.create_image(convertSize(1201),
                                                convertSize(304),
                                                image=Login_Entry)
    LoginEntry1 = Entry(bd=0,
                        bg="#ffffff",
                        highlightthickness=0,
                        font=(EntryFontSize))
    LoginEntry1.place(
        x=convertSize(962),
        y=convertSize(262) + EntryDiscrepancy,
        width=convertSize(478),
        height=EntryHeight,
    )

    # ---------- Entry Password
    LoginEntry2Background = canvas.create_image(convertSize(1201.0),
                                                convertSize(459.0),
                                                image=Login_Entry)
    LoginEntry2 = Entry(bd=0,
                        bg="#ffffff",
                        highlightthickness=0,
                        font=(EntryFontSize))
    LoginEntry2.place(
        x=convertSize(962),
        y=convertSize(417) + EntryDiscrepancy,
        width=convertSize(478),
        height=EntryHeight,
    )

    def submitLogin():
        usernameInput = LoginEntry1.get()
        passwordInput = LoginEntry2.get()
        print(usernameInput, passwordInput)

    # ---------- BUTTON "Log in"
    LoginLoginButton = Button(
        image=Login_LoginButton,
        borderwidth=0,
        highlightthickness=0,
        command=submitLogin,
        relief="flat",
    ).place(
        x=convertSize(946),
        y=convertSize(572),
        width=convertSize(510),
        height=convertSize(84),
    )

    # ---------- BUTTON "Create one"
    LoginSignupButton = Button(
        image=Login_SignupButton,
        borderwidth=0,
        highlightthickness=0,
        command=SignupScreen,
        relief="flat",
    ).place(
        x=convertSize(1302),
        y=convertSize(788),
        width=convertSize(129),
        height=convertSize(38),
    )


def SignupScreen():
    clearScreen()

    Signup_Background = convertImage("./assets/Signup_Background.png", 547,
                                     470)
    Signup_Entry = convertImage("./assets/Signup_Entry.png", 560, 88)
    Signup_BackButton = convertImage("./assets/Signup_BackButton.png", 228, 61)
    Signup_SubmitButton = convertImage("./assets/Signup_SubmitButton.png", 560,
                                       88)

    canvas = Canvas(
        window,
        bg="#ffffff",
        height=frameHeight,
        width=frameWidth,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    ).place(x=0, y=0)

    # Background
    SignupBackground = canvas.create_image(convertSize(806.5),
                                           convertSize(303.0),
                                           image=Signup_Background)

    # ---------- BUTTON "Back"
    SignupBackButton = Button(
        image=Signup_BackButton,
        borderwidth=0,
        highlightthickness=0,
        command=LoginScreen,
        relief="flat",
    ).place(
        x=convertSize(24),
        y=convertSize(20),
        width=convertSize(228),
        height=convertSize(61),
    )

    # ---------- Entry Username
    SignupEntry1Background = canvas.create_image(convertSize(800),
                                                 convertSize(270),
                                                 image=Signup_Entry)

    SignupEntry1 = Entry(bd=0,
                         bg="#ffffff",
                         highlightthickness=0,
                         font=(EntryFontSize))
    SignupEntry1.place(
        x=convertSize(536),
        y=convertSize(226) + EntryDiscrepancy,
        width=convertSize(528),
        height=EntryHeight,
    )

    # ---------- Entry Password
    SignupEntry2Background = canvas.create_image(convertSize(800),
                                                 convertSize(429),
                                                 image=Signup_Entry)

    SignupEntry2 = Entry(bd=0,
                         bg="#ffffff",
                         highlightthickness=0,
                         font=(EntryFontSize))
    SignupEntry2.place(
        x=convertSize(536),
        y=convertSize(385) + EntryDiscrepancy,
        width=convertSize(528),
        height=EntryHeight,
    )

    # ---------- Entry Bank Account
    SignupEntry3Background = canvas.create_image(convertSize(800),
                                                 convertSize(590),
                                                 image=Signup_Entry)

    SignupEntry3 = Entry(bd=0,
                         bg="#ffffff",
                         highlightthickness=0,
                         font=(EntryFontSize))
    SignupEntry3.place(
        x=convertSize(536),
        y=convertSize(546) + EntryDiscrepancy,
        width=convertSize(528),
        height=EntryHeight,
    )

    def checkFieldValid(typeCheck, userInput):
        if typeCheck == "username":
            if len(userInput) < 5:
                messagebox.showinfo(
                    "Invalid input",
                    "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)",
                )
                return False
            elif (all(c.isnumeric() or c.islower()
                      for c in userInput)) == False:
                messagebox.showinfo(
                    "Invalid input",
                    "Username must have at least 5 characters and contain letters (a-z), numbers (0-9)",
                )
                return False

        elif typeCheck == "password":
            if len(userInput) < 3:
                messagebox.showinfo(
                    "Invalid input",
                    "Password must have at least 3 characters")
                return False

        elif typeCheck == "bank":
            if len(userInput) != 10:
                messagebox.showinfo(
                    "Invalid input",
                    "Bank account must have 10 characters and contain numbers (0-9)",
                )
                return False
            elif userInput.isnumeric() == False:
                messagebox.showinfo(
                    "Invalid input",
                    "Bank account must have 10 characters and contain numbers (0-9)",
                )
                return False

    def submitForm():
        usernameInput = SignupEntry1.get()
        passwordInput = SignupEntry2.get()
        bankInput = SignupEntry3.get()
        print(usernameInput, passwordInput, bankInput)
        if checkFieldValid("username", usernameInput) == False:
            return
        if checkFieldValid("password", passwordInput) == False:
            return
        if checkFieldValid("bank", bankInput) == False:
            return

        print("Submitted !")

    # ---------- BUTTON "Submit"
    SignupSubmitButton = Button(
        image=Signup_SubmitButton,
        borderwidth=0,
        highlightthickness=0,
        command=submitForm,
        relief="flat",
    ).place(
        x=convertSize(520),
        y=convertSize(705),
        width=convertSize(560),
        height=convertSize(88),
    )


if __name__ == "__main__":
    window = Tk()

    # ==================== Constants Declaration ====================#
    scaleRate = 0.8
    frameWidth = window.winfo_screenwidth() * scaleRate
    frameHeight = (window.winfo_screenwidth() * scaleRate) * 9 / 16
    fontSize = convertSize(40)
    geometry = f"{floor(frameWidth)}" + "x" + f"{floor(frameHeight)}"

    EntryHeight = convertSize(60)
    EntryFontSize = f"{convertSize(80)}"
    EntryDiscrepancy = convertSize(12)

    # ==================== Image Declaration ====================#

    # ========================= Screen ==========================#
    window.geometry(geometry)
    window.configure(bg="#ffffff")

    print(window.winfo_screenwidth(), window.winfo_screenheight())
    window.resizable(False, False)
    LoginScreen()
    window.mainloop()
