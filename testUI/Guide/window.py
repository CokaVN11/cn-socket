from tkinter import *
from math import floor
from PIL import Image, ImageTk

window = Tk()
print(window.winfo_screenwidth(), window.winfo_screenheight())


def btn_clicked():
    print("Button Clicked")


def convertSize(originalSize):
    frameWidth = window.winfo_screenwidth() * scaleRate
    return floor((frameWidth * originalSize) / 1600)


# originalWidth & originalHeight are the Width and Height on Figma
def convertImage(path, originalWidth, originalHeight):
    originalImage = Image.open(path)
    resizedImage = originalImage.resize((convertSize(originalWidth), convertSize(originalHeight)))
    convertedImage = ImageTk.PhotoImage(resizedImage)    
    return convertedImage


# ==================== Constants Declaration ====================#
scaleRate = 0.8
windowWidth = window.winfo_screenwidth() * scaleRate
windowHeight = (window.winfo_screenwidth() * scaleRate) * 9 / 16
geometry = f'{floor(windowWidth)}' + "x" + f'{floor(windowHeight)}'

window.geometry(geometry)
window.configure(bg="#ffffff")


#===================== Init Scrollbar ======================#
guideFrame = Frame(window)
guideFrame.place(
    x = 0,
    y = 0,
    width = windowWidth,
    height = windowHeight
)

guideCanvas = Canvas(
    guideFrame,
    bg="#ffffff",
    height=windowHeight,
    width=windowWidth,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
guideCanvas.place(x=0, y=0)

scrollFrameHeight = convertSize(3710)

scrollBar = Scrollbar(
    guideFrame, 
    orient='vertical', 
    command=guideCanvas.yview
)
scrollBar.pack(side = RIGHT, fill = Y)

scrollableFrame = Frame(
    guideCanvas,
    width=windowWidth, 
    height=scrollFrameHeight, 
    background="white"
)

scrollableFrame.bind(
    "<Configure>",
    lambda e: guideCanvas.configure(
        scrollregion=guideCanvas.bbox("all")
    )
)

guideCanvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

guideCanvas.configure(yscrollcommand=scrollBar.set)


# ================ Add widgets to scrollableFrame ==================#
containerFrame = Frame(
    scrollableFrame, 
    width=windowWidth, 
    height=scrollFrameHeight, 
    background="white"
)
containerFrame.place(x = 0, y = 0)

containerCanvas = Canvas(
    containerFrame,
    bg="#ffffff",
    height=scrollFrameHeight,
    width=windowWidth,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
containerCanvas.place(x=0, y=0)

# ========== Button "Back"
ImgBackBtn = convertImage("Guide_backBtn.png", 227, 55)
ImgStep1 = convertImage("Guide_step1.png", 1430, 536)
ImgStep2 = convertImage("Guide_step2.png", 1430, 536)
ImgStep3 = convertImage("Guide_step3.png", 1430, 536)
ImgStep4 = convertImage("Guide_step4.png", 1430, 536)
ImgStep5 = convertImage("Guide_step5.png", 1430, 536)
ImgStep6 = convertImage("Guide_step6.png", 1430, 482)


backBtn = Button(
    containerFrame,
    image = ImgBackBtn,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat"
)
backBtn.place(
    x = convertSize(55), y = convertSize(45),
    width = convertSize(227),
    height = convertSize(55)
)
    
# ========== Title
titleReservation = Label(
    containerFrame,
    text = "Booking Guide",
    foreground="#47423D",
    background="#ffffff",
    justify=CENTER,
    font=("Noto Sans SemiBold", convertSize(36))
).place(
    x = windowWidth/2 ,
    y = convertSize(84),
    anchor="center"
)

# =========== Guide
step1Label = containerCanvas.create_image(
    convertSize(85 + 1431/2),
    convertSize(204 + 536/2),
    image=ImgStep1
)
step2Label = containerCanvas.create_image(
    convertSize(85 + 1431/2),
    convertSize(792 + 536/2),
    image=ImgStep2
)
step3Label = containerCanvas.create_image(
    convertSize(85 + 1431/2),
    convertSize(1380 + 536/2),
    image=ImgStep3
)
step4Label = containerCanvas.create_image(
    convertSize(85 + 1431/2),
    convertSize(1968 + 536/2),
    image=ImgStep4
)
step5Label = containerCanvas.create_image(
    convertSize(85 + 1431/2),
    convertSize(2556 + 536/2),
    image=ImgStep5
)
step6Label = containerCanvas.create_image(
    convertSize(85 + 1431/2),
    convertSize(3144 + 536/2),
    image=ImgStep6
)









window.resizable(False, False)
window.mainloop()
