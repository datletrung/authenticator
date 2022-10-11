from tkinter import *
from tkinter import ttk


root = Tk()
root.title('Theme Demo')
root.geometry('400x300')

s = ttk.Style()
s.theme_use('clam')


ttk.Label(root, text='sagasdghashashd').pack()
ttk.Button(root, text='sagasdghashashd').pack()
root.mainloop()
