from tkinter import *

window = Tk()

window.geometry("800x500")
window.configure(bg = "#ffffff")

canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 500,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

# Todo :
#     - Tạo hàm tạo chữ /
#     - Tạo fake data /
#     - Tạo nút chuyển trang
#     - Xử lí chuyển trang

hotelList = [
    {
        "name" : "Abc",
        "description" : "My favorite hotel",
        "status" : "Available"
    },
    {
        "name" : "Demacia",
        "description" : "Niceeee",
        "status" : "Available"
    },
    {
        "name" : "Leaf",
        "description" : "Lorem ipsum dolor sit amet",
        "status" : "Available"
    },
    {
        "name" : "HCMUS",
        "description" : "I go to here everyday",
        "status" : "Available"
    },
    {
        "name" : "Noxus",
        "description" : "Love it",
        "status" : "Available"
    },
    {
        "name" : "Figma",
        "description" : "Hehe test long long pai pai",
        "status" : "Available"
    }
]

#==================== Constants Declaration ====================#
rowHeight = 50

nameX = 65
descriptionX = 327
statusX = 594
firstRowTextY = 75

firstRowButtonY = 56
buttonX = 681

fontSize = 16
fontFamily = "Roboto Bold"

#==================== Image Declaration ====================#
LOH_Background = PhotoImage(file = "./assets/LOH_Background.png")
LOH_Button = PhotoImage(file = "./assets/LOH_Button.png")


def renderRow(nameData, descriptionData, statusData, row):
    canvas.create_text(
        nameX, firstRowTextY + (row-1)*rowHeight,
        text = nameData,
        fill = "#000000",
        font = (fontFamily, fontSize)
    )
    canvas.create_text(
        descriptionX, firstRowTextY + (row-1)*rowHeight,
        text = descriptionData,
        fill = "#000000",
        font = (fontFamily, fontSize)
    )
    canvas.create_text(
        statusX, firstRowTextY + (row-1)*rowHeight,
        text = statusData,
        fill = "#000000",
        font = (fontFamily, fontSize)
    )
    ButtonWhite = Button(
        image = LOH_Button,
        borderwidth = 0,
        highlightthickness = 0,
        command = lambda:print("Row", row) ,
        relief = "flat"
    )
    ButtonWhite.place(
        x = buttonX, y = firstRowButtonY + (row-1)*rowHeight,
        width = 104,
        height = 38
    )

def listOfHotelsScreen():

    # Background
    Background = canvas.create_image(
        400.0, 225.0,
        image=LOH_Background
    )

    ###########============== Rows
    rowIndex = 1
    for hotel in hotelList:
        renderRow(hotel["name"], hotel["description"], hotel["status"], rowIndex)
        rowIndex = rowIndex + 1

listOfHotelsScreen()


window.resizable(False, False)
window.mainloop()
