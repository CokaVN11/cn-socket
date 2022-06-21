from tkinter import *

window = Tk()

window.title('E-Booking')
window.geometry('600x400')

#Thêm label có nội dung Hello, font chữ
lbl = Label(window, text="Hello", font=("Arial Bold", 50))

#Xác định vị trí của label
lbl.grid(column=0, row=0)


window.mainloop()