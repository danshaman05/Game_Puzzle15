import tkinter
import random
from PIL import Image, ImageTk


#treba vytvorit 16 malych casti obrazku, kt. sa priradia do 16 premennych 


class Plocha:
    def __init__(self):
        self.canvas = tkinter.Canvas(width=100*4, height=100*4+50)
        self.canvas.pack()

##        self.pole = [[i for i in range(j*4 + 1, (j+1)*4 + 1)] for j in range(4)] #vygeneruje 2-dim pole od 1-16
##        self.pole[3][3] = 0 #prave dolne policko je prazdne, teda 0
##
##        self.pole = [random.shuffle(x[:]) for x in self.pole]#nahodne rozhodi pole

        earth = Image.open('earth.jpg')
        earth1 = earth.resize((400, 400))
        img1 = ImageTk.PhotoImage(earth1)
        self.canvas.create_image(0, 0, image=img1)
        

        cisla = [x for x in range(1,16)]
        random.shuffle(cisla) #nahodne zamiesa
        cisla.append(0)
        
        #print(cisla)
        #self.pole = [[cisla[j][i] for i in range(4)] for j in range(4)]



        self.pole = []
        ind = 0
        for i in range(4):
            riadok = []
            for j in range(4):
                riadok.append(cisla[ind])
                ind += 1
            self.pole.append(riadok)

    

        self.poc_tahov = 0
        self.poz_nuly = [3, 3] #pozicia prazdneho policka

        self.canvas.bind_all('<Up>', self.posun_hore)
        self.canvas.bind_all('<Down>', self.posun_dole)
        self.canvas.bind_all('<Right>', self.posun_vpravo)
        self.canvas.bind_all('<Left>', self.posun_vlavo)

        #self.x, self.y, self.dx, self.dy = 0, 0, 0, 0


    def dalsi_tah(self): #zmenit na pocet tahov!!
        self.poc_tahov += 1
        
    def nula(self):
        return tuple(self.poz_nuly)

##    def vnutri(self, x, y): # DOROBIT ak budem robit posun/klik mysou


    def stvorec(self, x, y, cislo):
        self.canvas.create_rectangle(x, y, x+100, y+100, width=1, outline='black')
        self.canvas.create_text(x+50, y+50, font='arial 50 bold', fill='blue', text=cislo)

    def vykresli(self):
        self.canvas.delete('all')
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                self.stvorec(j*100, i*100, self.pole[i][j])
        
            
    def volne(self): #vracia policka, ktorymi sa da hybat a smer kde je nula vzhladom k nim
        self.dic = {}
        for i in range(4):
            
            if self.nula()[1] > 0: #policko vlavo od nuly
                policko = self.nula()[0], self.nula()[1]-1
                self.dic['l'] = policko

            if self.nula()[1] < 3: #policko vpravo od nuly
                policko = self.nula()[0], self.nula()[1]+1
                self.dic['p'] = policko

            if self.nula()[0] > 0: #policko hore od nuly
                policko = self.nula()[0]-1, self.nula()[1]
                self.dic['h'] = policko

            if self.nula()[0] < 3: #policko dole od nuly
                policko = self.nula()[0]+1, self.nula()[1]
                self.dic['d'] = policko
            
        return self.dic

    def vymen_policka(self, smer):
        policko = self.volne()[smer]
        self.pole[self.nula()[0]][self.nula()[1]] = self.pole[policko[0]][policko[1]]
        self.pole[policko[0]][policko[1]] = 0

    def posun_hore(self, event):
        if 'h' in self.volne():
            self.vymen_policka('h')            

            self.vykresli()
            self.poz_nuly[0] -= 1
            self.volne()


    def posun_dole(self, event):
        if 'd' in self.volne():
            self.vymen_policka('d') 

            self.vykresli()
            self.poz_nuly[0] += 1
            self.volne()

            
    def posun_vlavo(self, event):
        
        if 'l' in self.volne():
            self.vymen_policka('l') 

            self.vykresli()
            self.poz_nuly[1] -= 1
            self.volne()
            
    def posun_vpravo(self, event):
        if 'p' in self.volne():
            self.vymen_policka('p') 

            self.vykresli()
            self.poz_nuly[1] += 1
            self.volne()

##class Stvorec:
##    def __init__(self, x, y, sirka=100, vyska=100):
##        
##    

class Program:
    def __init__(self):
        
        self.okno = tkinter.Tk() # vytv. graf. okno
        self.plocha = Plocha()

        self.plocha.vykresli()
         
        tkinter.mainloop()

w = Program()


##
##def test():
##    print(w.plocha.pole)
##    print(w.plocha.volne())
##
##test()


def test2():
    print(w.plocha.pole)
    print(w.plocha.volne())

    earth = Image.open('earth.jpg')
    earth.show()
##test2()
