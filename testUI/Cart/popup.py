from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
name = askstring('Go2Chill', 'Any note ?', width=200)
showinfo('Hello!', 'Hi, {}'.format(name))