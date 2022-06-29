from tkinter import *
from math import floor
from PIL import Image, ImageTk

window = Tk()
print(window.winfo_screenwidth(), window.winfo_screenheight())

#====================== Convert Function =======================#
def btn_clicked():
    print("Button Clicked")

def convertSize(originalSize):
    frameWidth = window.winfo_screenwidth() * scaleRate
    return floor((frameWidth * originalSize )/1600)


# originalWidth & originalHeight are the Width and Height on Figma
def convertImage(path, originalWidth, originalHeight):
    originalImage = Image.open(path)
    resizedImage = originalImage.resize((convertSize(originalWidth), convertSize(originalHeight)))
    convertedImage = ImageTk.PhotoImage(resizedImage)
    return convertedImage


#==================== Constants Declaration ====================#
scaleRate = 0.8
frameWidth = window.winfo_screenwidth() * scaleRate
frameHeight = (window.winfo_screenwidth() * scaleRate) * 9/16
fontSize = convertSize(40)
geometry = f'{floor(frameWidth)}' + "x" + f'{floor(frameHeight)}'

EntryHeight = convertSize(60)
EntryFontSize = f'{convertSize(80)}'
EntryDiscrepancy = convertSize(12)


#==================== Image Declaration ====================#
Login_Background = convertImage("./assets/Login_Background.png", 1448, 900)
Login_Entry = convertImage("./assets/Login_Entry.png", 510, 84)
Login_LoginButton = convertImage("./assets/Login_LoginButton.png", 510, 84)
Login_SignupButton = convertImage("./assets/Login_SignupButton.png", 129, 38)



#========================= Screen ==========================#
window.geometry(geometry)
window.configure(bg = "#ffffff")


def clearScreen(self = window):
    for widget in self.place_slaves():
        widget.place_forget()


def LoginScreen():
    clearScreen()

    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = frameHeight,
        width = frameWidth,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    # Background
    LoginBackground = canvas.create_image(
        convertSize(724.0), convertSize(450.0),
        image=Login_Background
    )

    #---------- Entry Username
    LoginEntry1Background = canvas.create_image(
        convertSize(1201), convertSize(304),
        image = Login_Entry
    )
    LoginEntry1 = Entry(
        bd = 0,
        bg = "#ffffff",
        highlightthickness = 0,
        font = (EntryFontSize)
    )
    LoginEntry1.place(
        x = convertSize(962), y = convertSize(262) + EntryDiscrepancy,
        width = convertSize(478),
        height = EntryHeight
    )

    #---------- Entry Password
    LoginEntry2Background = canvas.create_image(
        convertSize(1201.0), convertSize(459.0),
        image = Login_Entry
    )
    LoginEntry2 = Entry(
        bd = 0,
        bg = "#ffffff",
        highlightthickness = 0,
        font = (EntryFontSize)
    )
    LoginEntry2.place(
        x = convertSize(962), y = convertSize(417) + EntryDiscrepancy,
        width = convertSize(478),
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
        x = convertSize(946), y = convertSize(572),
        width = convertSize(510),
        height = convertSize(84)
    )

    #---------- BUTTON "Create one"
    LoginSignupButton = Button(
        image = Login_SignupButton,
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_clicked,
        relief = "flat"
    ).place(
        x = convertSize(1302), y = convertSize(788),
        width = convertSize(129),
        height = convertSize(38)
    )


LoginScreen()


window.resizable(False, False)
window.mainloop()
