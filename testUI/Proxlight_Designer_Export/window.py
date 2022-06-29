from tkinter import *
from math import floor
from PIL import Image, ImageTk

window = Tk()
print(window.winfo_screenwidth(), window.winfo_screenheight())

#====================== Convert Function =======================#
def btn_clicked():
    print("Button Clicked")

def convertSize(originalSize):
    frameWidth = window.winfo_screenwidth() * scaleRate
    return floor((frameWidth * originalSize )/1600)


# originalWidth & originalHeight are the Width and Height on Figma
def convertImage(path, originalWidth, originalHeight):
    originalImage = Image.open(path)
    resizedImage = originalImage.resize((convertSize(originalWidth), convertSize(originalHeight)))
    convertedImage = ImageTk.PhotoImage(resizedImage)
    return convertedImage


#==================== Constants Declaration ====================#
scaleRate = 0.8
frameWidth = window.winfo_screenwidth() * scaleRate
frameHeight = (window.winfo_screenwidth() * scaleRate) * 9/16
fontSize = convertSize(40)
geometry = f'{floor(frameWidth)}' + "x" + f'{floor(frameHeight)}'

EntryHeight = convertSize(60)
EntryFontSize = f'{convertSize(80)}'
EntryDiscrepancy = convertSize(12)


#==================== Image Declaration ====================#
background_img = convertImage('background.png', 1448, 900)
img0 = convertImage("img0.png", 129, 38)
img1 = convertImage("img1.png", 510, 84)
entry0_img = convertImage("img_textBox0.png", 510, 84)
entry1_img = convertImage("img_textBox1.png", 510, 84)



#========================= Screen ==========================#
window.geometry(geometry)
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = frameHeight,
    width = frameWidth,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)


def clearScreen(self = window):
    for widget in self.place_slaves():
        widget.place_forget()




background = canvas.create_image(
    convertSize(724.0), convertSize(450.0),
    image=background_img
)


b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat"
)
b0.place(
    x = convertSize(1302), y = convertSize(788),
    width = convertSize(129),
    height = convertSize(38)
)

b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat"
)
b1.place(
    x = convertSize(946), y = convertSize(572),
    width = convertSize(510),
    height = convertSize(84)
)


entry0_bg = canvas.create_image(
    convertSize(1201.0), convertSize(459.0),
    image = entry0_img
)
entry0 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,
    font = (EntryFontSize)
)
entry0.place(
    x = convertSize(962), y = convertSize(417) + EntryDiscrepancy,
    width = convertSize(478),
    height = EntryHeight
)


entry1_bg = canvas.create_image(
    convertSize(1201), convertSize(304),
    image = entry1_img
)
entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,
    font = (EntryFontSize)
)
entry1.place(
    x = convertSize(962), y = convertSize(262) + EntryDiscrepancy,
    width = convertSize(478),
    height = EntryHeight
)


window.resizable(False, False)
window.mainloop()
