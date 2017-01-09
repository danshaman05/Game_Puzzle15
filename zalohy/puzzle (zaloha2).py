import tkinter
import random
from PIL import Image, ImageTk


#
#treba vytvorit 16 malych casti obrazku, kt. vlozime do pola



class Plocha:
    def __init__(self):
        self.canvas = tkinter.Canvas(width=650, height=100*4+50)
        self.canvas.pack()

##        self.pole = [[i for i in range(j*4 + 1, (j+1)*4 + 1)] for j in range(4)] #vygeneruje 2-dim pole od 1-16
##        self.pole[3][3] = 0 #prave dolne policko je prazdne, teda 0
##
##        self.pole = [random.shuffle(x[:]) for x in self.pole]#nahodne rozhodi pole


        ##########################################
        #PRE OBRAZOK: 

        # NACITA OBR:
        self.obrazok_original = Image.open('obr/earth.jpg')
        obrazok = self.obrazok_original.resize((400, 400)) #format Image
        
        
        

##        self.pocet_tahov()

        
        #Prazdny stvorcek:
        self.prazdny_stv = ImageTk.PhotoImage(Image.new('RGB', (100,100), 'white'))

        #ROZDELI A NACITA DO POLA kusky obrazka:        
        self.pole = []
        
        for i in range(0, 400, 100):
            riadok = []
            for j in range(0, 400, 100):

                if (i, j) == (300, 300):
                    break
                
                stvorcek = obrazok.crop((j, i, j+100, i+100))
                stvorcek.load() #kvoli lazy vyhodnocovaniu
                stvorcek = ImageTk.PhotoImage(stvorcek)
                riadok.append(stvorcek)
            self.pole.append(riadok)

        #KOPIA POLA (kvoli overeniu vitazstva):
        self.pole_riesenie = [x[:] for x in self.pole]
        print(self.pole_riesenie)


        ##########
        #ZAMIESA POLE (3x): 
        #vramci riadkov:
        def miesaj_riadok(pole):
            for riadok in pole:
                riadok = random.shuffle(riadok)

        miesaj_riadok(self.pole)
            
        #vramci stlpcov:
        self.pole_pomocne = [x[:] for x in self.pole]
        
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                self.pole[j][i] = self.pole_pomocne[i][j]
        #3. zamiesanie - vramci riadku:
        miesaj_riadok(self.pole)
        

        #Na koniec prilepi prazdny stvorcek:
        self.pole[3].append(self.prazdny_stv)
        ##########
        
        ##########################################


######################################
        #PRE CISLA:
##        cisla = [x for x in range(1,16)]
##        random.shuffle(cisla) #nahodne zamiesa
##        cisla.append(0) #pripojime aby bola na konci
##        
##        #self.pole = [[cisla[j][i] for i in range(4)] for j in range(4)]
##
##
##    
##        #urobi 2-dim pole z pola cisla:
##        self.pole = []
##        ind = 0
##        for i in range(4):
##            riadok = []
##            for j in range(4):
##                riadok.append(cisla[ind])
##                ind += 1
##            self.pole.append(riadok)
######################################
    

        self.poc_tahov = 0
        self.poz_nuly = [3, 3] #pozicia prazdneho policka

        self.canvas.bind_all('<Up>', self.posun_hore)
        self.canvas.bind_all('<Down>', self.posun_dole)
        self.canvas.bind_all('<Right>', self.posun_vpravo)
        self.canvas.bind_all('<Left>', self.posun_vlavo)

        #self.x, self.y, self.dx, self.dy = 0, 0, 0, 0




        

        
    def vykresli_obrazky(self):
        self.canvas.delete('all')
        #self.canvas.create_image(0, 0, image=self.img_earth, anchor='nw')

        y = 0
        for riadok in self.pole:
            x = 0
            for obr in riadok:                
                self.canvas.create_image(x, y, image=obr, anchor='nw') #outline tu nefunguje!
                x += 100
            y += 100



    def pocet_tahov(self): #zmenit na pocet tahov!!
        self.canvas.create_text(300, 430, font='arial 12', text='pocet tahov:'+str(self.poc_tahov))
        #self.poc_tahov += 1
        
    def nula(self):
        return tuple(self.poz_nuly)

##    def vnutri(self, x, y): # DOROBIT ak budem robit posun/klik mysou


    def stvorec(self, x, y, cislo):
        self.canvas.create_rectangle(x, y, x+100, y+100, width=1, outline='black')
        self.canvas.create_text(x+50, y+50, font='arial 50 bold', fill='blue', text=cislo)

#CISLA:
##    def vykresli_cisla(self):
##        self.canvas.delete('all')
##        for i in range(len(self.pole)):
##            for j in range(len(self.pole[i])):
##                self.stvorec(j*100, i*100, self.pole[i][j])
##        


            
    def volne(self): #vracia policka, ktorymi sa da hybat a smer kde je nula vzhladom k nim
        self.dic = {}
        for i in range(4):
            
            if self.nula()[1] > 0: #policko vlavo od nuly
                policko = self.nula()[0], self.nula()[1]-1
                self.dic['p'] = policko

            if self.nula()[1] < 3: #policko vpravo od nuly
                policko = self.nula()[0], self.nula()[1]+1
                self.dic['l'] = policko

            if self.nula()[0] > 0: #policko hore od nuly
                policko = self.nula()[0]-1, self.nula()[1]
                self.dic['d'] = policko

            if self.nula()[0] < 3: #policko dole od nuly
                policko = self.nula()[0]+1, self.nula()[1]
                self.dic['h'] = policko
            
        return self.dic

#PRE CISLA:
##    def vymen_policka(self, smer):
##        policko = self.volne()[smer]
##        self.pole[self.nula()[0]][self.nula()[1]] = self.pole[policko[0]][policko[1]]
##        self.pole[policko[0]][policko[1]] = 0

    def vymen_obr(self, smer):
        policko = self.volne()[smer]
        self.pole[self.nula()[0]][self.nula()[1]] = self.pole[policko[0]][policko[1]]
        self.pole[policko[0]][policko[1]] = self.prazdny_stv 


    def posun_dole(self, event):
        if 'd' in self.volne():
            self.vymen_obr('d')            

            self.vykresli_obrazky()
            self.poz_nuly[0] -= 1
            self.volne()
            self.poc_tahov += 1


    def posun_hore(self, event):
        if 'h' in self.volne():
            self.vymen_obr('h') 

            self.vykresli_obrazky()
            self.poz_nuly[0] += 1
            self.volne()
            self.poc_tahov += 1

            
    def posun_vpravo(self, event):
        
        if 'p' in self.volne():
            self.vymen_obr('p') 

            self.vykresli_obrazky()
            self.poz_nuly[1] -= 1
            self.volne()
            self.poc_tahov += 1
            
    def posun_vlavo(self, event):
        if 'l' in self.volne():
            self.vymen_obr('l') 

            self.vykresli_obrazky()
            self.poz_nuly[1] += 1
            self.volne()
            self.poc_tahov += 1

#PRE CISLA:
####    def posun_hore(self, event):
####        if 'h' in self.volne():
####            self.vymen_policka('h')            
####
####            self.vykresli()
####            self.poz_nuly[0] -= 1
####            self.volne()
####
####
####    def posun_dole(self, event):
####        if 'd' in self.volne():
####            self.vymen_policka('d') 
####
####            self.vykresli()
####            self.poz_nuly[0] += 1
####            self.volne()
####
####            
####    def posun_vlavo(self, event):
####        
####        if 'l' in self.volne():
####            self.vymen_policka('l') 
####
####            self.vykresli()
####            self.poz_nuly[1] -= 1
####            self.volne()
####            
####    def posun_vpravo(self, event):
####        if 'p' in self.volne():
####            self.vymen_policka('p') 
####
####            self.vykresli()
####            self.poz_nuly[1] += 1
####            self.volne()

    def zisti_vyhru(self):
        ...


##class Stvorec:
##    def __init__(self, x, y, sirka=100, vyska=100):
##        
##    

class Program:
    def __init__(self):
        
        okno = tkinter.Tk() # vytv. graf. okno
        plocha = Plocha()

        
        plocha.vykresli_obrazky()

        napoveda = plocha.obrazok_original.resize((150, 150)) #napoveda 
        napoveda = ImageTk.PhotoImage(napoveda)
        plocha.canvas.create_image(500, 50, image=napoveda, anchor='nw')

        tkinter.mainloop()

        #PRE CISLA:
##        self.plocha.vykresli_cisla()
##        self.plocha.obrazky()

        
        

w = Program()



##def test2():
##    print(w.plocha.pole)
##    print(w.plocha.volne())
##
##
##test2()
