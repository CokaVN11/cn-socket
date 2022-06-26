from tkinter import *


window = Tk()

window.geometry("800x500")
window.configure(bg = "#ffffff")

# Todo :
#     - Tạo hàm tạo chữ
#     - Tạo fake data
#     - Tạo nút chuyển trang
#     - Xử lí chuyển trang


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


# Background
Background = canvas.create_image(
    400.0, 225.0,
    image=LOH_Background
)

###########============== Rows
renderRow("Demacia", "Hehe I haven't go to this hotel", "Availble", 1)
renderRow("Leaf", "My favorite place", "Availble", 2)
renderRow("HCMUS", "I go to here everyday", "Full", 3)
renderRow("Noxus", "Lorem ipsum dolor sit amet", "Availble", 4)
renderRow("Figma", "Lorem ipsum dolor sit amet", "Availble", 5)




window.resizable(False, False)
window.mainloop()
