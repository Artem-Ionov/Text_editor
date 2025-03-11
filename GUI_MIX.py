from tkinter import *

def button(root, text, command=None, side=LEFT):
    btn=Button(root, text=text, command=command)
    btn.config(width=6)
    btn.pack(side=side)       
    return btn

P=[]
def button2(root, pict, command=None, side=LEFT):
    btn=Button(root, command=command)
    img=PhotoImage(file='PictureMin/%s' % pict)
    btn.config(image=img, width=40, height=40)
    btn.pack(side=side)
    P.append(img)
    return btn

def option(root, command=None, *fonts,  font1):
    var=IntVar()
    opt=OptionMenu(root, var, command=command, *fonts)
    opt.pack()
    var.set(font1)
    return var


