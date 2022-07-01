
from PIL import Image, ImageTk
from tkinter import Tk, Label, BOTH
from tkinter.ttk import Frame, Style
from math import floor

def convertSize(originalSize):
    frameWidth = window.winfo_screenwidth() * scaleRate
    return floor((frameWidth * originalSize )/1600)

def convertImage(path, originalWidth, originalHeight):
    originalImage = Image.open(path)
    resizedImage = originalImage.resize((convertSize(originalWidth), convertSize(originalHeight)))
    print((convertSize(originalWidth), convertSize(originalHeight)))
    convertedImage = ImageTk.PhotoImage(resizedImage)
    return convertedImage

window = Tk()

#==================== Constants Declaration ====================#
scaleRate = 0.8
frameWidth = window.winfo_screenwidth() * scaleRate
frameHeight = (window.winfo_screenwidth() * scaleRate) * 9/16
geometry = f'{floor(frameWidth)}' + "x" + f'{floor(frameHeight)}'

EntryHeight = convertSize(60)
EntryFontSize = f'{convertSize(80)}'
EntryDiscrepancy = convertSize(12)


window.geometry(geometry)

class Login(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Login Screen")
        self.pack(fill=BOTH, expand=1)
    
        Style().configure("TFrame", background="#ffffff")
    
        # Background
        LoginBackground = convertImage("./assets/Login_Background.png", 1448, 900)
        LoginBgLbl = Label(self, image=LoginBackground, bg="#ffffff", bd="0")
        LoginBgLbl.image = LoginBackground
        LoginBgLbl.place(x=0, y=0)

        

        #
class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        loginScreen = Login(self)



print(frameWidth, frameHeight)
app = App(window)

window.mainloop()