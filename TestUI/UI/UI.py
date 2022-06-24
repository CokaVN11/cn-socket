# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from operator import truediv
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("800x500")
window.configure(bg="#FFFFFF")

# -------------------------------- Save image --------------------------------#
# LOGIN PAGE
LoginCreateOneButton = PhotoImage(file=relative_to_assets("LoginCreateOne.png"))
LoginButton = PhotoImage(file=relative_to_assets("LoginLogin.png"))
LoginEntry1 = PhotoImage(file=relative_to_assets("LoginEntry1.png"))
LoginEntry2 = PhotoImage(file=relative_to_assets("LoginEntry2.png"))

# SIGNUP PAGE

SignupBackButton = PhotoImage(
    file=relative_to_assets("SignupBack.png"))
SignupSubmitButton = PhotoImage(
    file=relative_to_assets("SignupSubmit.png"))
SignupEntry1 = PhotoImage(
    file=relative_to_assets("SignupEntry1.png"))
SignupEntry2 = PhotoImage(
    file=relative_to_assets("SignupEntry2.png"))
SignupEntry3 = PhotoImage(
    file=relative_to_assets("SignupEntry3.png"))



#---------------------------- Implement Function ----------------------------#
def clearScreen(self = window):
    for widget in self.place_slaves():
        widget.place_forget()


def SignupScreen():
    clearScreen()

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=500,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )

    canvas.place(x=0, y=0)

    # BUTTON "BACK"
    button_1 = Button(
        image=SignupBackButton,
        borderwidth=0,
        highlightthickness=0,
        command=LoginScreen,
        relief="flat",
    )
    button_1.place(x=19.00000000000003, y=13.0, width=85.0, height=34.0)

    # BUTTON "SUBMIT"
    button_2 = Button(
        image=SignupSubmitButton,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("SIGN UP SUBMIT CLICKED"),
        relief="flat",
    )
    button_2.place(x=292.0, y=395.0, width=216.0, height=50.0)

    # ENTRY USERNAME

    entry_bg_1 = canvas.create_image(
        400.0,
        336.0,
        image=SignupEntry1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0,
        font=("20")
    )
    entry_1.place(
        x=258.0,
        y=311.0 + 8,
        width=284.0,
        height=36.0
    )


    # ENTRY PASSWORD
    entry_bg_2 = canvas.create_image(
        400.0,
        242.0,
        image=SignupEntry2
    )
    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0,
        font=("20")
    )
    entry_2.place(
        x=258.0,
        y=217.0 + 8,
        width=284.0,
        height=36.0
    )


    # ENTRY BANK ACCOUNT
    entry_bg_3 = canvas.create_image(
        400.0,
        148.0,
        image=SignupEntry3
    )
    entry_3 = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0,
        font=("20")
    )
    entry_3.place(
        x=258.0,
        y=123.0 + 8,
        width=284.0,
        height=36.0
    )


    canvas.create_text(
        250.00000000000003,
        290.0,
        anchor="nw",
        text="Bank account (10 characters, 0-9)",
        fill="#000000",
        font=("Roboto Bold", 16 * -1),
    )

    canvas.create_text(
        250.00000000000003,
        195.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("Roboto Bold", 16 * -1),
    )

    canvas.create_text(
        250.00000000000003,
        102.0,
        anchor="nw",
        text="Username",
        fill="#000000",
        font=("Roboto Bold", 16 * -1),
    )

    canvas.create_text(
        330.0,
        39.0,
        anchor="nw",
        text="Sign up",
        fill="#000000",
        font=("Roboto Bold", 36 * -1),
    )


def LoginScreen():
    clearScreen()

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=500,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        1.1368683772161603e-13,
        5.684341886080802e-14,
        400.0000000000001,
        500.00000000000006,

        fill="#56BFD3",
        outline="")


    canvas.create_rectangle(
        139.9999999999999,
        329.99999999999994,
        259.9999999999999,
        440.99999999999994,
        fill="#56BFD3",
        outline="")


    canvas.create_text(
        439.9999999999999,
        448.99999999999994,
        anchor="nw",
        text="If you don't have an account,",
        fill="#000000",
        font=("Roboto Bold", 18 * -1),
    )

    canvas.create_rectangle(
        469.9999999999999,
        416.99999999999994,
        729.9999999999999,
        418.99999999999994,

        fill="#56BFD3",
        outline="")


    canvas.create_text(
        454,
        208,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("Roboto Bold", 20 * -1),
    )

    canvas.create_text(
        454,
        116,
        anchor="nw",
        text="Username",
        fill="#000000",
        font=("Roboto Bold", 20 * -1),
    )

    canvas.create_text(
        454.9999999999999,
        49.99999999999994,
        anchor="nw",
        text="Log in",
        fill="#000000",
        font=("Roboto Bold", 36 * -1),
    )

    canvas.create_text(
        32.999999999999886,
        90.99999999999994,
        anchor="nw",
        text="Welcome to Go2Chill",
        fill="#FFFFFF",
        font=("Roboto Bold", 28 * -1),
    )

    canvas.create_rectangle(
        32.999999999999886,
        150.99999999999994,
        192.9999999999999,
        152.99999999999994,
        fill="#FFFFFF",
        outline="",
    )

    # BUTTON "CREATE ONE"
    button_1 = Button(
        image=LoginCreateOneButton,
        borderwidth=0,
        highlightthickness=0,
        command=SignupScreen,
        relief="flat",
    )
    button_1.place(x=665.9999999999999, y=442.99999999999994, width=96.0, height=34.0)

    # BUTTON "LOG IN"
    button_2 = Button(
        image=LoginButton,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Hehe Submit"),
        relief="flat",
    )
    button_2.place(x=449.9999999999999, y=329.99999999999994, width=300.0, height=50.0)

    entry_bg_1 = canvas.create_image(

        599.9999999999999,
        261.99999999999994,
        image=LoginEntry1
    )
    entry_1 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0,
        font=("20")
    )
    entry_1.place(
        x=457.9999999999999,
        y=244,
        width=284.0,
        height=36.0

    )
    entry_1 = Entry(bd=0, bg="#FFFFFF", highlightthickness=0)
    entry_1.place(x=457.9999999999999, y=244, width=284.0, height=36.0)

    entry_bg_2 = canvas.create_image(

        599.9999999999999,
        167.99999999999994,
        image=LoginEntry2
    )
    entry_2 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0,
        font=("20")
    )
    entry_2.place(
        x=457.9999999999999,
        y=150,
        width=284.0,
        height=36.0
    )
    entry_2 = Entry(bd=0, bg="#FFFFFF", highlightthickness=0)
    entry_2.place(x=457.9999999999999, y=150, width=284.0, height=36.0)

    canvas.create_text(
        32.999999999999886,
        192.99999999999994,
        anchor="nw",

        text="The application provides easy and\nconvenient booking service for you.",

        fill="#FFFFFF",
        font=("Roboto Bold", 18 * -1),
    )

    canvas.create_text(
        32.999999999999886,
        247.99999999999994,
        anchor="nw",
        text="Bringing you the feeling of always having\nmoments of relaxation and comfort.",
        fill="#FFFFFF",
        font=("Roboto Bold", 18 * -1),
    )

LoginScreen()

window.resizable(False, False)
window.mainloop()
