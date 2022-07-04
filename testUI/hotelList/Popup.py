from tkinter import *
import datetime

# Nhớ install pip install tkcalendar
from tkcalendar import Calendar


class popup_window(object):
    def __init__(self, master):
        self.departDate = None
        self.arrivalDate = None
        top = self.top = Toplevel(master)

        current_time = datetime.datetime.now()
        self.arrivalChose = False
        self.departChose = False

        # ==================== Calendar for Arrival Date ====================#
        self.arrivalTitle = Label(top,
                                  text="CHOOSE ARRIVAL DATE : ",
                                  font=("Noto Sans Bold", 16)
                                  ).grid(row=0, column=0, pady=10)

        self.arrivalCalendar = Calendar(top,
                                        selectmode='day',
                                        font="14",
                                        year=current_time.year,
                                        month=current_time.month,
                                        day=current_time.day
                                        )
        self.arrivalCalendar.grid(row=1, column=0, padx=12)

        # Arrival Date Label
        self.arrivalLabel = Label(top, text="", font=("Noto Sans Bold", 14))
        self.arrivalLabel.grid(row=2, column=0, pady=20)

        # Arrival Button
        self.arrivalBtn = Button(top, text='Choose', font=6, command=self.showArrivalDate)
        self.arrivalBtn.grid(row=3, column=0)

        # ========================= Confirm Button =========================#
        self.confirmBtn = Button(top, text='Confirm', font=15, command=self.confirmAndOut)
        self.confirmBtn.grid(row=4, column=1, pady=20)

        # ==================== Calendar for Depart Date ====================#
        self.departTitle = Label(top, text="CHOOSE DEPARTURE DATE : ", font=("Noto Sans Bold", 16)).grid(row=0, column=2, pady=10)

        self.departCalendar = Calendar(top,
                                       selectmode='day',
                                       font="14",
                                       year=current_time.year,
                                       month=current_time.month,
                                       day=current_time.day
                                       )
        self.departCalendar.grid(row=1, column=2, padx=12)

        # Depart Date Label
        self.departLabel = Label(top,
                                 text="",
                                 font=("Noto Sans Bold", 14)
                                 )
        self.departLabel.grid(row=2, column=2, pady=20)

        # Depart Button
        self.departBtn = Button(top, text='Choose', font=6, command=self.showDepartDate)
        self.departBtn.grid(row=3, column=2)

    def showArrivalDate(self):
        self.arrivalChose = True
        self.arrivalLabel.config(text="Selected Arrival Date : " + self.arrivalCalendar.get_date())

    def showDepartDate(self):
        self.departChose = True
        self.departLabel.config(text="Selected Departure Date : " + self.departCalendar.get_date())

    def confirmAndOut(self):
        self.arrivalDate = self.arrivalCalendar.get_date()
        self.departDate = self.departCalendar.get_date()
        if not self.arrivalChose:
            self.arrivalLabel.config(text="You haven't chosen Arrival Date")
            return
        if not self.departChose:
            self.departLabel.config(text="You haven't chosen Departure Date")
            return
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
