import tkinter as tk
from tkinter import messagebox
from math import floor
from PIL import Image, ImageTk
from client_method import *


def convert_size(window, original_size):
    return floor((window.frameWidth * original_size) / 1600)


def convert_image(window, path, original_width, original_height):
    original_image = Image.open(path)
    resized_image = original_image.resize(
        (convert_size(window, original_width), convert_size(window, original_height))
    )
    converted_image = ImageTk.PhotoImage(resized_image)
    return converted_image


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.focus_force()
        self.grab_set()
        self.title("Go2Chill")
        self.scaleRate = 0.8

        self.frameWidth = floor(self.winfo_screenwidth() * self.scaleRate)
        self.frameHeight = floor(self.frameWidth * 9 / 16)
        self.fontSize = convert_size(self, 40)
        self.resolution = f"{self.frameWidth}x{self.frameHeight}"

        self.entryHeight = convert_size(self, 60)
        self.entryFontSize = f"{convert_size(self, 80)}"
        self.entryDiscrenpancy = convert_size(self, 12)

        # Current user
        self.username = ""

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry(self.resolution)
        # self.configure(bg="#ffffff")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginFrame, SignupFrame, MenuFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("LoginFrame")

    def on_closing(self):
        print(self.username)
        print(QUIT_MSG)
        # client.sendall("{quit}")
        send_s(client, QUIT_MSG)
        client.close()
        self.quit()

    def show_frame(self, page_name):
        """Show a frame for the given name"""
        print(f"Show {page_name}")
        frame = self.frames[page_name]
        frame.tkraise()


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.__create_widgets(controller)

    def __create_widgets(self, controller):
        self.canvas = tk.Canvas(
            self,
            bg="#ffffff",
            height=controller.frameHeight,
            width=controller.frameWidth,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)
        # ---Image---
        self.ImgLoginBg = convert_image(
            controller, "./assets/Login_Background.png", 1448, 900
        )
        self.ImgEntry = convert_image(controller, "./assets/Login_Entry.png", 510, 84)
        self.ImgLoginBtn = convert_image(
            controller, "./assets/Login_LoginButton.png", 510, 84
        )
        self.ImgSignupBtn = convert_image(
            controller, "./assets/Login_SignupButton.png", 129, 38
        )
        # ------

        # ---Background---
        self.LoginBg = self.canvas.create_image(
            convert_size(controller, 724),
            convert_size(controller, 450),
            image=self.ImgLoginBg,
        )

        # ---Entry username---
        self.UserEntryBg = self.canvas.create_image(
            convert_size(controller, 1201),
            convert_size(controller, 304),
            image=self.ImgEntry,
        )
        self.UserEntry = tk.Entry(
            master=self,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=controller.entryFontSize,
        )
        self.UserEntry.place(
            x=convert_size(controller, 962),
            y=convert_size(controller, 262) + controller.entryDiscrenpancy,
            width=convert_size(controller, 478),
            height=controller.entryHeight,
        )
        # ------

        # ---Entry password---
        self.PswdEntryBg = self.canvas.create_image(
            convert_size(controller, 1201),
            convert_size(controller, 459),
            image=self.ImgEntry,
        )
        self.PswdEntry = tk.Entry(
            master=self,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=controller.entryFontSize,
        )
        self.PswdEntry.place(
            x=convert_size(controller, 962),
            y=convert_size(controller, 417) + controller.entryDiscrenpancy,
            width=convert_size(controller, 478),
            height=controller.entryHeight,
        )
        # ------

        # --- BUTTON "Login" ---
        self.LoginLoginBtn = tk.Button(
            master=self,
            image=self.ImgLoginBtn,
            borderwidth=0,
            highlightthickness=0,
            command=self.submitLogin,
            relief="flat",
        )
        self.LoginLoginBtn.place(
            x=convert_size(controller, 946),
            y=convert_size(controller, 572),
            width=convert_size(controller, 510),
            height=convert_size(controller, 84),
        )
        # ------
        # --- BUTTON "Create one" ---
        self.LoginSignupBtn = tk.Button(
            master=self,
            image=self.ImgSignupBtn,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame("SignupFrame"),
            relief="flat",
        )
        self.LoginSignupBtn.place(
            x=convert_size(controller, 1302),
            y=convert_size(controller, 788),
            width=convert_size(controller, 129),
            height=convert_size(controller, 38),
        )
        # ------

    def submitLogin(self):
        username_input = self.UserEntry.get()
        password_input = self.PswdEntry.get()
        print(username_input, password_input)
        valid, pop_up, username = Login(client, username_input, password_input)
        print(pop_up)
        if not valid:
            messagebox.showinfo("Invalid input", pop_up)
        else:
            messagebox.showinfo("Login status", pop_up)
            if username:
                self.controller.username = username
                self.controller.show_frame("MenuFrame")


class SignupFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.__create_widgets(controller)
        # self.pack(fill=tk.BOTH, expand=1)

    def __create_widgets(self, controller):
        self.canvas = tk.Canvas(
            self,
            bg="#ffffff",
            height=controller.frameHeight,
            width=controller.frameWidth,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)
        self.ImgSignupBg = convert_image(
            controller, "./assets/Signup_Background.png", 547, 470
        )
        self.ImgSignupEntry = convert_image(
            controller, "./assets/Signup_Entry.png", 560, 88
        )
        self.ImgBackBtn = convert_image(
            controller, "./assets/Signup_BackButton.png", 228, 61
        )
        self.ImgSubmitBtn = convert_image(
            controller, "./assets/Signup_SubmitButton.png", 560, 88
        )
        # ------

        # ---Background---
        self.SignupBg = self.canvas.create_image(
            convert_size(controller, 806.5),
            convert_size(controller, 303.0),
            image=self.ImgSignupBg,
        )
        # ------

        # ---BUTTON "Back"---
        self.signupBackBtn = tk.Button(
            master=self,
            image=self.ImgBackBtn,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame("LoginFrame"),
            relief="flat",
        )
        self.signupBackBtn.place(
            x=convert_size(controller, 24),
            y=convert_size(controller, 20),
            width=convert_size(controller, 228),
            height=convert_size(controller, 61),
        )
        # ------

        # ---Entry username---
        self.signupUserBg = self.canvas.create_image(
            convert_size(controller, 800),
            convert_size(controller, 270),
            image=self.ImgSignupEntry,
        )
        self.signupUserEntry = tk.Entry(
            master=self,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=controller.entryFontSize,
        )
        self.signupUserEntry.place(
            x=convert_size(controller, 536),
            y=convert_size(controller, 226) + controller.entryDiscrenpancy,
            width=convert_size(controller, 528),
            height=controller.entryHeight,
        )
        # ------

        # ---Entry password---
        self.signupPswdBg = self.canvas.create_image(
            convert_size(controller, 800),
            convert_size(controller, 429),
            image=self.ImgSignupEntry,
        )
        self.signupPswdEntry = tk.Entry(
            master=self,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=controller.entryFontSize,
        )
        self.signupPswdEntry.place(
            x=convert_size(controller, 536),
            y=convert_size(controller, 385) + controller.entryDiscrenpancy,
            width=convert_size(controller, 528),
            height=controller.entryHeight,
        )
        # ------

        # ---Entry Bank number---
        self.signupBankBg = self.canvas.create_image(
            convert_size(controller, 800),
            convert_size(controller, 590),
            image=self.ImgSignupEntry,
        )
        self.signupBankEntry = tk.Entry(
            master=self,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=controller.entryFontSize,
        )
        self.signupBankEntry.place(
            x=convert_size(controller, 536),
            y=convert_size(controller, 546) + controller.entryDiscrenpancy,
            width=convert_size(controller, 528),
            height=controller.entryHeight,
        )

        # ---Submit button---
        self.submitBtn = tk.Button(
            master=self,
            image=self.ImgSubmitBtn,
            borderwidth=0,
            highlightthickness=0,
            command=self.Submit,
            relief="flat",
        )
        self.submitBtn.place(
            x=convert_size(controller, 520),
            y=convert_size(controller, 705),
            width=convert_size(controller, 560),
            height=convert_size(controller, 88),
        )

    def Submit(self):
        username = self.signupUserEntry.get()
        password = self.signupPswdEntry.get()
        bank = self.signupBankEntry.get()
        print(username, password, bank)
        valid, pop_up = Register(client, username, password, bank)
        print(pop_up)
        if not valid:
            messagebox.showinfo("Invalid input", pop_up)
        else:
            messagebox.showinfo("Register status", pop_up)


def btn_clicked():
    print("Button clicked")


class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.__create_widgets(controller)

    def __create_widgets(self, controller):
        self.canvas = tk.Canvas(self, bg="#ffffff",
                                height=controller.frameHeight, width=controller.frameWidth,
                                bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.ImgBg = convert_image(controller, "./assets/Menu_BG.png", 1302, 552)
        self.ImgLogout = convert_image(controller, "./assets/Menu_img0.png", 182, 258)
        self.ImgGuide = convert_image(controller, "./assets/Menu_img1.png", 182, 258)
        self.ImgReservation = convert_image(controller, "./assets/Menu_img2.png", 234, 258)
        self.ImgHotel = convert_image(controller, "./assets/Menu_img3.png", 182, 258)

        # ---Background---
        self.BG = self.canvas.create_image(convert_size(controller, 800),
                                           convert_size(controller, 624),
                                           image=self.ImgBg)
        # ------

        # ---Logout button---
        self.LogoutBtn = tk.Button(master=self, image=self.ImgLogout, borderwidth=0,
                                   highlightthickness=0, command=lambda: self.LogoutClicked(), relief="flat")
        self.LogoutBtn.place(x=convert_size(controller, 1255), y=convert_size(controller, 52),
                             width=convert_size(controller, 182), height=convert_size(controller, 258))
        # ------

        # ---Guide button---
        self.GuideBtn = tk.Button(master=self, image=self.ImgGuide, borderwidth=0,
                                  highlightthickness=0, command=lambda: btn_clicked(), relief="flat")
        self.GuideBtn.place(x=convert_size(controller, 891), y=convert_size(controller, 50),
                            width=convert_size(controller, 182), height=convert_size(controller, 258))
        # ------

        # ---Reservation button---
        self.ReservationBtn = tk.Button(master=self, image=self.ImgReservation, borderwidth=0,
                                        highlightthickness=0, command=lambda: self.ReservationClicked(), relief="flat")
        self.ReservationBtn.place(x=convert_size(controller, 502), y=convert_size(controller, 50),
                                  width=convert_size(controller, 234), height=convert_size(controller, 258))
        # ------

        # ---Hotel list Button---
        self.HotelBtn = tk.Button(master=self, image=self.ImgHotel, borderwidth=0,
                                  highlightthickness=0, command=lambda: self.HotelListClicked(), relief="flat")
        self.HotelBtn.place(x=convert_size(controller, 163), y=convert_size(controller, 50),
                            width=convert_size(controller, 182), height=convert_size(controller, 258))
        # ------

    @staticmethod
    def HotelListClicked():
        # username = self.controller.username
        ShowHotelList(client)

    def ReservationClicked(self):
        username = self.controller.username
        ShowBooked(client, username)

    def LogoutClicked(self):
        self.controller.username = ""
        self.controller.show_frame("LoginFrame")

if __name__ == "__main__":
    connected = True
    app = App()
    app.mainloop()
