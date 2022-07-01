import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from math import floor
from PIL import Image, ImageTk


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


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('Go2Chill')
        self.scaleRate = 0.8

        self.frameWidth = floor(self.winfo_screenwidth() * self.scaleRate)
        self.frameHeight = floor(self.frameWidth * 9 / 16)
        self.fontSize = convertSize(self, 40)
        self.resolution = f"{self.frameWidth}x{self.frameHeight}"

        self.entryHeight = convertSize(self, 60)
        self.entryFontSize = f"{convertSize(self, 80)}"
        self.entryDiscrenpancy = convertSize(self, 12)

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
            frame = F(parent=container, master=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        '''Show a frame for the given name'''
        print(f"Show {page_name}")
        frame = self.frames[page_name]
        frame.lift()


class LoginFrame(tk.Frame):

    def __init__(self, parent, master):
        tk.Frame.__init__(self, parent)
        self.controller = master
        self.__create_widgets(master)

    def __create_widgets(self, master):
        # self.pack(fill=tk.BOTH, expand=1)
        self.canvas = tk.Canvas(self,
                           bg="#ffffff",
                           height=master.frameHeight,
                           width=master.frameWidth,
                           bd=0,
                           highlightthickness=0,
                           relief="ridge")
        self.canvas.place(x=0, y=0)
        # ---Image---
        self.ImgLoginBg = convertImage(master, "./assets/Login_Background.png",
                                       1448, 900)
        self.ImgEntry = convertImage(master, "./assets/Login_Entry.png", 510,
                                     84)
        self.ImgLoginBtn = convertImage(master,
                                        "./assets/Login_LoginButton.png", 510,
                                        84)
        self.ImgSingupBtn = convertImage(master,
                                         "./assets/Login_SignupButton.png",
                                         129, 38)
        # ------

        # ---Background---
        self.LoginBg = self.canvas.create_image(convertSize(master, 724),
                                           convertSize(master, 450),
                                           image=self.ImgLoginBg)

        # ---Entry username---
        self.UserEntryBg = self.canvas.create_image(
            convertSize(master, 1201),
            convertSize(master, 304),
            image=self.ImgEntry,
        )
        self.UserEntry = tk.Entry(bd=0,
                                  bg="#ffffff",
                                  highlightthickness=0,
                                  font=master.entryFontSize)
        self.UserEntry.place(
            x=convertSize(master, 962),
            y=convertSize(master, 262) + master.entryDiscrenpancy,
            width=convertSize(master, 478),
            height=master.entryHeight,
        )
        # ------

        # ---Entry password---
        self.PswdEntryBg = self.canvas.create_image(
            convertSize(master, 1201),
            convertSize(master, 459),
            image=self.ImgEntry,
        )
        self.PswdEntry = tk.Entry(bd=0,
                                  bg="#ffffff",
                                  highlightthickness=0,
                                  font=master.entryFontSize)
        self.PswdEntry.place(
            x=convertSize(master, 962),
            y=convertSize(master, 417) + master.entryDiscrenpancy,
            width=convertSize(master, 478),
            height=master.entryHeight,
        )
        # ------

        # --- BUTTON "Login" ---
        self.LoginLoginBtn = tk.Button(
            image=self.ImgLoginBtn,
            borderwidth=0,
            highlightthickness=0,
            command=self.submitLogin,
            relief="flat",
        ).place(
            x=convertSize(master, 946),
            y=convertSize(master, 572),
            width=convertSize(master, 510),
            height=convertSize(master, 84),
        )
        # ------
        # --- BUTTON "Create one" ---
        self.LoginSignupBtn = tk.Button(
            image=self.ImgSingupBtn,
            borderwidth=0,
            highlightthickness=0,
            command=self.createOne,
            relief="flat",
        ).place(
            x=convertSize(master, 1302),
            y=convertSize(master, 788),
            width=convertSize(master, 129),
            height=convertSize(master, 38),
        )
        # ------

    def submitLogin(self):
        usernameInput = self.UserEntry.get()
        passwordInput = self.PswdEntry.get()
        print(usernameInput, passwordInput)

    def createOne(self):
        # master.clearScreen()
        # SignupScreen(master)
        print("get other")
        self.controller.__show_frame("SignupFrame")

        # label = ttk.Label(self, text="Hello").place(x=5,y=5)


class SignupFrame(tk.Frame):

    def __init__(self, parent, master):
        tk.Frame.__init__(self, parent)
        self.controller = master
        self.__create_widgets(master)

    def __create_widgets(self, master):
        # self.pack(fill=tk.BOTH, expand=1)
        canvas = tk.Canvas(
            self,
            bg="#ffffff",
            height=master.frameHeight,
            width=master.frameWidth,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.place(x=0, y=0)
        self.ImgSignupBg = convertImage(master,
                                        "./assets/Signup_Background.png", 547,
                                        470)
        self.ImgSignupEntry = convertImage(master, "./assets/Signup_Entry.png",
                                           560, 88)
        self.ImgBackBtn = convertImage(master,
                                       "./assets/Signup_BackButton.png", 228,
                                       61)
        self.ImgSubmitBtn = convertImage(master,
                                         "./assets/Signup_SubmitButton.png",
                                         560, 88)
        # ------

        # ---Background---
        self.SignupBg = canvas.create_image(
            convertSize(master, 806.5),
            convertSize(master, 303.0),
            image=self.ImgSignupBg,
        )
        # ------

        # ---BUTTON "Back"---
        self.signupBackBtn = tk.Button(
            image=self.ImgBackBtn,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.Back,
            relief="flat",
        ).place(
            x=convertSize(master, 24),
            y=convertSize(master, 20),
            width=convertSize(master, 228),
            height=convertSize(master, 61),
        )
        # ------

        # ---Entry username---
        self.signupUserBg = canvas.create_image(
            convertSize(master, 800),
            convertSize(master, 270),
            image=self.ImgSignupEntry,
        )
        self.signupUserEntry = tk.Entry(bd=0,
                                        bg="#ffffff",
                                        highlightthickness=0,
                                        font=master.entryFontSize)
        self.signupUserEntry.place(
            x=convertSize(master, 536),
            y=convertSize(master, 226) + master.entryDiscrenpancy,
            width=convertSize(master, 528),
            height=master.entryHeight,
        )
        # ------

        # ---Entry password---
        self.signupPswdBg = canvas.create_image(
            convertSize(master, 800),
            convertSize(master, 429),
            image=self.ImgSignupEntry,
        )
        self.signupPswdEntry = tk.Entry(bd=0,
                                        bg="#ffffff",
                                        highlightthickness=0,
                                        font=master.entryFontSize)
        self.signupPswdEntry.place(
            x=convertSize(master, 536),
            y=convertSize(master, 385) + master.entryDiscrenpancy,
            width=convertSize(master, 528),
            height=master.entryHeight,
        )
        # ------

        # ---Entry Bank number---
        self.signupBankBg = canvas.create_image(
            convertSize(master, 800),
            convertSize(master, 590),
            image=self.ImgSignupEntry,
        )
        self.signupBankEntry = tk.Entry(bd=0,
                                        bg="#ffffff",
                                        highlightthickness=0,
                                        font=master.entryFontSize)
        self.signupBankEntry.place(
            x=convertSize(master, 536),
            y=convertSize(master, 546) + master.entryDiscrenpancy,
            width=convertSize(master, 528),
            height=master.entryHeight,
        )

        # ---Submit button---
        self.submitBtn = tk.Button(image=self.ImgSubmitBtn,
                                   borderwidth=0,
                                   highlightthickness=0,
                                   command=self.Submit,
                                   relief="flat").place(
                                       x=convertSize(master, 520),
                                       y=convertSize(master, 705),
                                       width=convertSize(master, 560),
                                       height=convertSize(master, 88))

    def Submit(self):
        username = self.signupUserEntry.get()
        password = self.signupPswdEntry.get()
        bank = self.signupBankEntry.get()
        print(username, password, bank)

    def Back(self):
        self.controller.show_frame("LoginFrame")


if __name__ == "__main__":
    app = App()
    app.mainloop()
