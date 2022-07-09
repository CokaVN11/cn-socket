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

######################################################################
# Button "Back"
ImgBackBtn = convertImage("LOH_BackButton.png", 177, 55)
backBtn = Button(
    image=ImgBackBtn,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat")
backBtn.place(
    x=convertSize(38), y=convertSize(40),
    width=convertSize(177),
    height=convertSize(55))

# ==================== CARD Constants ====================#
cardWidth = convertSize(423)
cardHeight = convertSize(564)

canvasWidth = convertSize(423)
canvasHeight = convertSize(564)

firstCardX = convertSize(81)
firstCardY = convertSize(163)
cardDiscrepancy = convertSize(588 - 81)

namePosX = convertSize(103 - 81)
namePosY = convertSize(270 - 4)

descPosX = convertSize(103 - 81)
descPosY = convertSize((500 - 163) - 12)

tagAvailableX = convertSize((324 - 81) + (161 / 2))
tagAvailableY = convertSize((364 - 163) + (42 / 2))
tagFullX = convertSize((394 - 81) + (91 / 2))
tagFullY = convertSize((364 - 163) + (42 / 2))

cardBtnX = convertSize((289 - 81))
cardBtnY = convertSize((644 - 163))

thumbnailX = convertSize(423 / 2)
thumbnailY = convertSize(564 / 2)

#############################
#    CARD FRAME             #
#  ##### CARD CANVAS #####  #
#  #                     #  #
#  #                     #  #
#  #   CARD THUMBNAIL    #  #
#  #                     #  #
#  #           CARD TAG  #  #
#  #######################  #
#   CARD NAME               #
#   CARD DESCRIPTION        #
#                           #
#           (CARD BUTTON)   #
#############################
ImgThumbnail = convertImage("LOH_thumbnail1.png", 423, 564)
ImgAvailable = convertImage("LOH_Available.png", 161, 42)
ImgFull = convertImage("LOH_Full.png", 91, 42)
ImgLookupBtn = convertImage("LOH_LookupBtn.png", 197, 65)
ImgDisLookupBtn = convertImage("LOH_LookupDisabled.png", 197, 65)


def renderCard(Column, cardName, cardDescription, cardStatus, cardThumbPath):
    # CARD ITEM FRAME
    cardFrame = Frame()
    cardFrame.place(
        x=firstCardX + cardDiscrepancy * (Column - 1),
        y=firstCardY,
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

    if cardStatus == 1:
        # Tag Available
        cardTag = cardCanvas.create_image(
            tagAvailableX,
            tagAvailableY,
            image=ImgAvailable
        )
    else:
        # Tag Full
        cardTag = cardCanvas.create_image(
            tagFullX,
            tagFullY,
            image=ImgFull
        )

    # Card Name
    cardName = Label(
        master=cardFrame,
        text=cardName,
        foreground="#47423D",
        background="white",
        font=("Noto Sans Bold", convertSize(28))
    ).place(
        x=namePosX,
        y=namePosY,
    )

    # Card Description
    cardDesc = Label(
        master=cardFrame,
        text=cardDescription,
        foreground="#7D8693",
        background="#444444",
        justify=LEFT,
        wraplength=convertSize(380),
        font=("Hind Guntur Medium", convertSize(14)),
    ).place(
        x=descPosX,
        y=descPosY,
        height=convertSize(150)
    )

    if cardStatus == 1:
        # Button "Look up"
        lookupBtn = Button(
            master=cardFrame,
            image=ImgLookupBtn,
            borderwidth=0,
            highlightthickness=0,
            command=btn_clicked,
            relief="flat")
        lookupBtn.place(
            x=cardBtnX,
            y=cardBtnY,
            width=convertSize(197),
            height=convertSize(65))
    else:
        # Button "Look up" (DISABLED)
        disLookupBtn = Button(
            master=cardFrame,
            image=ImgDisLookupBtn,
            borderwidth=0,
            highlightthickness=0,
            # state = "disabled",
            relief="flat")
        disLookupBtn.place(
            x=cardBtnX,
            y=cardBtnY,
            width=convertSize(197),
            height=convertSize(65))


renderCard(1, "Lake Place", "123123123 12313 nghhe nknkdgn zxc vvcxvcxvcxv adsa  xvc gfgf fdncvncmvn", 1, "LOH_thumbnail1.png")
renderCard(2, "Rubidi", "Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem v Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem lorem 14 15 16 17 18 hehe 20 14 15 16 17 18 hehe 20", 0, "LOH_thumbnail2.png")
renderCard(3, "Diamond", "HCMUs", 1, "LOH_thumbnail3.png")

# ------------- Chuyen trang -------------#
ImgUnclicked1 = convertImage("LOH_Unclicked1.png", 76, 76)
ImgUnclicked2 = convertImage("LOH_Unclicked2.png", 76, 76)
ImgUnclicked3 = convertImage("LOH_Unclicked3.png", 76, 76)
ImgUnclicked4 = convertImage("LOH_Unclicked4.png", 76, 76)
ImgClicked1 = convertImage("LOH_Clicked1.png", 76, 76)
ImgClicked2 = convertImage("LOH_Clicked2.png", 76, 76)
ImgClicked3 = convertImage("LOH_Clicked3.png", 76, 76)
ImgClicked4 = convertImage("LOH_Clicked4.png", 76, 76)

pageBtnFrame = Frame()
pageBtnFrame.configure(bg="#ffffff")
pageBtnFrame.place(
    x=convertSize(506), y=convertSize(780),
    width=convertSize(586),
    height=convertSize(76))


def page1():  # 1C 2U 3U 4U
    unclicked1Btn.place_forget()
    clicked2Btn.place_forget()
    clicked3Btn.place_forget()
    clicked4Btn.place_forget()

    clicked1Btn.place(
        x=convertSize(102), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    unclicked2Btn.place(
        x=convertSize(204), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    unclicked3Btn.place(
        x=convertSize(306), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    unclicked4Btn.place(
        x=convertSize(408), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))


def page2():  # 1U 2C 3U 4U
    clicked1Btn.place_forget()
    unclicked2Btn.place_forget()
    clicked3Btn.place_forget()
    clicked4Btn.place_forget()

    unclicked1Btn.place(
        x=convertSize(102), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    clicked2Btn.place(
        x=convertSize(204), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    unclicked3Btn.place(
        x=convertSize(306), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    unclicked4Btn.place(
        x=convertSize(408), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))


def page3():  # 1U 2U 3C 4U
    clicked1Btn.place_forget()
    clicked2Btn.place_forget()
    unclicked3Btn.place_forget()
    clicked4Btn.place_forget()

    unclicked1Btn.place(
        x=convertSize(102), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    unclicked2Btn.place(
        x=convertSize(204), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    clicked3Btn.place(
        x=convertSize(306), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    unclicked4Btn.place(
        x=convertSize(408), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))


def page4():  # 1U 2U 3U 4C
    clicked1Btn.place_forget()
    clicked2Btn.place_forget()
    clicked3Btn.place_forget()
    unclicked4Btn.place_forget()

    unclicked1Btn.place(
        x=convertSize(102), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    unclicked2Btn.place(
        x=convertSize(204), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    unclicked3Btn.place(
        x=convertSize(306), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))
    clicked4Btn.place(
        x=convertSize(408), y=convertSize(0),
        width=convertSize(76),
        height=convertSize(76))


# Button "1" (Unclicked)
unclicked1Btn = Button(
    master=pageBtnFrame,
    image=ImgUnclicked1,
    borderwidth=0,
    highlightthickness=0,
    command=page1,
    relief="flat"
)

# Button "2" (Unclicked)
unclicked2Btn = Button(
    master=pageBtnFrame,
    image=ImgUnclicked2,
    borderwidth=0,
    highlightthickness=0,
    command=page2,
    relief="flat"
)

# Button "3" (Unclicked)
unclicked3Btn = Button(
    master=pageBtnFrame,
    image=ImgUnclicked3,
    borderwidth=0,
    highlightthickness=0,
    command=page3,
    relief="flat"
)

# Button "4" (Unclicked)
unclicked4Btn = Button(
    master=pageBtnFrame,
    image=ImgUnclicked4,
    borderwidth=0,
    highlightthickness=0,
    command=page4,
    relief="flat"
)

# Button "1" (Clicked)
clicked1Btn = Button(
    master=pageBtnFrame,
    image=ImgClicked1,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)

# Button "2" (Clicked)
clicked2Btn = Button(
    master=pageBtnFrame,
    image=ImgClicked2,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)

# Button "3" (Clicked)
clicked3Btn = Button(
    master=pageBtnFrame,
    image=ImgClicked3,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)

# Button "4" (Clicked)
clicked4Btn = Button(
    master=pageBtnFrame,
    image=ImgClicked4,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)

page1()
# currPage = 1
# def increasePage():
#     currPage = currPage + 1
#     if currPage == 2:
#         page2()
#     elif currPage == 3:
#         page3()
#     elif currPage == 4:
#         page4()
#     else:
#         currPage = 4

# def decreasePage():
#     currPage = currPage - 1
#     if currPage == 1:
#         page1()
#     elif currPage == 2:
#         page2()
#     elif currPage == 3:
#         page3()
#     else:
#         currPage = 1


# # Button "Prev"
# ImgPrevBtn = convertImage("LOH_PrevBtn.png", 76, 76)
# prevBtn = Button(
#     master=pageBtnFrame,
#     image = ImgPrevBtn,
#     borderwidth = 0,
#     highlightthickness = 0,
#     command = decreasePage,
#     relief = "flat")
# prevBtn.place(
#     x = convertSize(0), y = convertSize(0),
#     width = convertSize(76),
#     height = convertSize(76))

# # Button "Next"
# ImgNextBtn = convertImage("LOH_NextBtn.png", 76, 76)
# nextBtn = Button(
#     master=pageBtnFrame,
#     image = ImgNextBtn,
#     borderwidth = 0,
#     highlightthickness = 0,
#     command = increasePage,
#     relief = "flat")
# nextBtn.place(
#     x = convertSize(510), y = convertSize(0),
#     width = convertSize(76),
#     height = convertSize(76))


window.resizable(False, False)
window.mainloop()
