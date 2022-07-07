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
reservationFrame = Frame(window)
reservationFrame.place(
    x = 0,
    y = 0,
    width = windowWidth,
    height = windowHeight
)

reservationCanvas = Canvas(
    reservationFrame,
    bg="#ffffff",
    height=windowHeight,
    width=windowWidth,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
reservationCanvas.place(x=0, y=0)

numberOfItem = 6    # The number of items in Cart
scrollFrameHeight = convertSize(157 + numberOfItem*298)

scrollBar = Scrollbar(
    reservationFrame, 
    orient='vertical', 
    command=reservationCanvas.yview
)
scrollBar.pack(side = RIGHT, fill = Y)

scrollableFrame = Frame(
    reservationCanvas,
    width=windowWidth, 
    height=scrollFrameHeight, 
    background="white"
)

scrollableFrame.bind(
    "<Configure>",
    lambda e: reservationCanvas.configure(
        scrollregion=reservationCanvas.bbox("all")
    )
)

reservationCanvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

reservationCanvas.configure(yscrollcommand=scrollBar.set)




# ================ Add widgets to scrollableFrame ==================#
containerFrame = Frame(
    scrollableFrame, 
    width=windowWidth, 
    height=scrollFrameHeight, 
    background="white"
)
containerFrame.place(x = 0, y = 0)

# ========== Button "Back"
ImgBackBtn = convertImage("Res_backBtn.png", 227, 55)
backBtn = Button(
    containerFrame,
    image = ImgBackBtn,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat"
)
backBtn.place(
    x = convertSize(41), y = convertSize(44),
    width = convertSize(227),
    height = convertSize(55)
)
    
# ========== Title
titleReservation = Label(
    containerFrame,
    text = "Your Reservation",
    foreground="#47423D",
    background="#ffffff",
    justify=CENTER,
    font=("Noto Sans SemiBold", convertSize(36))
).place(
    x = windowWidth/2 ,
    y = convertSize(84),
    anchor="center"
)

#
# ImgTemplate = convertImage("template.png", 1378, 272)
# heheTemplate = Button(
#     containerFrame,
#     image = ImgTemplate,
#     borderwidth = 0,
#     highlightthickness = 0,
#     command = btn_clicked,
#     relief = "flat")
# heheTemplate.place(
#     x = convertSize(122), y = convertSize(157),
#     width = convertSize(1378),
#     height = convertSize(272))

# # ==================== CARD Constants ====================#
cardWidth = convertSize(1378)
cardHeight = convertSize(272)

firstCardX = convertSize(122)
firstCardY = convertSize(157)
cardDiscrepancy = convertSize(455 - 157)

thumbnailX = convertSize(1378 / 2)
thumbnailY = convertSize(272 / 2)

namePosX = convertSize(544 - 122 - 2)
namePosY = convertSize((177 - 157) - 10)

datePosX = convertSize(544 - 122 - 2)
datePosY = convertSize(245 - 157 - 6)

quantityPosX = convertSize(544 - 122 - 2)
quantityPosY = convertSize(289 - 157 - 6)

resIdPosX = convertSize(544 - 122 - 2)
resIdPosY = convertSize(333 - 157 - 6)

resTimePosX = convertSize(544 - 122 - 2)
resTimePosY = convertSize(377 - 157 - 6)

pricePosX = convertSize(1294 - 122 + 186)
pricePosY = convertSize((174 - 157) + 32)

cancelPosX = convertSize(1301 - 122)
cancelPosY = convertSize(353 - 157)

ImgThumbnail = convertImage("background.png", 1378, 272)
ImgCancelBtn = convertImage("Res_cancelBtn.png", 170, 54)

def renderCard(Row, hotelName, typeRoom, arrivalDate, departureDate, quantityRoom, thumbnail, pricePerRoom, enableCancel):
    # CARD ITEM FRAME
    cardFrame = Frame(containerFrame)
    cardFrame.place(
        x=firstCardX,
        y=firstCardY + cardDiscrepancy*(Row - 1),
        width=cardWidth,
        height=cardHeight
    )

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


    #========== Card Thumbnail
    card_Thumbnail = cardCanvas.create_image(
        thumbnailX, 
        thumbnailY,
        image=ImgThumbnail
    )

    #========== Card Name
    card_Name = Label(
        master=cardFrame,
        text= f'{hotelName} ({typeRoom})',
        foreground="#47423D",
        background="#ffffff",
        justify=LEFT,
        font=("Noto Sans Bold", convertSize(32))
    ).place(
        x=namePosX,
        y=namePosY,
        height=convertSize(68)
    )

    #========== Card Date
    card_Date = Label(
        master=cardFrame,
        text = f"{arrivalDate} - {departureDate}",
        foreground="#7D8693",
        background="#ffffff",
        justify=LEFT,
        font=("Hind Guntur SemiBold", convertSize(18))
    ).place(
        x=datePosX,
        y=datePosY,
        height=convertSize(40)
    )

    #========== Card Quantity
    card_Quantity = Label(
        master=cardFrame,
        text = f"Quantity : {quantityRoom}",
        foreground="#7D8693",
        background="#ffffff",
        justify=LEFT,
        font=("Hind Guntur SemiBold", convertSize(18))
    ).place(
        x=quantityPosX,
        y=quantityPosY,
        height=convertSize(40)
    )

    #========== Card Reservation ID
    card_Id = Label(
        master=cardFrame,
        text = "Reservation ID : 123567890",
        foreground="#7D8693",
        background="#ffffff",
        justify=LEFT,
        font=("Hind Guntur SemiBold", convertSize(18))
    ).place(
        x=resIdPosX,
        y=resIdPosY,
        height=convertSize(40)
    )

    #========== Card Reservation Time
    card_Time = Label(
        master=cardFrame,
        text = "Reservation Time : 04/07/2022 - 17:06",
        foreground="#7D8693",
        background="#ffffff",
        justify=LEFT,
        font=("Hind Guntur SemiBold", convertSize(18))
    ).place(
        x=resTimePosX,
        y=resTimePosY,
        height=convertSize(40)
    )

    #=========== Card Price
    card_Price = Label(
        master=cardFrame,
        anchor="e",
        text = "$300",
        foreground="#35bdda",
        background="#ffffff",
        justify=RIGHT,
        font=("Noto Sans Bold", convertSize(42)),
        width= convertSize(10)
    ).place(
        anchor="e",
        x=pricePosX,
        y=pricePosY,
        height = convertSize(80)
    )

    if enableCancel == True:
        card_cancelBtn = Button(
            cardFrame,
            image = ImgCancelBtn,
            borderwidth = 0,
            highlightthickness = 0,
            command = btn_clicked,
            relief = "flat"
        )
        card_cancelBtn.place(
            x = cancelPosX, 
            y = cancelPosY,
            width = convertSize(170),
            height = convertSize(54)
        )

renderCard(1, "Lake Place", "Single Room", 
            "04/07/2022", "07/07/2022", 2, "#thumbnailPath", 200, True)
renderCard(2, "Lake Place", "V.I.P Room", 
            "06/07/2022", "08/07/2022", 1, "#thumbnailPath", 200, False)
renderCard(3, "Hehe Hotel", "Single Room", 
            "04/07/2022", "07/07/2022", 12, "#thumbnailPath", 200, True)
renderCard(4, "Hehe Hotel", "Double Room", 
            "02/07/2022", "07/07/2022", 2, "#thumbnailPath", 200, True)
renderCard(5, "Lake Place", "V.I.P Room", 
            "04/07/2022", "07/07/2022", 2, "#thumbnailPath", 200, True)
renderCard(6, "Lake Place", "Single Room", 
            "04/07/2022", "07/07/2022", 2, "#thumbnailPath", 200, True)

window.resizable(False, False)
window.mainloop()
