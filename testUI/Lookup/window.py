from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("1600x900")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 900,
    width = 1600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    800.0, 669.0,
    image=background_img)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 471, y = 739,
    width = 91,
    height = 42)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b1.place(
    x = 1216, y = 732,
    width = 234,
    height = 68)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    800.0, 317.0,
    image=background_img)

canvas.create_text(
    800.0, 215.0,
    text = "Single Room",
    fill = "#47423d",
    font = ("None", int(44.0)))

canvas.create_text(
    921.0, 304.5,
    text = "Small room with standard conditions. lorem ipsum dolor sit amet. lorem ipsum dolor sit amet. lorem ipsum dolor sit amet",
    fill = "#7d8693",
    font = ("HindGuntur-Medium", int(24.0)))

canvas.create_text(
    1356.5, 223.0,
    text = "$100",
    fill = "#35bdda",
    font = ("None", int(60.0)))

canvas.create_text(
    983.0, 422.5,
    text = "2 Guest",
    fill = "#8f8f8f",
    font = ("None", int(20.0)))

canvas.create_text(
    843.5, 424.5,
    text = "68 m2",
    fill = "#8f8f8f",
    font = ("None", int(20.0)))

canvas.create_text(
    706.5, 422.5,
    text = "1 Bed",
    fill = "#8f8f8f",
    font = ("None", int(20.0)))

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 1216, y = 380,
    width = 234,
    height = 68)

img3 = PhotoImage(file = f"img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b3.place(
    x = 401, y = 389,
    width = 161,
    height = 42)

img4 = PhotoImage(file = f"img4.png")
b4 = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b4.place(
    x = 1462, y = 30,
    width = 109,
    height = 109)

img5 = PhotoImage(file = f"img5.png")
b5 = Button(
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b5.place(
    x = 41, y = 44,
    width = 227,
    height = 55)

canvas.create_text(
    800.0, 80.0,
    text = "Lake Place Hotel",
    fill = "#47423d",
    font = ("Sarabun-SemiBold", int(60.0)))

window.resizable(False, False)
window.mainloop()
