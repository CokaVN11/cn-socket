import tkinter as tk
from tkinter import messagebox
from math import floor, ceil
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
        self.hotel_list = {}

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry(self.resolution)
        # self.configure(bg="#ffffff")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginFrame, SignupFrame, MenuFrame, HotelListFrame):
            page_name = F.__name__
            if page_name != HotelListFrame.__name__:
                frame = F(parent=container, controller=self)
                self.frames[page_name] = frame

                frame.grid(row=0, column=0, sticky="nsew")
            else:
                self.frames[page_name] = None

        # self.frame = HotelListFrame(parent=container, controller=self)
        # self.frame.grid(row=0, column=0, sticky="nsew")
        # self.frame.go_to_page(1)
        self.show_frame("MenuFrame")

    def on_closing(self):
        # print(self.username)
        # print(self.hotel_list)
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

    def show_hotel_list(self, container):
        self.frames["HotelListFrame"] = HotelListFrame(parent=container, controller=self)
        self.frames["HotelListFrame"].grid(row=0, column=0, sticky="nsew")
        self.frames["HotelListFrame"].tkraise()


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
        self.__create_widgets(parent, controller)

    def __create_widgets(self, parent, controller):
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
                                  highlightthickness=0, command=lambda: self.HotelListClicked(parent), relief="flat")
        self.HotelBtn.place(x=convert_size(controller, 163), y=convert_size(controller, 50),
                            width=convert_size(controller, 182), height=convert_size(controller, 258))
        # ------

    def HotelListClicked(self, parent):
        # username = self.controller.username
        self.controller.hotel_list = ShowHotelList(client)
        self.controller.show_hotel_list(parent)

    def ReservationClicked(self):
        username = self.controller.username
        ShowBooked(client, username)

    def LogoutClicked(self):
        self.controller.username = ""
        self.controller.show_frame("LoginFrame")


class CardFrame(tk.Frame):
    def __init__(self, parent, controller, column, card_name, card_description, card_status, card_thumbnail_path):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # ---CARD Constants---
        self.canvas_width = convert_size(controller, 423)
        self.canvas_height = convert_size(controller, 564)

        self.name_x = convert_size(controller, 103 - 81)
        self.name_y = convert_size(controller, 270 - 4)

        self.desc_x = convert_size(controller, 103 - 81)
        self.desc_y = convert_size(controller, 500 - 163 - 12)

        # self.tag_available_x = convert_size(controller, (324 - 81) + (161 / 2))
        # self.tag_available_y = convert_size(controller, (364 - 163) + (42 / 2))
        # self.tag_full_x = convert_size(controller, (394 - 81) + (91 / 2))
        # self.tag_full_y = convert_size(controller, (364 - 163) + (42 / 2))

        self.btn_x = convert_size(controller, 289 - 81)
        self.btn_y = convert_size(controller, 644 - 163)

        self.thumbnail_x = convert_size(controller, 423 / 2)
        self.thumbnail_y = convert_size(controller, 564 / 2)

        self.column = column
        self.card_name = card_name
        self.card_description = card_description
        self.card_status = card_status
        self.thumbnail_path = card_thumbnail_path
        # ------
        self.__create_widgets(controller)

    def __create_widgets(self, controller):
        self.canvas = tk.Canvas(self, bg="#ffffff",
                                height=self.canvas_height, width=self.canvas_width,
                                bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        # ---Declare image---
        self.ImgThumbnail = convert_image(controller, self.thumbnail_path, 423, 564)
        self.ImgAvailable = convert_image(controller, "./assets/LOH_Available.png", 161, 42)
        self.ImgFull = convert_image(controller, "./assets/LOH_Full.png", 91, 42)
        self.ImgLookupBtn = convert_image(controller, "./assets/LOH_LookupBtn.png", 197, 65)
        self.ImgDisLookupBtn = convert_image(controller, "./assets/LOH_LookupDisabled.png", 197, 65)
        # ------
        self.card_thumbnail = self.canvas.create_image(self.thumbnail_x,
                                                       self.thumbnail_y,
                                                       image=self.ImgThumbnail)
        # if self.card_status:
        #     # Tag available
        #     self.card_tag = self.canvas.create_image(self.tag_available_x, self.tag_available_y,
        #                                              image=self.ImgAvailable)
        
        # Button Lookup
        self.lookupBtn = tk.Button(master=self, image=self.ImgLookupBtn, borderwidth=0, highlightthickness=0,
                                    command=lambda: btn_clicked(), relief="flat")
        self.lookupBtn.place(x=self.btn_x, y=self.btn_y, width=convert_size(controller, 197),
                                height=convert_size(controller, 65))
        # else:
        #     # Tag Full
        #     self.card_tag = self.canvas.create_image(self.tag_full_x, self.tag_full_y,
        #                                              image=self.ImgFull)
        #     # Button Lookup Disable
        #     self.lookupBtn = tk.Button(master=self, image=self.ImgDisLookupBtn, borderwidth=0, highlightthickness=0,
        #                                relief="flat")
        #     self.lookupBtn.place(x=self.btn_x, y=self.btn_y, width=convert_size(controller, 197),
        #                          height=convert_size(controller, 65))

        # Card name
        self.name_label = tk.Label(master=self, text=self.card_name, foreground="#47423D", background="white",
                                   font=("Noto Sans Bold", convert_size(controller, 28)))
        self.name_label.place(x=self.name_x, y=self.name_y)
        # ------
        # Card description
        self.desc_label = tk.Label(master=self, text=self.card_description, foreground="#7D8693",
                                   background="white", justify=tk.LEFT,
                                   font=("Hind Guntur Medium", convert_size(controller, 16)))
        self.desc_label.place(x=self.desc_x, y=self.desc_y)
        # ------


class HotelPageFrame(tk.Frame):
    def __init__(self, parent, window, controller, page_number, hotel_list):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # ---Card constants---
        self.card_width = convert_size(window, 423)
        self.card_height = convert_size(window, 564)
        self.first_card_x = convert_size(window, 81)
        self.first_card_y = convert_size(window, 163)
        self.card_discrepancy = convert_size(window, 588 - 81)
        # ------

        self.page_number = page_number
        self.hotels = hotel_list

        self.__create_widgets(parent, window, controller)

    def __create_widgets(self, parent, window, controller):
        self.canvas = tk.Canvas(self, bg="#ffffff",
                                height=window.frameHeight, width=window.frameWidth,
                                bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # ---Button Back---
        self.ImgBackBtn = convert_image(window, "./assets/LOH_BackButton.png", 177, 55)
        self.BackBtn = tk.Button(master=self, image=self.ImgBackBtn, borderwidth=0,
                                 highlightthickness=0, command=lambda: window.show_frame("MenuFrame"), relief="flat")
        self.BackBtn.place(x=convert_size(window, 38), y=convert_size(window, 40),
                           width=convert_size(window, 177), height=convert_size(window, 55))
        # ------
        self.cards = {}
        column = 0
        for i in self.hotels:
            self.cards[i['ID']] = CardFrame(self, window, i['ID'], i['NAME'], f"{i['DESC']} {self.page_number}", int(i['AVAILABLE']), "./assets/LOH_thumbnail1.png")
            self.cards[i['ID']].place(x=self.first_card_x + self.card_discrepancy * column, y=self.first_card_y, width=self.card_width, height=self.card_height)
            column += 1

        # ---Declare button image---
        self.ImgUnclick = convert_image(window, "./assets/LOH_Unclicked.png", 76, 76)
        self.ImgClicked = convert_image(window, "./assets/LOH_Clicked.png", 76, 76)
        # ------

        # ---Pagination button---
        self.next_btn = tk.Button(master=self, text="NEXT", font=("Noto Sans SemiBold", convert_size(window, 16)), image=self.ImgClicked, compound=tk.CENTER,
                                  borderwidth=0, highlightthickness=0, command=lambda: controller.go_to_page(self.page_number+1), relief="flat")
        self.prev_btn = tk.Button(master=self, text="PREV", font=("Noto Sans SemiBold", convert_size(window, 16)), image=self.ImgClicked, compound=tk.CENTER,
                                  borderwidth=0, highlightthickness=0, command=lambda: controller.go_to_page(self.page_number-1), relief="flat")

        self.page_label = tk.Label(master=self, text=f"{self.page_number}", image=self.ImgClicked, compound=tk.CENTER, font=("Noto Sans SemiBold", convert_size(window, 16)))
        self.page_label.place(x=convert_size(window, 506 + 102*2), y=convert_size(window, 780),
                              width=convert_size(window, 76), height=convert_size(window, 76))
        self.next_btn.place(x=convert_size(window, 506 + 102*3), y=convert_size(window, 780),
                            width=convert_size(window, 76), height=convert_size(window, 76))
        self.prev_btn.place(x=convert_size(window, 506 + 102*1), y=convert_size(window, 780),
                            width=convert_size(window, 76), height=convert_size(window, 76))

    def Back(self):
        self.controller.show_frame("MenuFrame")


class HotelListFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.hotel_list = self.controller.hotel_list

        self.begin_page = 1
        self.end_page = ceil(len(self.hotel_list)/3)
        print(self.begin_page, self.end_page)
        self.__create_widgets_(controller)

    def __create_widgets_(self, controller):
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in range(self.begin_page, self.end_page+1):
            mini_hotel_list = self.hotel_list[F*3 - 3:F*3 - 3 +3]
            print(mini_hotel_list)
            frame = HotelPageFrame(parent=container, window=controller, controller=self, page_number=F, hotel_list=mini_hotel_list)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.go_to_page(self.begin_page)

    def go_to_page(self, page_number):
        if page_number < self.begin_page or page_number > self.end_page:
            messagebox.showerror("Error", "Page not exist")
        else:
            print(f"Go to {page_number}")
            frame = self.frames[page_number]
            frame.tkraise()


if __name__ == "__main__":
    connected = True
    app = App()
    app.mainloop()
