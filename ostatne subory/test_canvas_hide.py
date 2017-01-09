import tkinter

canvas = tkinter.Canvas()
canvas.pack()

id1 = canvas.create_text(100, 20, text='ahoj')
id2 = canvas.create_rectangle(20, 20, 100, 100, fill='black')



id3 = canvas.create_rectangle(30, 20, 50, 100, fill='gold')

canvas.itemconfig(id3, state='hidden')


#VYSLEDOK TESTU:
# itemy v canvase sa daju skryt!:
#canvas.itemconfig(id3, state='hidden')
