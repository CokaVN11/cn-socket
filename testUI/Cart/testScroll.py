from cgitb import text
from tkinter import *
from math import floor
from PIL import Image, ImageTk

scaleRate = 0.8
def convertSize(originalSize):
    frameWidth = window.winfo_screenwidth() * scaleRate
    return floor((frameWidth * originalSize) / 1600)


# originalWidth & originalHeight are the Width and Height on Figma
def convertImage(path, originalWidth, originalHeight):
    originalImage = Image.open(path)
    resizedImage = originalImage.resize((convertSize(originalWidth), convertSize(originalHeight)))
    convertedImage = ImageTk.PhotoImage(resizedImage)
    return convertedImage


# create root window
window = Tk()
window.geometry("800x500")

itemFrame = Frame(window)
itemFrame.place(x=0, y=0, width=500, height=500)

infoFrame = Frame(window)
infoFrame.place(x=500, y=0, width=300, height=500)


itemCanvas = Canvas(
    itemFrame,
    bg="#666666",
    height=500,
    width=500,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
itemCanvas.place(x=0, y=0)

infoCanvas = Canvas(
    infoFrame,
    bg="#222222",
    height=500,
    width=300,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
infoCanvas.place(x=0, y=0)


################### window ##################
#          Item Frame        #  Info Frame  #  
#                            #              #  
# ########################## #              #  
# #        Item Canvas     #S#              #  
# #                        #C#              #  
# #  ####################  #R#              #  
# #  #    Scrollable    #  #O#              #  
# #  #           Frame  #  #L#              #  
# #  #                  #  #L#              #  
# #  #                  #  # #              #  
# #  #                  #  #B#              #  
# #  #                  #  #A#              #  
# #  #                  #  #R#              #  
# #  #                  #  # #              #  
# #  #                  #  # #              #  


scrollBar = Scrollbar(itemFrame, orient='vertical', command=itemCanvas.yview)
scrollBar.pack(side = RIGHT, fill = Y)

scrollableFrame = Frame(itemCanvas,width=500, height=1000, background="blue")
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


# ========== Để widget vào scrollable frame ============= #
ImgThumbnail = convertImage("LK_room5_single.png", 400, 500)

itemInCart = 5

testFrame = Frame(scrollableFrame, width=500, height=999, background="red")
testFrame.place(x = 0, y = 0)



for i in range(5):
    cardCanvas = Canvas(
        testFrame,
        bg="#ffffff",
        height=200,
        width=400,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    cardCanvas.place(x=0, y=i*220)


  






window.mainloop()

		
