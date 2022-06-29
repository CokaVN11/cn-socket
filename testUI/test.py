from math import floor
from tkinter import *


window = Tk()
print(window.winfo_screenwidth(), window.winfo_screenheight())

scaleRate = 0.8
testWidth = window.winfo_screenwidth() * scaleRate
testHeight = (window.winfo_screenwidth() * scaleRate) * 9/16

def convertSize(size):
    rootWeigt = window.winfo_screenwidth() * scaleRate
    return floor((rootWeigt * size )/1600)

textSize = convertSize(40)
print(textSize)
geometry = f'{floor(testWidth)}' + "x" + f'{floor(testHeight)}'
print(geometry)


window.geometry(geometry)
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#333",
    height = testHeight,
    width = testWidth,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

lbl = Label(window, text="Test size", font=("Roboto" , textSize)).pack()

window.resizable(False, False)
window.mainloop()