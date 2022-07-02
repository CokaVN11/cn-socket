
from PIL import Image, ImageTk
from tkinter import *
from tkinter.ttk import Frame, Style
from math import floor

@staticmethod
def convertSize(window, originalSize):
    return floor((window.frameWidth * originalSize) / 1600)


@staticmethod
def convertImage(window, path, originalWidth, originalHeight):
    originalImage = Image.open(path)
    resizedImage = originalImage.resize(
        (convertSize(window, originalWidth), 
        convertSize(window, originalHeight))
    )
    convertedImage = ImageTk.PhotoImage(resizedImage)
    return convertedImage


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        #==================== Constants Declaration ====================#
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
        self.resizable(0, 0)

        # Frame Switch
        self._frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        Button(self, text="Open page one",
                  command=lambda: master.switch_frame(PageOne)).pack()
        Button(self, text="Open page two",
                  command=lambda: master.switch_frame(PageTwo)).pack()

class PageOne(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

class PageTwo(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


class LoginPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Login Screen")
        self.pack(fill=BOTH, expand=1)
    
        Style().configure("TFrame", background="#ffffff")
    
        # Background
        LoginBackground = convertImage(self, "./assets/Login_Background.png", 1448, 900)
        LoginBgLbl = Label(self, image=LoginBackground, bg="#ffffff", bd="0")
        LoginBgLbl.image = LoginBackground
        LoginBgLbl.place(x=0, y=0)

        LoginEntry1Background = convertImage(self, "./assets/Login_Entry.png", 510, 84)
        LoginEntry1Lbl = Label(self, image=LoginEntry1Background, bg="#ffffff", bd="0")
        LoginEntry1Lbl.image = LoginEntry1Background
        LoginEntry1Lbl.place(x=0, y=0)
        LoginEntry1 = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0,
            font = ("40")
        )
        LoginEntry1.place(
            x = convertSize(self, 962), y = convertSize(self, 262),
            width = convertSize(self, 478),
            height = 100
        )



window = App()
print(window.frameWidth, window.frameHeight)

window.mainloop()