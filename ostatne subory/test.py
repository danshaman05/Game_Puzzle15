#test
#ROZDELI OBR NA CASTI !

import tkinter
from PIL import Image, ImageTk

okno = tkinter.Tk()

canvas = tkinter.Canvas(width=500, height=500)
canvas.pack()



#########################
##id1 = canvas.create_text(50, 450, text='Jaruska')
##canvas.itemconfig(id1, text='Danusko')
##
##earth = Image.open('obr/earth.jpg')
##earth = earth.resize((400, 400)) #format Image
##img = ImageTk.PhotoImage(earth)  # format ImageTk
##
##
#### FUNGUJE:
##maly = earth.crop((0,0,100,100))
##maly = ImageTk.PhotoImage(maly)
##
##maly1 = earth.crop((100,0,200,100))
##maly1 = ImageTk.PhotoImage(maly1)
##
####canvas.create_image(0,0, image=maly, anchor='nw')
####canvas.create_image(110,0, image=maly1, anchor='nw')
##
##pole = [maly, maly1]
##
##for i in range(2):
##    canvas.create_image(i*100,0, image=pole[i], anchor='nw')
##
##
##
#### ROZDELI OBR. A VLOZI DO POLA:
##pole = []
##for i in range(0, 400, 100):
##    riadok = []
##    for j in range(0, 400, 100):
##        
##        stvorcek = earth.crop((j, i, j+100, i+100))
##        stvorcek.load() #kvoli lazy vyhodnocovaniu
##        stvorcek = ImageTk.PhotoImage(stvorcek)
##        riadok.append(stvorcek)
##    pole.append(riadok)
##
##
####maly = pole[0][0]
####canvas.create_image(50,50, image=maly)
##
##
##    
#### IDE POLOM A ZOBRAZUJE:
##y = 0
##for riadok in pole:
##    x = 0
##    for obr in riadok:
##        #stvorcek = ImageTk.PhotoImage(obr)
##        
##        canvas.create_image(x, y, image=obr, anchor='nw')
##        x += 110
##    y += 110
##    
###########################################


label1 = tkinter.Label(okno, 100, 100, text='moja kolonka').pack()

