
import tkinter
from tkinter import Menu
import random
from PIL import Image, ImageTk



# cele zmenit tak, aby obrazky boli ID .. a menit ich - pri vymene policok

class Plocha:

################ __init__ ##############################
    def __init__(self, jpg_subor):
        self.canvas = tkinter.Canvas(width=650, height=100*4+50, bg='white')
        self.canvas.pack()

        # NACITA OBR:
        self.obrazok_original = Image.open(jpg_subor)
        obrazok = self.obrazok_original.resize((400, 400)) #format Image

        

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



        #KOPIA POLA (kvoli overeniu vitazstva): #### NEBUDE FUNGOVAT OVERENIE, kvoli bielemu stvorceku !
        self.pole_riesenie = [x[:] for x in self.pole]
##        print(self.pole_riesenie)


        self.zamiesaj_pole()

        #Na koniec self.pole prilepi prazdny stvorcek:
        self.pole[3].append(self.prazdny_stv)
        


        self.poc_tahov = 0
        self.poz_nuly = [3, 3] #pozicia prazdneho policka

        self.canvas.bind_all('<Up>', self.posun_hore)
        self.canvas.bind_all('<Down>', self.posun_dole)
        self.canvas.bind_all('<Right>', self.posun_vpravo)
        self.canvas.bind_all('<Left>', self.posun_vlavo)

        self.vykresli_obrazky()

        #pocitadlo:
        self.canvas.create_rectangle(270,420,340,430, fill='grey')
        self.pocitadlo = self.canvas.create_text(300, 430, font='arial 12', text='pocet tahov: '+str(self.poc_tahov))

        #self.x, self.y, self.dx, self.dy = 0, 0, 0, 0

##        self.napoveda() #neviem preco nejde

################ KONIEC __init__ ####################

    def zamiesaj_pole(self):

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
        


    def vykresli_obrazky(self):
        #self.canvas.delete('all')

        y = 0
        for riadok in self.pole:
            x = 0
            for obr in riadok:                
                self.canvas.create_image(x, y, image=obr, anchor='nw') #outline tu nefunguje!
                x += 100
            y += 100



##    def pocet_tahov(self): 
##        return self.poc_tahov
##        

    def pocet_tahov(self):
        self.poc_tahov += 1
        self.canvas.itemconfig(self.pocitadlo, text='pocet tahov: '+str(self.poc_tahov))
        
        
    def nula(self):
        return tuple(self.poz_nuly)

##    def vnutri(self, x, y): # DOROBIT ak budem robit posun/klik mysou


    def stvorec(self, x, y, cislo):
        self.canvas.create_rectangle(x, y, x+100, y+100, width=1, outline='black')
        self.canvas.create_text(x+50, y+50, font='arial 50 bold', fill='blue', text=cislo)


            
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

    def vymen_obr(self, smer):
        policko = self.volne()[smer]
        self.pole[self.nula()[0]][self.nula()[1]] = self.pole[policko[0]][policko[1]]
        self.pole[policko[0]][policko[1]] = self.prazdny_stv

        self.pocet_tahov()


    def posun_dole(self, event):
        if 'd' in self.volne():
            self.vymen_obr('d')            

            self.vykresli_obrazky()
            self.poz_nuly[0] -= 1
            self.volne()
            


    def posun_hore(self, event):
        if 'h' in self.volne():
            self.vymen_obr('h') 

            self.vykresli_obrazky()
            self.poz_nuly[0] += 1
            self.volne()

            
    def posun_vpravo(self, event):
        
        if 'p' in self.volne():
            self.vymen_obr('p') 

            self.vykresli_obrazky()
            self.poz_nuly[1] -= 1
            self.volne()
            
    def posun_vlavo(self, event):
        if 'l' in self.volne():
            self.vymen_obr('l') 

            self.vykresli_obrazky()
            self.poz_nuly[1] += 1
            self.volne()


    def zisti_vyhru(self):
        ...

##    def napoveda(self):



class Program:
    def __init__(self):
        
        self.okno = tkinter.Tk() # vytv. graf. okno
        plocha = Plocha('obr/earth.jpg')
        
        self.menu()

        # NAPOVEDA napravo:
        napoveda = plocha.obrazok_original.resize((150, 150)) #napoveda = maly obrazok vpravo
        napoveda = ImageTk.PhotoImage(napoveda)
        plocha.canvas.create_image(410, 10, image=napoveda, anchor='nw')


        tkinter.mainloop()



    def menu(self):
        
        def donothing():
           filewin = tkinter.Toplevel(self.okno)
           button = tkinter.Button(filewin, text="Do nothing button")
           button.pack()
           
        menubar = Menu(self.okno)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=donothing)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_command(label="Save as...", command=donothing)
        filemenu.add_command(label="Close", command=donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.okno.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=donothing)

        editmenu.add_separator()

##        editmenu.add_command(label="Cut", command=donothing)
##        editmenu.add_command(label="Copy", command=donothing)
##        editmenu.add_command(label="Paste", command=donothing)
##        editmenu.add_command(label="Delete", command=donothing)
##        editmenu.add_command(label="Select All", command=donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.okno.config(menu=menubar)
##        self.okno.mainloop()




w = Program()

