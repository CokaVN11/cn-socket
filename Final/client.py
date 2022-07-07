import tkinter as tk
from tkinter import messagebox
from math import floor, ceil
from PIL import Image, ImageTk
from client_method import *
from tkcalendar import Calendar


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
        self.bank = ""
        self.hotel_list = {}
        self.reserve_list = {}
        self.booking_list = []

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry(self.resolution)
        self.iconbitmap(r"./assets/booking.ico")
        # self.configure(bg="#ffffff")
        self.resizable(False, False)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginFrame, SignupFrame, MenuFrame, HotelListFrame, ReservationPageFrame):
            page_name = F.__name__
            if page_name != HotelListFrame.__name__ and page_name != ReservationPageFrame.__name__:
                frame = F(parent=self.container, controller=self)
                self.frames[page_name] = frame

                frame.grid(row=0, column=0, sticky="nsew")
            else:
                self.frames[page_name] = None

        # self.show_frame("LoginFrame")
        self.show_frame("LoginFrame")

    def on_closing(self):
        print(QUIT_MSG)
        for room in self.booking_list:
            print(room)
        send_s(client, QUIT_MSG)
        client.close()
        self.quit()

    def show_frame(self, page_name):
        """Show a frame for the given name"""
        print(f"Show {page_name}")
        frame = self.frames[page_name]
        frame.tkraise()

    def show_hotel_list(self, container):
        if self.frames["HotelListFrame"] is None:
            self.frames["HotelListFrame"] = HotelListFrame(parent=container, controller=self)
            self.frames["HotelListFrame"].grid(row=0, column=0, sticky="nsew")
        self.frames["HotelListFrame"].tkraise()

    def show_reserve_list(self, container):
        if self.frames["ReservationPageFrame"] is None:
            self.frames["ReservationPageFrame"] = ReservationPageFrame(parent=container,
                                                                       controller=self,
                                                                       window=self,
                                                                       reserve_list=self.reserve_list)
            self.frames["ReservationPageFrame"].grid(row=0, column=0, sticky="nsew")
        self.frames["ReservationPageFrame"].tkraise()


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
        self.LoginBg = self.canvas.create_image(convert_size(controller, 724),
                                                convert_size(controller, 450),
                                                image=self.ImgLoginBg)

        # ---Entry username---
        self.UserEntryBg = self.canvas.create_image(convert_size(controller, 1201),
                                                    convert_size(controller, 304),
                                                    image=self.ImgEntry
                                                    )
        self.UserEntry = tk.Entry(master=self, bd=0, bg="#ffffff", highlightthickness=0, font=controller.entryFontSize)
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
            master=self, image=self.ImgLoginBtn,
            borderwidth=0, highlightthickness=0,
            command=self.submitLogin, relief="flat",
        )
        self.LoginLoginBtn.place(
            x=convert_size(controller, 946), y=convert_size(controller, 572),
            width=convert_size(controller, 510), height=convert_size(controller, 84),
        )
        # ------
        # --- BUTTON "Create one" ---
        self.LoginSignupBtn = tk.Button(
            master=self, image=self.ImgSignupBtn, borderwidth=0, highlightthickness=0,
            command=lambda: controller.show_frame("SignupFrame"), relief="flat",
        )
        self.LoginSignupBtn.place(
            x=convert_size(controller, 1302), y=convert_size(controller, 788),
            width=convert_size(controller, 129), height=convert_size(controller, 38),
        )
        # ------

    def submitLogin(self):
        username_input = self.UserEntry.get()
        password_input = self.PswdEntry.get()
        print(username_input, password_input)
        valid, pop_up, username, bank = Login(client, username_input, password_input)
        print(pop_up)
        if not valid:
            messagebox.showwarning("Invalid input", pop_up)
        else:
            messagebox.showinfo("Login status", pop_up)
            if username:
                self.controller.username = username
                self.controller.bank = bank
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
                                        highlightthickness=0, command=lambda: self.ReservationClicked(parent),
                                        relief="flat")
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

    def ReservationClicked(self, parent):
        username = self.controller.username
        self.controller.reserve_list = ShowBooked(client, username)
        self.controller.show_reserve_list(parent)

    def LogoutClicked(self):
        self.controller.username = ""
        self.controller.bank = ""
        self.controller.hotel_list = {}
        self.controller.reserve_list = {}
        self.controller.booking_list = {}
        self.controller.show_frame("LoginFrame")


class CardHotelFrame(tk.Frame):
    def __init__(self, parent, controller, window, column, card_name, card_description, card_status,
                 card_thumbnail_path, hotel_page):
        tk.Frame.__init__(self, parent)
        self.popup_screen = None
        self.window = window
        self.controller = controller
        self.parent = parent
        self.hotel_page = hotel_page

        # ---CARD Constants---
        self.canvas_width = convert_size(window, 423)
        self.canvas_height = convert_size(window, 564)

        self.name_x = convert_size(window, 103 - 81)
        self.name_y = convert_size(window, 270 - 4)

        self.desc_x = convert_size(window, 103 - 81)
        self.desc_y = convert_size(window, 500 - 163 - 12)

        self.btn_x = convert_size(window, 289 - 81)
        self.btn_y = convert_size(window, 644 - 163)

        self.thumbnail_x = convert_size(window, 423 / 2)
        self.thumbnail_y = convert_size(window, 564 / 2)

        self.column = column
        self.card_name = card_name
        self.card_description = card_description
        self.card_status = card_status
        self.thumbnail_path = card_thumbnail_path
        # ------
        self.__create_widgets(window)

    def __create_widgets(self, window):
        self.canvas = tk.Canvas(self, bg="#ffffff",
                                height=self.canvas_height, width=self.canvas_width,
                                bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        # ---Declare image---
        self.ImgThumbnail = convert_image(window, self.thumbnail_path, 423, 564)
        self.ImgAvailable = convert_image(window, "./assets/LOH_Available.png", 161, 42)
        self.ImgFull = convert_image(window, "./assets/LOH_Full.png", 91, 42)
        self.ImgLookupBtn = convert_image(window, "./assets/LOH_LookupBtn.png", 197, 65)
        self.ImgDisLookupBtn = convert_image(window, "./assets/LOH_LookupDisabled.png", 197, 65)
        # ------
        self.card_thumbnail = self.canvas.create_image(self.thumbnail_x,
                                                       self.thumbnail_y,
                                                       image=self.ImgThumbnail)

        # Button Lookup
        self.lookupBtn = tk.Button(master=self, image=self.ImgLookupBtn, borderwidth=0,
                                   highlightthickness=0, command=lambda: self.popup_date(), relief="flat")
        self.lookupBtn.place(x=self.btn_x, y=self.btn_y, width=convert_size(window, 197),
                             height=convert_size(window, 65))
        # Card name
        self.name_label = tk.Label(master=self, text=self.card_name, foreground="#47423D", background="white",
                                   font=("Noto Sans Bold", convert_size(window, 28)))
        self.name_label.place(x=self.name_x, y=self.name_y)
        # ------
        # Card description
        self.desc_label = tk.Label(master=self, text=self.card_description, foreground="#7D8693",
                                   background="white", justify=tk.LEFT,
                                   font=("Hind Guntur Medium", convert_size(window, 16)))
        self.desc_label.place(x=self.desc_x, y=self.desc_y)
        # ------

    def popup_date(self):
        self.popup_screen = DatePopup(self, self.window)
        self.wait_window(self.popup_screen.top)
        room_list = LookUpRoom(client, self.card_name, self.arrival_value(), self.depart_value())
        if room_list is not None:
            self.controller.show_room_frame(room_list, self.card_name, self.hotel_page, self.arrival_value(),
                                            self.depart_value())

    def arrival_value(self):
        return self.popup_screen.arrival_date

    def depart_value(self):
        return self.popup_screen.depart_date


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

        self.__create_widgets(window, controller)

    def __create_widgets(self, window, controller):
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

        # ---Hotel Card---
        self.cards = {}
        column = 0
        for i in self.hotels:
            self.cards[i['ID']] = CardHotelFrame(self, controller, window, i['ID'], i['NAME'],
                                                 f"{i['DESC']} {self.page_number}",
                                                 int(i['AVAILABLE']), "./assets/LOH_thumbnail1.png", self.page_number)
            self.cards[i['ID']].place(x=self.first_card_x + self.card_discrepancy * column, y=self.first_card_y,
                                      width=self.card_width, height=self.card_height)
            column += 1

        # ---Declare button image---
        self.ImgUnclick = convert_image(window, "./assets/LOH_Unclicked.png", 76, 76)
        self.ImgClicked = convert_image(window, "./assets/LOH_Clicked.png", 76, 76)
        # ------

        # ---Pagination button---
        self.next_btn = tk.Button(master=self, text="NEXT", font=("Noto Sans SemiBold", convert_size(window, 16)),
                                  image=self.ImgClicked, compound=tk.CENTER,
                                  borderwidth=0, highlightthickness=0,
                                  command=lambda: controller.go_to_page(self.page_number + 1), relief="flat")
        self.prev_btn = tk.Button(master=self, text="PREV", font=("Noto Sans SemiBold", convert_size(window, 16)),
                                  image=self.ImgClicked, compound=tk.CENTER,
                                  borderwidth=0, highlightthickness=0,
                                  command=lambda: controller.go_to_page(self.page_number - 1), relief="flat")

        self.page_label = tk.Label(master=self, text=f"{self.page_number}", image=self.ImgClicked, compound=tk.CENTER,
                                   font=("Noto Sans SemiBold", convert_size(window, 16)))
        self.page_label.place(x=convert_size(window, 506 + 102 * 2), y=convert_size(window, 780),
                              width=convert_size(window, 76), height=convert_size(window, 76))
        self.next_btn.place(x=convert_size(window, 506 + 102 * 3), y=convert_size(window, 780),
                            width=convert_size(window, 76), height=convert_size(window, 76))
        self.prev_btn.place(x=convert_size(window, 506 + 102 * 1), y=convert_size(window, 780),
                            width=convert_size(window, 76), height=convert_size(window, 76))

    def Back(self):
        self.controller.show_frame("MenuFrame")


class HotelListFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cart_frame = None
        self.controller = controller

        self.hotel_list = self.controller.hotel_list
        self.room_frame = None

        self.begin_page = 1
        self.end_page = ceil(len(self.hotel_list) / 3)
        print(self.begin_page, self.end_page)
        self.__create_widgets_(controller)

    def __create_widgets_(self, controller):
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in range(self.begin_page, self.end_page + 1):
            mini_hotel_list = self.hotel_list[F * 3 - 3:F * 3]
            print(mini_hotel_list)
            frame = HotelPageFrame(parent=self.container, window=controller, controller=self, page_number=F,
                                   hotel_list=mini_hotel_list)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(master=self, text=f"{self.controller.username}",
                 font=("Noto Sans SemiBold", 20), background="#ffffff").place(x=convert_size(controller, 1420),
                                                                              y=convert_size(controller, 40))
        self.go_to_page(self.begin_page)

    def go_to_page(self, page_number):
        if page_number < self.begin_page or page_number > self.end_page:
            messagebox.showerror("Error", "Page not exist")
        else:
            print(f"Go to {page_number}")
            frame = self.frames[page_number]
            frame.tkraise()

    def show_room_frame(self, room_list, hotel_name, previous_page, arrival_date, depart_date):
        self.room_frame = RoomPageFrame(parent=self.container, controller=self, window=self.controller,
                                        hotel_name=hotel_name, room_list=room_list, previous_frame=previous_page,
                                        arrival_date=arrival_date, depart_date=depart_date)
        self.room_frame.grid(row=0, column=0, sticky="nsew")
        self.room_frame.tkraise()

    def show_cart_frame(self, reserve_list):
        if len(reserve_list) <= 0:
            messagebox.showinfo("Info", "You are not booking any room")
            return
        self.cart_frame = CartPageFrame(parent=self.container, controller=self.room_frame, window=self.controller,
                                        reserve_list=reserve_list)
        self.cart_frame.grid(row=0, column=0, sticky="nsew")
        self.cart_frame.tkraise()


class DatePopup:
    def __init__(self, master, window):

        self.top = tk.Toplevel(master)
        # print("Pop up")
        self.depart_date = None
        self.arrival_date = None

        self.current_time = datetime.datetime.now()
        self.arrival_chose = False
        self.depart_chose = False

        # ---Arrival calendar---
        # --Title--
        self.arrival_title = tk.Label(self.top, text="CHOOSE ARRIVAL DATE: ",
                                      font=("Noto Sans Bold", convert_size(window, 16)))
        self.arrival_title.grid(row=0, column=0, pady=10)

        # --Calendar--
        self.arrival_calendar = Calendar(self.top, selectmode='day', font=f"{convert_size(window, 14)}",
                                         year=self.current_time.year, month=self.current_time.month,
                                         day=self.current_time.day, date_pattern="dd/mm/yyyy",
                                         showweeknumbers=0, borderwidth=0, background="white", foreground="gray1",
                                         selectbackground="#1294F2", selectforeground="ghost white",
                                         headersbackground="white", headersforeground="black",
                                         cursor="hand2", relief="ridge")
        self.arrival_calendar.grid(row=1, column=0, padx=12)

        # --Label--
        self.arrival_label = tk.Label(self.top, text="", font=("Noto Sans Bold", convert_size(window, 14)))
        self.arrival_label.grid(row=2, column=0, pady=20)

        # --Button--
        self.arrival_btn = tk.Button(self.top, text="Choose", font=("Noto Sans Bold", convert_size(window, 20)),
                                     command=lambda: self.show_arrival_date(), relief="ridge")
        self.arrival_btn.grid(row=3, column=0)

        # ---Departure calendar---
        # --Title--
        self.departure_title = tk.Label(self.top, text="CHOOSE DEPARTURE DATE: ",
                                        font=("Noto Sans Bold", convert_size(window, 16)))
        self.departure_title.grid(row=0, column=2, pady=10)

        # --Calendar--
        self.depart_calendar = Calendar(self.top, selectmode='day', font=f"{convert_size(window, 14)}",
                                        year=self.current_time.year, month=self.current_time.month,
                                        day=self.current_time.day + 3, date_pattern="dd/mm/yyyy",
                                        showweeknumbers=0, borderwidth=0, background="white", foreground="gray1",
                                        selectbackground="#1294F2", selectforeground="ghost white",
                                        headersbackground="white", headersforeground="black",
                                        cursor="hand2", relief="ridge")
        self.depart_calendar.grid(row=1, column=2, padx=12)
        # --Label--
        self.depart_label = tk.Label(self.top, text="", font=("Noto Sans Bold", convert_size(window, 14)))
        self.depart_label.grid(row=2, column=2, pady=20)
        # --Button--
        self.depart_btn = tk.Button(self.top, text="Choose", font=("Noto Sans Bold", convert_size(window, 20)),
                                    command=lambda: self.show_depart_date(), relief="ridge")
        self.depart_btn.grid(row=3, column=2)
        # ------

        # ---Confirm button---
        self.confirm_btn = tk.Button(self.top, text="Confirm", font=convert_size(window, 15),
                                     command=self.confirm_and_out, relief="ridge")
        self.confirm_btn.grid(row=4, column=1, pady=20)

        # ------

    def show_arrival_date(self):
        self.arrival_chose = True
        self.arrival_label.config(text=f"Selected Arrival Date: {self.arrival_calendar.get_date()}")

    def show_depart_date(self):
        self.depart_chose = True
        self.depart_label.config(text=f"Selected Departure Date: {self.depart_calendar.get_date()}")

    def confirm_and_out(self):
        self.arrival_date = self.arrival_calendar.get_date()
        self.depart_date = self.depart_calendar.get_date()

        if not self.arrival_chose:
            self.arrival_label.config(text="You haven't chosen Arrival Date")
            return
        if not self.depart_chose:
            self.depart_label.config(text="You haven't chosen Departure Date")
            return
        self.top.destroy()


class CardRoomFrame(tk.Frame):
    def __init__(self, parent, controller, window, room_id, card_name, card_description, room_vacancies, card_price,
                 card_thumbnail_path, card_bed, card_area, card_guest):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # ---Card constants---
        self.card_width = convert_size(window, 1354)
        self.card_height = convert_size(window, 324)

        self.canvas_width = convert_size(window, 1354)
        self.canvas_height = convert_size(window, 324)

        self.thumbnail_x = convert_size(window, 1354 / 2)
        self.thumbnail_y = convert_size(window, 324 / 2)

        self.name_x = convert_size(window, 619 - 123)
        self.name_y = convert_size(window, 186 - 155 - 26)

        self.desc_x = convert_size(window, 619 - 123)
        self.desc_y = convert_size(window, 253 - 155 - 4)

        self.price_x = convert_size(window, 1268 - 123 + 186)
        self.price_y = convert_size(window, 186 - 155 + 20)

        self.tag_available_x = convert_size(window, (401 - 123) + (161 / 2))
        self.tag_available_y = convert_size(window, (389 - 155) + (42 / 2))
        self.tag_full_x = convert_size(window, (471 - 123) + (91 / 2))
        self.tag_full_y = convert_size(window, (389 - 155) + (42 / 2))

        self.bed_x = convert_size(window, 670 - 123 - 4)
        self.bed_y = convert_size(window, 408 - 155 - 12)
        self.area_x = convert_size(window, 807 - 123 - 4)
        self.area_y = convert_size(window, 408 - 155 - 12)
        self.guest_x = convert_size(window, 938 - 123 - 4)
        self.guest_y = convert_size(window, 408 - 155 - 12)

        self.btn_x = convert_size(window, 1216 - 123)
        self.btn_y = convert_size(window, 380 - 155)

        self.room_id = room_id
        self.card_name = card_name
        self.description = card_description
        self.status = True
        if room_vacancies <= 0:
            self.status = False
        self.price = card_price
        self.thumbnail_path = card_thumbnail_path
        self.bed = card_bed
        self.area = card_area
        self.guest = card_guest
        # ------
        self.__create_widgets(window)

    def __create_widgets(self, window):
        self.canvas = tk.Canvas(master=self, bg="#ffffff", bd=0, highlightthickness=0, relief="ridge",
                                height=self.canvas_height, width=self.canvas_width)
        self.canvas.place(x=0, y=0)

        # ---Image declaration---
        self.ImgThumbnail = convert_image(window, "./assets/LK_room1_single.png", 1354, 324)
        self.ImgTagAvailable = convert_image(window, "./assets/LK_Available.png", 161, 42)
        self.ImgTagFull = convert_image(window, "./assets/LK_Full.png", 91, 42)
        self.ImgReserveBtn = convert_image(window, "./assets/LK_ReserveBtn.png", 234, 68)
        self.ImgReserveDis = convert_image(window, "./assets/LK_ReserveDisabled.png", 234, 68)

        # ---Card thumbnail---
        self.card_thumbnail = self.canvas.create_image(self.thumbnail_x,
                                                       self.thumbnail_y, image=self.ImgThumbnail)
        # ---Card status---
        if self.status:
            self.tag_available = self.canvas.create_image(self.tag_available_x, self.tag_available_y,
                                                          image=self.ImgTagAvailable)
        else:
            self.tag_full = self.canvas.create_image(self.tag_full_x, self.tag_full_y, image=self.ImgTagFull)
        # ---Card name---
        self.name_label = tk.Label(master=self, text=self.card_name, foreground="#47423D", background="#ffffff",
                                   font=("Noto Sans Bold", convert_size(window, 40)))
        self.name_label.place(x=self.name_x, y=self.name_y)
        # ---Card description---
        self.card_desc = tk.Label(master=self, text=self.description,
                                  foreground="#7D8693", background="#ffffff", justify=tk.LEFT,
                                  wraplength=convert_size(window, 600),
                                  font=("Hind Guntur Medium", convert_size(window, 18)))
        self.card_desc.place(x=self.desc_x, y=self.desc_y)
        # ---Card price---
        self.card_price = tk.Label(master=self, anchor="e", text=self.price,
                                   foreground="#35bdda", background="white",
                                   justify=tk.RIGHT, font=("Noto Sans Bold", convert_size(window, 50)),
                                   width=convert_size(window, 8))
        self.card_price.place(anchor="e", x=self.price_x, y=self.price_y, height=convert_size(window, 80))
        # ---Card bed---
        self.card_bed = tk.Label(master=self, text=f"{self.bed} Bed",
                                 foreground="#8f8f8f", background="#ffffff",
                                 justify=tk.LEFT, font=("Noto Sans Regular", convert_size(window, 18)))
        self.card_bed.place(x=self.bed_x, y=self.bed_y)
        # ---Card area---
        self.card_area = tk.Label(master=self, text=f"{self.area} m2",
                                  foreground="#8f8f8f", background="#ffffff",
                                  justify=tk.LEFT, font=("Noto Sans Regular", convert_size(window, 18)))
        self.card_area.place(x=self.area_x, y=self.area_y)
        # ---Card guest---
        self.card_guest = tk.Label(master=self, text=f"{self.guest} Guest",
                                   foreground="#8f8f8f", background="#ffffff",
                                   justify=tk.LEFT, font=("Noto Sans Regular", convert_size(window, 18)))
        self.card_guest.place(x=self.guest_x, y=self.guest_y)
        # ---Reserve Button---
        if self.status:
            self.reserve_btn = tk.Button(master=self, image=self.ImgReserveBtn, borderwidth=0,
                                         highlightthickness=0, relief="flat",
                                         command=lambda: self.__Reserve_clicked(window))
            self.reserve_btn.place(x=self.btn_x, y=self.btn_y,
                                   width=convert_size(window, 234), height=convert_size(window, 68))
        else:
            self.reserve_btn = tk.Button(master=self, image=self.ImgReserveDis, borderwidth=0,
                                         highlightthickness=0, command=lambda: btn_clicked(), relief="flat")
            self.reserve_btn.place(x=self.btn_x, y=self.btn_y,
                                   width=convert_size(window, 234), height=convert_size(window, 68))

    def __Reserve_clicked(self, window):
        window.booking_list.append({
            "ID": self.room_id,
            "Hotel Name": self.controller.hotel_name,
            "Room type": self.card_name,
            "Arrival": self.controller.arrival,
            "Depart": self.controller.depart,
            "Price": self.price,
            "Quantity": 1,
            "Thumbnail": "#Thumbnail"
        })


class RoomPageFrame(tk.Frame):
    def __init__(self, parent, controller, window, hotel_name, room_list, previous_frame, arrival_date, depart_date):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.previous_frame = previous_frame
        self.room_list = room_list
        self.hotel_name = hotel_name
        self.arrival = arrival_date
        self.depart = depart_date
        self.number_items = len(room_list)
        self.scroll_frame_height = convert_size(window, 155 + self.number_items * 367)
        # ---Card constants---
        self.card_width = convert_size(window, 1354)
        self.card_height = convert_size(window, 324)

        self.first_x = convert_size(window, 123)
        self.first_y = convert_size(window, 155)
        self.card_discrepancy = convert_size(window, 522 - 155)

        self.__create_widgets(window)

    def __create_widgets(self, window):
        self.canvas = tk.Canvas(master=self, bg="#ffffff", bd=0,
                                height=window.frameHeight, width=window.frameWidth,
                                highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # ---Scroll Bar---
        self.scroll_bar = tk.Scrollbar(master=self, orient="vertical",
                                       command=self.canvas.yview)
        self.scroll_bar.pack(side=tk.RIGHT, fill="y")

        self.scrollable_frame = tk.Frame(master=self.canvas,
                                         width=window.frameWidth, height=self.scroll_frame_height,
                                         bg="#ffffff")
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.canvas.configure(
                                       scrollregion=self.canvas.bbox("all")
                                   ))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)

        self.container = tk.Frame(master=self.scrollable_frame,
                                  width=window.frameWidth, height=self.scroll_frame_height,
                                  bg="#ffffff")
        self.container.place(x=0, y=0)

        # ---Back button---
        self.ImgBackBtn = convert_image(window, "./assets/LK_BackBtn.png", 227, 55)
        self.back_btn = tk.Button(master=self.container, image=self.ImgBackBtn, borderwidth=0, relief="ridge",
                                  highlightthickness=0, command=lambda: self.Back())
        self.back_btn.place(x=convert_size(window, 41), y=convert_size(window, 44),
                            width=convert_size(window, 227), height=convert_size(window, 55))
        # ---Cart button---
        self.ImgCartBtn = convert_image(window, "./assets/LK_Cart.png", 109, 109)
        self.cart_btn = tk.Button(master=self.container, image=self.ImgCartBtn, borderwidth=0, relief="flat",
                                  highlightthickness=0,
                                  command=lambda: self.controller.show_cart_frame(window.booking_list))
        self.cart_btn.place(x=convert_size(window, 1462), y=convert_size(window, 30),
                            width=convert_size(window, 109), height=convert_size(window, 109))

        # ---Hotel name title---
        self.hotel_name_label = tk.Label(master=self.container, text=f"{self.hotel_name}",
                                         foreground="#47423D", background="#ffffff",
                                         justify=tk.CENTER, font=("Noto Sans SemiBold", convert_size(window, 50)))
        self.hotel_name_label.place(x=window.frameWidth / 2, y=convert_size(window, 84), anchor="center")

        self.cards = {}

        row = 0
        # ex_desc = ("", "", "")
        for room in self.room_list:
            self.cards[row] = CardRoomFrame(self.container, self, window, room['ID'], room['TYPE'], room['DESC'],
                                            room['VACANCIES'],
                                            room['PRICE'], "#Thumbnail",
                                            room['BED'], room['AREA'], room['GUEST'])
            self.cards[row].place(x=self.first_x, y=self.first_y + self.card_discrepancy * row,
                                  width=self.card_width, height=self.card_height)
            row += 1

    # This method will be call from the room card
    def ReserveClicked(self, window, room_id, room_price):
        total = GetMoneyStaying(self.arrival, self.depart, room_price)
        isOk = Booking(client=client, username=window.username, room_id=room_id,
                       quantity=1, arrival=self.arrival, departure=self.depart, total=total)
        if isOk:
            messagebox.showinfo("Booking", "Finish")
        else:
            messagebox.showinfo("Booking", "Fail")

    def Back(self):
        self.grid_forget()
        self.destroy()


class CardCartFrame(tk.Frame):
    def __init__(self, parent, controller, window, row, hotel_name, room_type,
                 arrival_date, departure_date, room_quantity, thumbnail, room_price):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.row = row
        self.hotel_name = hotel_name
        self.room_type = room_type
        self.arrival_date = arrival_date
        self.departure_date = departure_date
        self.room_quantity = room_quantity
        self.thumbnail = thumbnail
        self.room_price = room_price

        # ---Card constants---
        self.card_width = convert_size(window, 819)
        self.card_height = convert_size(window, 200)

        self.thumbnail_x = convert_size(window, 819 / 2)
        self.thumbnail_y = convert_size(window, 200 / 2)

        self.name_x = convert_size(window, 337 - 31 - 2)
        self.name_y = convert_size(window, 118 - 102 - 12)

        self.date_x = convert_size(window, 337 - 31 - 2)
        self.date_y = convert_size(window, 162 - 102 + 4)

        self.quantity_x = convert_size(window, 376 - 31 + 10)
        self.quantity_y = convert_size(window, 244 - 102 - 4 + 14)

        self.price_x = convert_size(window, 648 - 31 + 186)
        self.price_y = convert_size(window, 240 - 102 + 14)

        self.decrease_btn_x = convert_size(window, 339 - 31)
        self.decrease_btn_y = convert_size(window, 245 - 102)
        self.increase_btn_x = convert_size(window, 406 - 31)
        self.increase_btn_y = convert_size(window, 245 - 102)

        # ---Image declare---
        self.ImgThumbnail = convert_image(window, "./assets/Cart_thumbnail.png", 819, 200)
        self.ImgIncreaseBtn = convert_image(window, "./assets/Cart_increaseBtn.png", 28, 28)
        self.ImgDecreaseBtn = convert_image(window, "./assets/Cart_decreaseBtn.png", 28, 28)

        self.__create_widgets(window)

    def __create_widgets(self, window):
        self.canvas = tk.Canvas(self, bg="#ffffff", bd=0, relief="ridge",
                                highlightthickness=0,
                                height=self.card_height, width=self.card_width)
        self.canvas.place(x=0, y=0)

        # ---Card thumbnail---
        self.card_thumbnail = self.canvas.create_image(self.thumbnail_x,
                                                       self.thumbnail_y,
                                                       image=self.ImgThumbnail)

        # ---Card name---
        self.card_name = tk.Label(master=self, text=f"{self.hotel_name} ({self.room_type})",
                                  foreground="#47423D", background="#ffffff",
                                  justify=tk.LEFT, font=("Noto Sans Bold", convert_size(window, 24)))
        self.card_name.place(x=self.name_x, y=self.name_y, height=convert_size(window, 60))

        # ---Card date---
        self.card_date = tk.Label(master=self, text=f"{self.arrival_date} - {self.departure_date}",
                                  foreground="#7D8693", background="#ffffff",
                                  justify=tk.LEFT, font=("Hind Guntur SemiBold", convert_size(window, 16)))
        self.card_date.place(x=self.date_x, y=self.date_y)

        # ---Card price---
        money = GetMoneyStaying(self.arrival_date, self.departure_date, self.room_price)
        self.card_price = tk.Label(master=self, anchor="e", text=f"${self.room_quantity * money}",
                                   foreground="#35BDDA", background="#ffffff", justify=tk.RIGHT,
                                   font=("Noto Sans Bold", convert_size(window, 30)), width=convert_size(window, 8))
        self.card_price.place(anchor="e", x=self.price_x, y=self.price_y, height=convert_size(window, 80))

        # ---Quantity label---
        self.canvas.create_text(self.quantity_x, self.quantity_y, text=f"{self.room_quantity}",
                                fill="#000000", font=("Noto Sans Regular", convert_size(window, 16)))

        # ---Button '-'---
        self.decrease_btn = tk.Button(master=self, image=self.ImgDecreaseBtn,
                                      borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: btn_clicked())
        self.decrease_btn.place(x=self.decrease_btn_x, y=self.decrease_btn_y,
                                width=convert_size(window, 28), height=convert_size(window, 28))
        # ---Button '+'---
        self.increase_btn = tk.Button(master=self, image=self.ImgIncreaseBtn,
                                      borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: btn_clicked())
        self.increase_btn.place(x=self.increase_btn_x, y=self.increase_btn_y,
                                width=convert_size(window, 28), height=convert_size(window, 28))


class CartPageFrame(tk.Frame):
    """Container for info frame & item frame of CART PAGE"""

    def __init__(self, parent, controller, window, reserve_list):
        self.controller = controller
        self.window = window
        tk.Frame.__init__(self, parent)

        self.item_frame_width = convert_size(window, 900)
        self.item_frame_height = convert_size(window, 900)

        self.info_frame_width = convert_size(window, 700)
        self.info_frame_height = convert_size(window, 900)

        self.number_items = len(reserve_list)
        self.reserve_list = reserve_list

        # ---Card constants---
        self.first_x = convert_size(window, 31)
        self.first_y = convert_size(window, 102)
        self.card_discrepancy = convert_size(window, 324 - 102)

        self.card_width = convert_size(window, 819)
        self.card_height = convert_size(window, 200)

        # --- Image declaration---
        self.ImgInfoBg = convert_image(window, "./assets/Cart_background.png", 603, 516)
        self.ImgConfirmBtn = convert_image(window, "./assets/Cart_confirmBtn.png", 455, 87)

        self.__create_widgets_()

    def __create_widgets_(self):
        self.item_frame = tk.Frame(self)
        self.item_frame.place(x=0, y=0, width=self.item_frame_width, height=self.item_frame_height)

        self.info_frame = tk.Frame(self)
        self.info_frame.place(x=self.item_frame_width, y=0, width=self.info_frame_width, height=self.info_frame_height)

        self.item_canvas = tk.Canvas(master=self.item_frame, bg="#ffffff", bd=0, relief="ridge",
                                     highlightthickness=0,
                                     height=self.item_frame_height, width=self.item_frame_width)
        self.item_canvas.place(x=0, y=0)

        self.info_canvas = tk.Canvas(master=self.info_frame, bg="#ffffff", bd=0, relief="ridge",
                                     highlightthickness=0,
                                     height=self.info_frame_height, width=self.info_frame_width)
        self.info_canvas.place(x=0, y=0)

        # =================== Init Scrollbar for ItemFrame ======================#
        self.scroll_frame_height = convert_size(self.window, 102 + self.number_items * 222)

        self.scroll_bar = tk.Scrollbar(self.item_frame, orient="vertical",
                                       command=self.item_canvas.yview)
        self.scroll_bar.pack(side='right', fill='y')

        self.scrollable_frame = tk.Frame(self.item_canvas, bg="white",
                                         width=self.item_frame_width, height=self.scroll_frame_height)
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.item_canvas.configure(
                                       scrollregion=self.item_canvas.bbox("all")
                                   ))
        self.item_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.item_canvas.configure(yscrollcommand=self.scroll_bar.set)
        # =================== Add widgets to scrollableFrame ==================#
        self.container_frame = tk.Frame(self.scrollable_frame, width=self.item_frame_width,
                                        height=self.scroll_frame_height, bg="#ffffff")
        self.container_frame.place(x=0, y=0)
        # =================== Button Back ===================
        self.ImgBackBtn = convert_image(self.window, "./assets/Cart_backBtn.png", 137, 44)
        self.back_btn = tk.Button(master=self.container_frame, image=self.ImgBackBtn,
                                  borderwidth=0, highlightthickness=0,
                                  command=lambda: self.Back(), relief="flat")
        self.back_btn.place(x=convert_size(self.window, 43), y=convert_size(self.window, 30),
                            width=convert_size(self.window, 137), height=convert_size(self.window, 44))

        self.cards = {}
        row = 0
        self.sub_total = 0
        for reserve in self.reserve_list:
            self.cards[row] = CardCartFrame(parent=self.container_frame, controller=self, window=self.window,
                                            row=row, hotel_name=reserve['Hotel Name'],
                                            room_type=reserve['Room type'], arrival_date=reserve['Arrival'],
                                            departure_date=reserve['Depart'], thumbnail=reserve['Thumbnail'],
                                            room_price=reserve['Price'], room_quantity=reserve['Quantity'])
            self.cards[row].place(x=self.first_x, y=self.first_y + self.card_discrepancy*row,
                                  width=self.card_width, height=self.card_height)
            row += 1
            self.sub_total += GetMoneyStaying(arrival=reserve['Arrival'], depart=reserve['Depart'], price=reserve['Price'])
            # print(self.sub_total)
        # ==================== INFORMATION FRAME =====================#
        self.info_bg = self.info_canvas.create_image(convert_size(self.window, 950 - 900 + 603 / 2),
                                                     convert_size(self.window, 134 + 516 / 2),
                                                     image=self.ImgInfoBg)
        # ---Username---
        self.info_username = tk.Label(master=self.info_frame, anchor="e",
                                      text=self.window.username, foreground="#7D8693", background="#ffffff",
                                      justify=tk.RIGHT, font=("Hind Guntur SemiBold", convert_size(self.window, 22)),
                                      width=convert_size(self.window, 24))
        self.info_username.place(anchor="e", x=convert_size(self.window, 1272 - 900 + 270),
                                 y=convert_size(self.window, 213 + 20), height=convert_size(self.window, 40))
        # ---Bank account---
        self.info_bank = tk.Label(master=self.info_frame, anchor="e",
                                  text=self.window.bank, foreground="#7D8693", background="#ffffff",
                                  justify=tk.RIGHT, font=("Hind Guntur SemiBold", convert_size(self.window, 22)),
                                  width=convert_size(self.window, 24))
        self.info_bank.place(anchor="e",
                             x=convert_size(self.window, 1272 - 900 + 270),
                             y=convert_size(self.window, 213 + 20 + (262 - 213)),
                             height=convert_size(self.window, 40))
        # ---Subtotal---
        self.info_subtotal = tk.Label(master=self.info_frame, anchor="e",
                                      text=f"${self.sub_total}", foreground="#7D8693", background="#ffffff",
                                      justify=tk.RIGHT, font=("Hind Guntur SemiBold", convert_size(self.window, 22)),
                                      width=convert_size(self.window, 24))
        self.info_subtotal.place(anchor="e",
                                 x=convert_size(self.window, 1272 - 900 + 270),
                                 y=convert_size(self.window, 213 + 20 + (463 - 213)),
                                 height=convert_size(self.window, 40))
        # ---Tax---
        self.tax = self.sub_total // 10
        self.info_tax = tk.Label(master=self.info_frame, anchor="e",
                                 text=f"${self.tax}", foreground="#7D8693", background="#ffffff",
                                 justify=tk.RIGHT, font=("Hind Guntur SemiBold", convert_size(self.window, 22)),
                                 width=convert_size(self.window, 24))
        self.info_tax.place(anchor="e",
                            x=convert_size(self.window, 1272 - 900 + 270),
                            y=convert_size(self.window, 213 + 20 + 518 - 213),
                            height=convert_size(self.window, 40))
        # ---Total---
        self.info_total = tk.Label(master=self.info_frame, anchor="e",
                                   text=f"${self.sub_total + self.tax}", foreground="#35BDDA", background="#ffffff",
                                   justify=tk.RIGHT,
                                   font=("Hind Guntur SemiBold", convert_size(self.window, 36)))
        self.info_total.place(anchor="e",
                              x=convert_size(self.window, 1272 - 900 + 270),
                              y=convert_size(self.window, 213 + 594 - 213 + 36),
                              height=convert_size(self.window, 60))
        # ---Button Confirm---
        self.confirm_btn = tk.Button(master=self.info_frame, image=self.ImgConfirmBtn,
                                     borderwidth=0, highlightthickness=0, command=lambda: btn_clicked(),
                                     relief="flat")
        self.confirm_btn.place(x=convert_size(self.window, 1024 - 900), y=convert_size(self.window, 691),
                               width=convert_size(self.window, 455), height=convert_size(self.window, 87))

    def Back(self):
        self.grid_forget()
        self.destroy()


class CardReservationFrame(tk.Frame):
    def __init__(self, parent, controller, window, hotel_name, room_type, timestamp,
                 arrival_date, departure_date, room_quantity, thumbnail, room_price):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # ==================== CARD Constants ====================#
        self.card_width = convert_size(window, 1378)
        self.card_height = convert_size(window, 272)

        self.thumbnail_x = convert_size(window, 1378 / 2)
        self.thumbnail_y = convert_size(window, 272 / 2)

        self.name_x = convert_size(window, 544 - 122 - 2)
        self.name_y = convert_size(window, 177 - 157 - 10)

        self.date_x = convert_size(window, 544 - 122 - 2)
        self.date_y = convert_size(window, 245 - 157 - 6)

        self.quantity_x = convert_size(window, 544 - 122 - 2)
        self.quantity_y = convert_size(window, 289 - 157 - 6)

        self.resID_x = convert_size(window, 544 - 122 - 2)
        self.resID_y = convert_size(window, 333 - 157 - 6)

        self.res_time_x = convert_size(window, 544 - 122 - 2)
        self.res_time_y = convert_size(window, 377 - 157 - 6)

        self.price_x = convert_size(window, 1294 - 122 + 186)
        self.price_y = convert_size(window, 174 - 157 + 32)

        self.cancel_x = convert_size(window, 1301 - 122)
        self.cancel_y = convert_size(window, 353 - 157)

        self.arrival_date = arrival_date
        self.cancel_enable = CanCancel(timestamp)
        self.departure_date = departure_date
        self.hotel_name = hotel_name
        self.room_price = room_price
        self.room_quantity = room_quantity
        self.room_type = room_type
        self.thumbnail_path = thumbnail
        self.timestamp = timestamp
        # ==================== IMAGE ====================#
        self.ImgThumbnail = convert_image(window, "./assets/Res_background.png", 1378, 272)
        self.ImgCancelBtn = convert_image(window, "./assets/Res_cancelBtn.png", 170, 54)

        self.__create_widgets(window)

    def __create_widgets(self, window):
        self.canvas = tk.Canvas(master=self, bg="#ffffff", bd=0,
                                height=self.card_height, width=self.card_width,
                                highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # ---Thumbnail---
        self.thumbnail = self.canvas.create_image(self.thumbnail_x, self.thumbnail_y, image=self.ImgThumbnail)

        # ---Name---
        self.name = tk.Label(master=self, text=f"{self.hotel_name} ({self.room_type})",
                             fg="#47423D", bg="#ffffff", justify=tk.LEFT,
                             font=("Noto Sans Bold", convert_size(window, 32)))
        self.name.place(x=self.name_x, y=self.name_y, height=convert_size(window, 68))

        # ---Date---
        self.date = tk.Label(master=self, text=f"{self.arrival_date}-{self.departure_date}",
                             fg="#7D8693", bg="#ffffff", justify=tk.LEFT,
                             font=("Hind Guntur SemiBold", convert_size(window, 18)))
        self.date.place(x=self.date_x, y=self.date_y, height=convert_size(window, 40))
        # ---Quantity---
        self.quantity = tk.Label(master=self, text=f"Quantity: {self.room_quantity}",
                                 fg="#7D8693", bg="#ffffff", justify=tk.LEFT,
                                 font=("Hind Guntur SemiBold", convert_size(window, 18)))
        self.quantity.place(x=self.quantity_x, y=self.quantity_y, height=convert_size(window, 40))

        # ---Reservation time---
        self.time = tk.Label(master=self, text=f"Reservation time: {self.timestamp}",
                             fg="#7D8693", bg="#ffffff", justify=tk.LEFT,
                             font=("Hind Guntur SemiBold", convert_size(window, 18)))
        self.time.place(x=self.res_time_x, y=self.res_time_y, height=convert_size(window, 40))
        # ---Price---
        self.price = tk.Label(master=self, text=f"{self.room_price}",
                              anchor="e", fg="#35BDAA", bg="#ffffff",
                              justify=tk.RIGHT, font=("Noto Sans Bold", convert_size(window, 42)),
                              width=convert_size(window, 10))
        self.price.place(x=self.price_x, y=self.price_y,
                         anchor="e", height=convert_size(window, 80))
        # ---Cancel Button---
        if self.cancel_enable:
            self.cancel_btn = tk.Button(master=self, image=self.ImgCancelBtn, relief="flat",
                                        bd=0, highlightthickness=0, command=lambda: btn_clicked())
            self.cancel_btn.place(x=self.cancel_x, y=self.cancel_y,
                                  width=convert_size(window, 170), height=convert_size(window, 54))


class ReservationPageFrame(tk.Frame):
    def __init__(self, parent, controller, window, reserve_list):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.reserve_list = reserve_list
        self.number_items = len(reserve_list)
        self.scroll_frame_height = convert_size(window, 157 + self.number_items * 298)
        # ---Card Constants---
        self.card_width = convert_size(window, 1378)
        self.card_height = convert_size(window, 272)

        self.first_x = convert_size(window, 122)
        self.first_y = convert_size(window, 157)
        self.card_discrepancy = convert_size(window, 455 - 157)

        self.__create_widgets(window)

    def __create_widgets(self, window):
        self.canvas = tk.Canvas(master=self, bg="#ffffff", bd=0, relief="ridge",
                                width=window.frameWidth, height=window.frameHeight,
                                highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # ---Scroll Bar---
        self.scroll_bar = tk.Scrollbar(master=self, orient="vertical",
                                       command=self.canvas.yview)

        self.scroll_bar.pack(side=tk.RIGHT, fill="y")

        self.scrollable_frame = tk.Frame(master=self.canvas,
                                         width=window.frameWidth, height=self.scroll_frame_height,
                                         bg="#ffffff")
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.canvas.configure(
                                       scrollregion=self.canvas.bbox("all")
                                   ))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)

        # ================ Add widgets to scrollableFrame ==================#
        self.container = tk.Frame(master=self.scrollable_frame,
                                  width=window.frameWidth, height=self.scroll_frame_height,
                                  bg="#ffffff")
        self.container.place(x=0, y=0)

        # ========== Button "Back" ===========
        self.ImgBackBtn = convert_image(window, "./assets/Res_backBtn.png", 227, 55)
        self.back_btn = tk.Button(master=self.container, image=self.ImgBackBtn, bd=0,
                                  highlightthickness=0, command=lambda: self.Back(),
                                  relief="flat")
        self.back_btn.place(x=convert_size(window, 41), y=convert_size(window, 44),
                            width=convert_size(window, 227), height=convert_size(window, 55))
        # ========== Title ===========
        self.title = tk.Label(master=self.container, text="Your Reservation",
                              fg="#47423D", bg="#ffffff", justify=tk.CENTER,
                              font=("Noto Sans SemiBold", convert_size(window, 36)))
        self.title.place(x=(window.frameWidth / 2), y=convert_size(window, 84), anchor="center")

        self.cards = {}
        row = 0
        for reserve in self.reserve_list:
            self.cards[row] = CardReservationFrame(parent=self.container, controller=self,
                                                   window=window, hotel_name=reserve['NAME'],
                                                   room_type=reserve['TYPE'], thumbnail="#thumbnail",
                                                   timestamp=reserve['TIMESTAMP'],
                                                   arrival_date=reserve['ARRIVAL'],
                                                   departure_date=reserve['DEPARTURE'],
                                                   room_quantity=reserve['QUALITY'],
                                                   room_price=reserve['TOTAL'])
            self.cards[row].place(x=self.first_x, y=self.first_y + self.card_discrepancy * row,
                                  width=self.card_width, height=self.card_height)
            row += 1

    def Back(self):
        self.controller.show_frame("MenuFrame")


if __name__ == "__main__":
    connected = True
    app = App()
    app.mainloop()
