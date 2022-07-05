from math import floor
from tkinter import *

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
frameWidth = window.winfo_screenwidth() * scaleRate
frameHeight = (window.winfo_screenwidth() * scaleRate) * 9 / 16
geometry = f'{floor(frameWidth)}' + "x" + f'{floor(frameHeight)}'

window.geometry(geometry)
window.configure(bg="#ffffff")

canvas = Canvas(
    window,
    bg="#ffffff",
    height=frameHeight,
    width=frameWidth,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

# ==================================================================#
# Button "Back"
ImgBackBtn = convertImage("LK_BackBtn.png", 227, 55)
backBtn = Button(
    image=ImgBackBtn,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)
backBtn.place(
    x=convertSize(41), y=convertSize(44),
    width=convertSize(227),
    height=convertSize(55)
)

# Button "Cart"
ImgCart = convertImage("LK_Cart.png", 109, 109)
cartBtn = Button(
    image=ImgCart,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)
cartBtn.place(
    x=convertSize(1462), y=convertSize(30),
    width=convertSize(109),
    height=convertSize(109)
)

# Title Hotel name
hotelName = Label(
    # window,
    text="#Hotel name",
    foreground="#47423D",
    background="#ffffff",
    justify=CENTER,
    font=("Noto Sans SemiBold", convertSize(50))
).pack(pady=14)

# ==================== CARD Constants ====================#
cardWidth = convertSize(1354)
cardHeight = convertSize(324)

canvasWidth = convertSize(1354)
canvasHeight = convertSize(324)

firstCardX = convertSize(123)
firstCardY = convertSize(155)
cardDiscrepancy = convertSize(522 - 155)

thumbnailX = convertSize(1354 / 2)
thumbnailY = convertSize(324 / 2)

namePosX = convertSize(619 - 123)
namePosY = convertSize((186 - 155) - 26)

descPosX = convertSize(619 - 123)
descPosY = convertSize((253 - 155) - 4)

pricePosX = convertSize(1268 - 123 + 186)
pricePosY = convertSize((186 - 155) + 20)

tagAvailableX = convertSize((401 - 123) + (161 / 2))
tagAvailableY = convertSize((389 - 155) + (42 / 2))
tagFullX = convertSize((471 - 123) + (91 / 2))
tagFullY = convertSize((389 - 155) + (42 / 2))

bedPosX = convertSize((670 - 123) - 4)
bedPosY = convertSize((408 - 155) - 12)
areaPosX = convertSize((807 - 123) - 4)
areaPosY = convertSize((408 - 155) - 12)
guestPosX = convertSize((938 - 123) - 4)
guestPosY = convertSize((408 - 155) - 12)

cardBtnX = convertSize((1216 - 123))
cardBtnY = convertSize((380 - 155))

ImgThumbnail = convertImage("LK_room1_single.png", 1354, 324)
ImgTagAvailable = convertImage("LK_Available.png", 161, 42)
ImgTagFull = convertImage("LK_Full.png", 91, 42)
ImgReserveBtn = convertImage("LK_ReserveBtn.png", 234, 68)
ImgReserveDis = convertImage("LK_ReserveDisabled.png", 234, 68)


def renderCard(Row, cardName, cardDescription, cardStatus, cardPrice,
               cardThumbPath, cardBed, cardArea, cardGuest):
    # CARD ITEM FRAME
    cardFrame = Frame()
    cardFrame.place(
        x=firstCardX,
        y=firstCardY + cardDiscrepancy * (Row - 1),
        width=cardWidth,
        height=cardHeight)

    # Card Canvas (used for display Tag without background)
    # khai báo ở đây để ko đè các widget khác
    cardCanvas = Canvas(
        cardFrame,
        bg="#ffffff",
        height=canvasHeight,
        width=canvasWidth,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    cardCanvas.place(x=0, y=0)

    # Card Thumbnail
    cardThumbnail = cardCanvas.create_image(
        thumbnailX,
        thumbnailY,
        image=ImgThumbnail
    )

    # Card Status
    if cardStatus == 1:
        # Tag Available
        tagAvailable = cardCanvas.create_image(
            tagAvailableX,
            tagAvailableY,
            image=ImgTagAvailable
        )
    else:
        # Tag Full
        tagFull = cardCanvas.create_image(
            tagFullX,
            tagFullY,
            image=ImgTagFull
        )

    # Card Name
    card_Name = Label(
        master=cardFrame,
        text=cardName,
        foreground="#47423D",
        background="#ffffff",
        font=("Noto Sans Bold", convertSize(40))
    ).place(
        x=namePosX,
        y=namePosY,
    )

    # Card Description
    card_Desc = Label(
        master=cardFrame,
        text=cardDescription,
        foreground="#7D8693",
        background="#ffffff",
        justify=LEFT,
        wraplength=convertSize(600),
        font=("Hind Guntur Medium", convertSize(18))
    ).place(
        x=descPosX,
        y=descPosY,
    )

    # Card Price
    card_Price = Label(
        master=cardFrame,
        anchor="e",
        text=cardPrice,
        foreground="#35bdda",
        background="white",
        justify=RIGHT,
        font=("Noto Sans Bold", convertSize(50)),
        width=convertSize(8)
    ).place(
        anchor="e",
        x=pricePosX,
        y=pricePosY,
        height=convertSize(80)
    )

    # Card Bed
    card_Bed = Label(
        master=cardFrame,
        text=cardBed,
        foreground="#8f8f8f",
        background="#ffffff",
        justify=LEFT,
        font=("Noto Sans Regular", convertSize(18))
    ).place(
        x=bedPosX,
        y=bedPosY,
    )

    # Card Area
    card_Area = Label(
        master=cardFrame,
        text=cardArea,
        foreground="#8f8f8f",
        background="#ffffff",
        justify=LEFT,
        font=("Noto Sans Regular", convertSize(18))
    ).place(
        x=areaPosX,
        y=areaPosY,
    )

    # Card Guest
    card_Guest = Label(
        master=cardFrame,
        text=cardGuest,
        foreground="#8f8f8f",
        background="#ffffff",
        justify=LEFT,
        font=("Noto Sans Regular", convertSize(18))
    ).place(
        x=guestPosX,
        y=guestPosY,
    )

    if cardStatus == 1:
        # Button "Reserve"
        reserveBtn = Button(
            master=cardFrame,
            image=ImgReserveBtn,
            borderwidth=0,
            highlightthickness=0,
            command=btn_clicked,
            relief="flat"
        )
        reserveBtn.place(
            x=cardBtnX,
            y=cardBtnY,
            width=convertSize(234),
            height=convertSize(68)
        )
    else:
        # Button "Reserve DISABLED"
        reserveBtnDisabled = Button(
            master=cardFrame,
            image=ImgReserveDis,
            borderwidth=0,
            highlightthickness=0,
            command=btn_clicked,
            relief="flat"
        )
        reserveBtnDisabled.place(
            x=cardBtnX,
            y=cardBtnY,
            width=convertSize(234),
            height=convertSize(68)
        )


renderCard(1, "Single Room", "For single person", 1, "$100", "#Thumbnail", "1 Bed", "68 m2", "2 Guest")
renderCard(2, "V.I.P Room", "Hehe", 0, "$1000", "#Thumbnail", "2 Bed", "86 m2", "4 Guest")

window.resizable(False, False)
window.mainloop()
