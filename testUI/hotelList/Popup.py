from tkinter import *
import datetime

# Nhớ install pip install tkcalendar
from tkcalendar import Calendar


class popup_window(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        # --Title--
        self.note_title = Label(self.top, text="Any note ?",
                                      font=("Noto Sans Bold", 16))
        self.note_title.grid(row=0, column=0, pady=10)


        # --Entry--
        self.note_Entry = Text(self.top, 
                                    width=50, # Số kí tự trong 1 dòng (~line wrap)
                                    height=3, # Số dòng mà khung hiển thị
                                    font=("Noto Sans Bold", 14))
        self.note_Entry.grid(row=1, column=0, pady=20)

        # -- Length -- #
        self.note_len = Label(self.top, text="(0/100 character)", font=("Noto Sans Regular", 11))
        self.note_len.grid(row=2, column=0, pady=10)

        self.note_Entry.bind('<KeyPress>', self.updateLength)
        self.note_Entry.bind('<KeyRelease>', self.updateLength)
        # ---Confirm button---
        self.confirm_btn = Button(self.top, text="Confirm", font=15,
                                     command=self.confirmAndOut, relief="ridge")
        self.confirm_btn.grid(row=3, column=0, pady=20)
        # self.departDate = None
        # self.arrivalDate = None

        # current_time = datetime.datetime.now()
        # self.arrivalChose = False
        # self.departChose = False

        # # ==================== Calendar for Arrival Date ====================#
        # self.arrivalTitle = Label(top,
        #                           text="CHOOSE ARRIVAL DATE : ",
        #                           font=("Noto Sans Bold", 16)
        #                           ).grid(row=0, column=0, pady=10)

        # self.arrivalCalendar = Calendar(top,
        #                                 selectmode='day',
        #                                 font="14",
        #                                 year=current_time.year,
        #                                 month=current_time.month,
        #                                 day=current_time.day
        #                                 )
        # self.arrivalCalendar.grid(row=1, column=0, padx=12)

        # # Arrival Date Label
        # self.arrivalLabel = Label(top, text="", font=("Noto Sans Bold", 14))
        # self.arrivalLabel.grid(row=2, column=0, pady=20)

        # # Arrival Button
        # self.arrivalBtn = Button(top, text='Choose', font=6, command=self.showArrivalDate)
        # self.arrivalBtn.grid(row=3, column=0)

        # # ========================= Confirm Button =========================#
        # self.confirmBtn = Button(top, text='Confirm', font=15, command=self.confirmAndOut)
        # self.confirmBtn.grid(row=4, column=1, pady=20)

        # # ==================== Calendar for Depart Date ====================#
        # self.departTitle = Label(top, text="CHOOSE DEPARTURE DATE : ", font=("Noto Sans Bold", 16)).grid(row=0, column=2, pady=10)

        # self.departCalendar = Calendar(top,
        #                                selectmode='day',
        #                                font="14",
        #                                year=current_time.year,
        #                                month=current_time.month,
        #                                day=current_time.day
        #                                )
        # self.departCalendar.grid(row=1, column=2, padx=12)

        # # Depart Date Label
        # self.departLabel = Label(top,
        #                          text="",
        #                          font=("Noto Sans Bold", 14)
        #                          )
        # self.departLabel.grid(row=2, column=2, pady=20)

        # # Depart Button
        # self.departBtn = Button(top, text='Choose', font=6, command=self.showDepartDate)
        # self.departBtn.grid(row=3, column=2)

    # def showArrivalDate(self):
    #     self.arrivalChose = True
    #     self.arrivalLabel.config(text="Selected Arrival Date : " + self.arrivalCalendar.get_date())

    # def showDepartDate(self):
    #     self.departChose = True
    #     self.departLabel.config(text="Selected Departure Date : " + self.departCalendar.get_date())

    # def confirmAndOut(self):
    #     self.arrivalDate = self.arrivalCalendar.get_date()
    #     self.departDate = self.departCalendar.get_date()
    #     if not self.arrivalChose:
    #         self.arrivalLabel.config(text="You haven't chosen Arrival Date")
    #         return
    #     if not self.departChose:
    #         self.departLabel.config(text="You haven't chosen Departure Date")
    #         return
    #     self.top.destroy()

    def updateLength(self, event):
        if len(self.note_Entry.get("1.0", "end-1c")) > 100:
            self.note_len.config(text="(Maximum length !)")
            oldNote = self.note_Entry.get("1.0", "end-2c")
            print(oldNote)
            self.note_Entry.delete("1.0", "end-1c")
            self.note_Entry.insert("1.0",oldNote)
        else:
            self.note_len.config(text="(" + str(len(self.note_Entry.get("1.0", "end-1c"))) + "/100 character)")
    
    def confirmAndOut(self):
        self.noteInput = self.note_Entry.get("1.0", "end-1c") # Lấy nội dung từ đầu tới cuối
        print(self.noteInput)
        self.top.destroy()


class mainWindow(object):
    def __init__(self, master):
        self.popupScreen = None
        self.master = master

        # Look up Button
        self.LookupBtn = Button(
            master,
            text="Look up",
            command=self.popup
        )
        self.LookupBtn.pack()

        self.testPrintBtn = Button(
            master,
            text="Print date",
            command=lambda: print("Arrival Date :", self.arrivalValue(), "\nDeparture Date :", self.departValue())
        )
        self.testPrintBtn.pack()

    def popup(self):
        self.popupScreen = popup_window(self.master)
        self.master.wait_window(self.popupScreen.top)

    def arrivalValue(self):
        return self.popupScreen.arrivalDate

    def departValue(self):
        return self.popupScreen.departDate


if __name__ == "__main__":
    root = Tk()
    root.geometry("400x400")
    m = mainWindow(root)
    root.mainloop()
