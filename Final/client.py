import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from math import floor
from PIL import Image, ImageTk
from client_method import *


@staticmethod
def convertSize(window, originalSize):
    return floor((window.frameWidth * originalSize) / 1600)


@staticmethod
def convertImage(window, path, originalWidth, originalHeight):
    originalImage = Image.open(path)
    resizedImage = originalImage.resize(
        (convertSize(window,
                     originalWidth), convertSize(window, originalHeight)))
    convertedImage = ImageTk.PhotoImage(resizedImage)
    return convertedImage


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.focus_force()
        self.grab_set()
        self.title('Go2Chill')
        self.scaleRate = 0.8

        self.frameWidth = floor(self.winfo_screenwidth() * self.scaleRate)
        self.frameHeight = floor(self.frameWidth * 9 / 16)
        self.fontSize = convertSize(self, 40)
        self.resolution = f"{self.frameWidth}x{self.frameHeight}"

        self.entryHeight = convertSize(self, 60)
        self.entryFontSize = f"{convertSize(self, 80)}"
        self.entryDiscrenpancy = convertSize(self, 12)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry(self.resolution)
        # self.configure(bg="#ffffff")
        self.resizable(0, 0)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginFrame, SignupFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("LoginFrame")

    def on_closing(self):
        print(QUIT_MSG)
        # client.sendall("{quit}")
        send_s(client, QUIT_MSG)
        client.close()
        self.quit()

    def show_frame(self, page_name):
        '''Show a frame for the given name'''
        print(f"Show {page_name}")
        frame = self.frames[page_name]
        frame.tkraise()


class LoginFrame(ttk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.__create_widgets(parent, controller)
        # self.pack(side="top", fill=tk.BOTH, expand=1)

    def __create_widgets(self, parent, controller):
        self.canvas = tk.Canvas(self,
                                bg="#ffffff",
                                height=controller.frameHeight,
                                width=controller.frameWidth,
                                bd=0,
                                highlightthickness=0,
                                relief="ridge")
        self.canvas.place(x=0, y=0)
        # ---Image---
        self.ImgLoginBg = convertImage(controller,
                                       "./assets/Login_Background.png", 1448,
                                       900)
        self.ImgEntry = convertImage(controller, "./assets/Login_Entry.png",
                                     510, 84)
        self.ImgLoginBtn = convertImage(controller,
                                        "./assets/Login_LoginButton.png", 510,
                                        84)
        self.ImgSingupBtn = convertImage(controller,
                                         "./assets/Login_SignupButton.png",
                                         129, 38)
        # ------

        # ---Background---
        self.LoginBg = self.canvas.create_image(convertSize(controller, 724),
                                                convertSize(controller, 450),
                                                image=self.ImgLoginBg)

        # ---Entry username---
        self.UserEntryBg = self.canvas.create_image(
            convertSize(controller, 1201),
            convertSize(controller, 304),
            image=self.ImgEntry,
        )
        self.UserEntry = tk.Entry(master=self,
                                  bd=0,
                                  bg="#ffffff",
                                  highlightthickness=0,
                                  font=controller.entryFontSize)
        self.UserEntry.place(
            x=convertSize(controller, 962),
            y=convertSize(controller, 262) + controller.entryDiscrenpancy,
            width=convertSize(controller, 478),
            height=controller.entryHeight,
        )
        # ------

        # ---Entry password---
        self.PswdEntryBg = self.canvas.create_image(
            convertSize(controller, 1201),
            convertSize(controller, 459),
            image=self.ImgEntry,
        )
        self.PswdEntry = tk.Entry(master=self,
                                  bd=0,
                                  bg="#ffffff",
                                  highlightthickness=0,
                                  font=controller.entryFontSize)
        self.PswdEntry.place(
            x=convertSize(controller, 962),
            y=convertSize(controller, 417) + controller.entryDiscrenpancy,
            width=convertSize(controller, 478),
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
        ).place(
            x=convertSize(controller, 946),
            y=convertSize(controller, 572),
            width=convertSize(controller, 510),
            height=convertSize(controller, 84),
        )
        # ------
        # --- BUTTON "Create one" ---
        self.LoginSignupBtn = tk.Button(
            master=self,
            image=self.ImgSingupBtn,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame("SignupFrame"),
            relief="flat",
        ).place(
            x=convertSize(controller, 1302),
            y=convertSize(controller, 788),
            width=convertSize(controller, 129),
            height=convertSize(controller, 38),
        )
        # ------

    def submitLogin(self):
        usernameInput = self.UserEntry.get()
        passwordInput = self.PswdEntry.get()
        print(usernameInput, passwordInput)
        valid, pop_up, username = Login(client, usernameInput, passwordInput)
        print(pop_up)
        if not valid:
            messagebox.showinfo("Invalid input", pop_up)
        else:
            messagebox.showinfo("Login status", pop_up)


class SignupFrame(ttk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.__create_widgets(parent, controller)
        # self.pack(fill=tk.BOTH, expand=1)

    def __create_widgets(self, parent, controller):
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
        self.ImgSignupBg = convertImage(controller,
                                        "./assets/Signup_Background.png", 547,
                                        470)
        self.ImgSignupEntry = convertImage(controller,
                                           "./assets/Signup_Entry.png", 560,
                                           88)
        self.ImgBackBtn = convertImage(controller,
                                       "./assets/Signup_BackButton.png", 228,
                                       61)
        self.ImgSubmitBtn = convertImage(controller,
                                         "./assets/Signup_SubmitButton.png",
                                         560, 88)
        # ------

        # ---Background---
        self.SignupBg = self.canvas.create_image(
            convertSize(controller, 806.5),
            convertSize(controller, 303.0),
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
        ).place(
            x=convertSize(controller, 24),
            y=convertSize(controller, 20),
            width=convertSize(controller, 228),
            height=convertSize(controller, 61),
        )
        # ------

        # ---Entry username---
        self.signupUserBg = self.canvas.create_image(
            convertSize(controller, 800),
            convertSize(controller, 270),
            image=self.ImgSignupEntry,
        )
        self.signupUserEntry = tk.Entry(master=self,
                                        bd=0,
                                        bg="#ffffff",
                                        highlightthickness=0,
                                        font=controller.entryFontSize)
        self.signupUserEntry.place(
            x=convertSize(controller, 536),
            y=convertSize(controller, 226) + controller.entryDiscrenpancy,
            width=convertSize(controller, 528),
            height=controller.entryHeight,
        )
        # ------

        # ---Entry password---
        self.signupPswdBg = self.canvas.create_image(
            convertSize(controller, 800),
            convertSize(controller, 429),
            image=self.ImgSignupEntry,
        )
        self.signupPswdEntry = tk.Entry(master=self,
                                        bd=0,
                                        bg="#ffffff",
                                        highlightthickness=0,
                                        font=controller.entryFontSize)
        self.signupPswdEntry.place(
            x=convertSize(controller, 536),
            y=convertSize(controller, 385) + controller.entryDiscrenpancy,
            width=convertSize(controller, 528),
            height=controller.entryHeight,
        )
        # ------

        # ---Entry Bank number---
        self.signupBankBg = self.canvas.create_image(
            convertSize(controller, 800),
            convertSize(controller, 590),
            image=self.ImgSignupEntry,
        )
        self.signupBankEntry = tk.Entry(master=self,
                                        bd=0,
                                        bg="#ffffff",
                                        highlightthickness=0,
                                        font=controller.entryFontSize)
        self.signupBankEntry.place(
            x=convertSize(controller, 536),
            y=convertSize(controller, 546) + controller.entryDiscrenpancy,
            width=convertSize(controller, 528),
            height=controller.entryHeight,
        )

        # ---Submit button---
        self.submitBtn = tk.Button(master=self,
                                   image=self.ImgSubmitBtn,
                                   borderwidth=0,
                                   highlightthickness=0,
                                   command=self.Submit,
                                   relief="flat").place(
                                       x=convertSize(controller, 520),
                                       y=convertSize(controller, 705),
                                       width=convertSize(controller, 560),
                                       height=convertSize(controller, 88))

    def Submit(self):
        username = self.signupUserEntry.get()
        password = self.signupPswdEntry.get()
        bank = self.signupBankEntry.get()
        print(username, password, bank)
        valid, pop_up = Register(client, username, password, bank)
        print(pop_up)
        if not valid:
            messagebox.showinfo("Invalid input", pop_up)
        else: messagebox.showinfo("Register status", pop_up)


if __name__ == "__main__":
    connected = True
    app = App()
    app.mainloop()
