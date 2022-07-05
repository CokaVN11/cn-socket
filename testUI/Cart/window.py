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

# ====================== Note Chia Frame ==========================#

################### window ######################
#          Item Frame            #  Info Frame  #
#                                #              #
# #############################  #              #
# #        Item Canvas        #S #              #
# #                           #C #              #
# #  #######################  #R #              #
# #  #    Scrollable       #  #O #              #
# #  #           Frame     #  #L #              #
# #  #                     #  #L #              #
# #  #   Thì xem cái frame #  #  #              #
# #  #  này như là window  #  #B #              #
# #  #                     #  #A #              #
# #  #    Tạo ra trong     #  #R #              #
# #  #  frame này những    #  #  #              #
# #  #  cái card frame     #  #  #              #

itemFrameWidth = convertSize(900)
itemFrameHeight = convertSize(900)

infoFrameWidth = convertSize(700)
infoFrameHeight = convertSize(900)

itemFrame = Frame(window)
itemFrame.place(x=0, y=0,
                width=itemFrameWidth,
                height=itemFrameHeight)

infoFrame = Frame(window)
infoFrame.place(x=itemFrameWidth, y=0,
                width=infoFrameWidth,
                height=infoFrameHeight)

itemCanvas = Canvas(
    itemFrame,
    bg="#ffffff",
    height=itemFrameHeight,
    width=itemFrameWidth,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
itemCanvas.place(x=0, y=0)

infoCanvas = Canvas(
    infoFrame,
    bg="#ffffff",
    height=infoFrameHeight,
    width=infoFrameWidth,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
infoCanvas.place(x=0, y=0)

# =================== Init Scrollbar for ItemFrame ======================#
numberOfItem = 6  # The number of items in Cart
scrollFrameHeight = convertSize(102 + numberOfItem * 222)

scrollBar = Scrollbar(itemFrame, orient='vertical', command=itemCanvas.yview)
scrollBar.pack(side=RIGHT, fill=Y)

scrollableFrame = Frame(itemCanvas,
                        width=itemFrameWidth,
                        height=scrollFrameHeight,
                        background="white")
# scrollableFrame.place(
#     x = 0,
#     y = 0,
# )
scrollableFrame.bind(
    "<Configure>",
    lambda e: itemCanvas.configure(
        scrollregion=itemCanvas.bbox("all")
    )
)

itemCanvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

itemCanvas.configure(yscrollcommand=scrollBar.set)

# ================ Add widgets to scrollableFrame ==================#
containerFrame = Frame(scrollableFrame,
                       width=itemFrameWidth,
                       height=scrollFrameHeight,
                       background="white")
containerFrame.place(x=0, y=0)

# ========== Button "Back"
ImgBackBtn = convertImage("Cart_backBtn.png", 137, 44)
backBtn = Button(
    containerFrame,
    image=ImgBackBtn,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)
backBtn.place(
    x=convertSize(43), y=convertSize(30),
    width=convertSize(137),
    height=convertSize(44)
)

cardWidth = convertSize(819)
cardHeight = convertSize(200)

firstCardX = convertSize(31)
firstCardY = convertSize(102)
cardDiscrepancy = convertSize(324 - 102)

thumbnailX = convertSize(819 / 2)
thumbnailY = convertSize(200 / 2)

namePosX = convertSize(337 - 31 - 2)
namePosY = convertSize((118 - 102) - 12)

datePosX = convertSize(337 - 31 - 2)
datePosY = convertSize(162 - 102 + 4)

quantityPosX = convertSize(376 - 31 + 10)
quantityPosY = convertSize(244 - 102 - 4 + 14)

pricePosX = convertSize(648 - 31 + 186)
pricePosY = convertSize((240 - 102) + 14)

decreaseBtnX = convertSize(339 - 31)
decreaseBtnY = convertSize(245 - 102)
increaseBtnX = convertSize(406 - 31)
increaseBtnY = convertSize(245 - 102)

ImgThumbnail = convertImage("Cart_thumbnail.png", 819, 200)
ImgIncreaseBtn = convertImage("Cart_increaseBtn.png", 28, 28)
ImgDecreaseBtn = convertImage("Cart_decreaseBtn.png", 28, 28)


def renderCard(Row, hotelName, typeRoom, arrivalDate, departureDate, quantityRoom, thumbnail, pricePerRoom):
    # CARD ITEM FRAME
    cardFrame = Frame(containerFrame)
    cardFrame.place(
        x=firstCardX,
        y=firstCardY + cardDiscrepancy * (Row - 1),
        width=cardWidth,
        height=cardHeight)

    cardCanvas = Canvas(
        cardFrame,
        bg="#ffffff",
        height=cardHeight,
        width=cardWidth,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    cardCanvas.place(x=0, y=0)

    # ========== Card Thumbnail
    card_Thumbnail = cardCanvas.create_image(
        thumbnailX,
        thumbnailY,
        image=ImgThumbnail
    )

    # ========== Card Name
    card_Name = Label(
        master=cardFrame,
        text=f'{hotelName} ({typeRoom})',
        foreground="#47423D",
        background="#ffffff",
        justify=LEFT,
        font=("Noto Sans Bold", convertSize(24))
    ).place(
        x=namePosX,
        y=namePosY,
        height=convertSize(60)
    )

    # ========== Card Date
    card_Date = Label(
        master=cardFrame,
        text=f"{arrivalDate} - {departureDate}",
        foreground="#7D8693",
        background="#ffffff",
        justify=LEFT,
        font=("Hind Guntur SemiBold", convertSize(16))
    ).place(
        x=datePosX,
        y=datePosY,
    )

    # ========== Card Price
    money = "departDate - arrivalDate" * pricePerRoom

    card_Price = Label(
        master=cardFrame,
        anchor="e",
        # text = f"${quantityRoom * money}",
        text="$123",
        foreground="#35bdda",
        background="white",
        justify=RIGHT,
        font=("Noto Sans Bold", convertSize(30)),
        width=convertSize(8)
    ).place(
        anchor="e",
        x=pricePosX,
        y=pricePosY,
        height=convertSize(80)
    )

    # ========== Quantity Label (Dùng Canvas tạo text vì Label dính background)
    cardCanvas.create_text(
        quantityPosX,
        quantityPosY,
        text=f"{quantityRoom}",
        fill="#000000",
        font=("Noto Sans Regular", convertSize(16))
    )

    # ========== Button "-"
    decreaseBtn = Button(
        master=cardFrame,
        image=ImgDecreaseBtn,
        borderwidth=0,
        highlightthickness=0,
        command=btn_clicked,
        relief="flat"
    )
    decreaseBtn.place(
        x=decreaseBtnX,
        y=decreaseBtnY,
        width=convertSize(28),
        height=convertSize(28)
    )
    # ========== Button "+"
    increaseBtn = Button(
        master=cardFrame,
        image=ImgIncreaseBtn,
        borderwidth=0,
        highlightthickness=0,
        command=btn_clicked,
        relief="flat"
    )
    increaseBtn.place(
        x=increaseBtnX,
        y=increaseBtnY,
        width=convertSize(28),
        height=convertSize(28)
    )


# Chú ý biến numberOfItem ở line 99
renderCard(1, "Lake Place", "Single Room",
           "04/07/2022", "07/07/2022", 2, "#thumbnailPath", 200)
renderCard(2, "Lake Place", "Single Room",
           "04/07/2022", "07/07/2022", 1, "#thumbnailPath", 200)
renderCard(3, "Lake Place", "Single Room",
           "04/07/2022", "07/07/2022", 12, "#thumbnailPath", 200)
renderCard(4, "Lake Place", "Single Room",
           "04/07/2022", "07/07/2022", 2, "#thumbnailPath", 200)
renderCard(5, "Lake Place", "V.I.P Room",
           "04/07/2022", "07/07/2022", 2, "#thumbnailPath", 200)
renderCard(6, "Lake Place", "Single Room",
           "04/07/2022", "07/07/2022", 2, "#thumbnailPath", 200)

# ==================== INFORMATION FRAME =====================#
ImgBackground = convertImage("Cart_background.png", 603, 516)
ImgConfirmBtn = convertImage("Cart_confirmBtn.png", 455, 87)

# ========== Background
background = infoCanvas.create_image(
    convertSize((950 - 900) + (603 / 2)),
    convertSize(134 + (516 / 2)),
    image=ImgBackground
)

# =========== Username
infoUsername = Label(
    master=infoFrame,
    anchor="e",
    text="devilboiz",
    foreground="#7D8693",
    background="#ffffff",
    justify=RIGHT,
    font=("Hind Guntur SemiBold", convertSize(22)),
    width=convertSize(24)
).place(
    anchor="e",
    x=convertSize((1272 - 900) + 270),
    y=convertSize(213 + 20),
    height=convertSize(40)
)

# =========== Bank Account
infoBankAccount = Label(
    master=infoFrame,
    anchor="e",
    text="1234567890",
    foreground="#7D8693",
    background="#ffffff",
    justify=RIGHT,
    font=("Hind Guntur SemiBold", convertSize(22)),
    width=convertSize(24)
).place(
    anchor="e",
    x=convertSize((1272 - 900) + 270),
    y=convertSize(213 + 20 + (262 - 213)),
    height=convertSize(40)
)

# =========== SubTotal
infoSubTotal = Label(
    master=infoFrame,
    anchor="e",
    text="$800",
    foreground="#7D8693",
    background="#ffffff",
    justify=RIGHT,
    font=("Hind Guntur SemiBold", convertSize(22)),
    width=convertSize(24)
).place(
    anchor="e",
    x=convertSize((1272 - 900) + 270),
    y=convertSize(213 + 20 + (463 - 213)),
    height=convertSize(40)
)

# =========== Tax
infoTax = Label(
    master=infoFrame,
    anchor="e",
    text="$80",
    foreground="#7D8693",
    background="#ffffff",
    justify=RIGHT,
    font=("Hind Guntur SemiBold", convertSize(22)),
    width=convertSize(24)
).place(
    anchor="e",
    x=convertSize((1272 - 900) + 270),
    y=convertSize(213 + 20 + (518 - 213)),
    height=convertSize(40)
)

# =========== Total
infoTotal = Label(
    master=infoFrame,
    anchor="e",
    text="$880",
    foreground="#35BDDA",
    background="#ffffff",
    justify=RIGHT,
    font=("Hind Guntur Bold", convertSize(36)),
).place(
    anchor="e",
    x=convertSize((1272 - 900) + 270),
    y=convertSize(213 + (594 - 213) + 36),
    height=convertSize(60)
)

# ========== Button "Confirm"
confirmBtn = Button(
    master=infoFrame,
    image=ImgConfirmBtn,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)
confirmBtn.place(
    x=convertSize(1024 - 900), y=convertSize(691),
    width=convertSize(455),
    height=convertSize(87)
)

window.resizable(False, False)
window.mainloop()
