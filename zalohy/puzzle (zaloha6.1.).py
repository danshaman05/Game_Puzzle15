import tkinter
from tkinter import Menu
import random
from PIL import Image, ImageTk

class Plocha:

##zaujimave, ze objekt self.stvorce[3][3] je "Stvorec objekt" ale nema id, neda sa s nim nic robit.
    
################ __init__ ##############################
    def __init__(self, jpg_subor):
        self.canvas = tkinter.Canvas(width=650, height=100*4+50, bg='white')
        self.canvas.pack()

        Stvorec.canvas = self.canvas
        
        # NACITA OBR:
        self.obrazok_original = Image.open(jpg_subor)
        obrazok = self.obrazok_original.resize((400, 400)) #format Image


        #Prazdny stvorcek:
        self.prazdny_stv = ImageTk.PhotoImage(Image.new('RGB', (100,100), 'white'))

##        self.poz_nuly = -1,-1



        #SELF.POLE - self.obrazok rozdeleny po kuskoch:        
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


        #SELF.INDEXY - pole indexov pre self.pole:
        #self.indexy =[[(0,0),(0,1)...]]

        self.indexy =[]
        for i in range(4):
            riadok = []
            for j in range(4):
                riadok.append((i, j))
            self.indexy.append(riadok)


        #SELF.STVORCE - pole objektov triedy Stvorec:
        self.stvorce = []  


        #KOPIA self.indexy (kvoli overeniu vitazstva): #### NEBUDE FUNGOVAT OVERENIE, kvoli bielemu stvorceku !
        self.indexy_riesenie = [x[:] for x in self.indexy] #OK

        self.pole[3].append(0)
##        self.poz_nuly = [3, 3] #pozicia prazdneho policka
        self.poc_tahov = 0

        
        self.zamiesaj_pole()


##        print(self.pole)

        
        self.pridaj_stvorce()

        


# ######  PRE KLAVESY:
##        self.canvas.bind_all('<Up>', self.posun_hore)
##        self.canvas.bind_all('<Down>', self.posun_dole)
##        self.canvas.bind_all('<Right>', self.posun_vpravo)
##        self.canvas.bind_all('<Left>', self.posun_vlavo)

#netreba:
        #Na koniec self.pole prilepi prazdny stvorcek:
##        self.pole[3].append(self.prazdny_stv)


        self.canvas.bind('<Button-1>', self.mouse_click)
        

        #pocitadlo:
##        self.canvas.create_rectangle(270,420,340,430, fill='grey')
        self.pocitadlo = self.canvas.create_text(300, 430, font='arial 12', text='pocet tahov: '+str(self.poc_tahov))

        self.poz_nuly = list(self.nula())

        print('poz nuly:', self.poz_nuly, type(self.poz_nuly))
        print(self.indexy)

################ KONIEC __init__ ####################

    def zamiesaj_pole(self):

        #ZAMIESA SELF.INDEXY (3x): 
        #vramci riadkov:
        
        def miesaj_riadok(pole):
            for riadok in pole:
                riadok = random.shuffle(riadok)

        self.canvas.after(500) #NEFUNGUJE!!
        self.canvas.update()
        
        miesaj_riadok(self.indexy)
            
        #vramci stlpcov:
        self.indexy_pomocne = [x[:] for x in self.indexy]
        
        for i in range(len(self.indexy)):
            for j in range(len(self.indexy[i])):
                self.indexy[j][i] = self.indexy_pomocne[i][j]

        #NEFUNGUJE:
##        self.canvas.after(500) 
##        self.canvas.update()

        #3. zamiesanie - vramci riadku:
        miesaj_riadok(self.indexy)

##        print(self.indexy)


    def pridaj_stvorce(self):
        '''pridava zaradom stvorce kazdy podla mriezky... To, kt. stvorec sa prida, je urcene v self.indexy'''
        ...
        y = 0
        for i in range(4):
            x =0
            riadok = []
            for j in range(4):
                s = Stvorec(x,y, self.pole[self.indexy[i][j][0]][self.indexy[i][j][1]])
                riadok.append(s)

##                if (i, j) == (0,2):
##                    self.canvas.move(self.id, 100, 0)
##                    print('pohol som', self.id)

                x += 100
            y += 100
            self.stvorce.append(riadok)

##        print(self.stvorce[3][3])
##        Stvorec.move(self.stvorce[3][2], 100, 0)
        

##        print(self.pole[3][2])


    def pocet_tahov(self): #ZMENIT NA RETURN! a pridat label
        self.poc_tahov += 1
        self.canvas.itemconfig(self.pocitadlo, text='pocet tahov: '+str(self.poc_tahov))
        
        
    def nula(self):
        if self.poc_tahov > 0:
            return list(self.poz_nuly)
        else:
            for i in range(len(self.indexy)):
                for j in range(len(self.indexy[i])):
                    x, y = self.indexy[i][j]
                    if x == 3 and y == 3:
                        self.poz_nuly = list((i, j))
##        print(list(self.poz_nuly))
        return list(self.poz_nuly)


##    def vnutri(self, x, y): # DOROBIT ak budem robit posun/klik mysou



######## PRE CISLA: 
##    def stvorec(self, x, y, cislo):
##        self.canvas.create_rectangle(x, y, x+100, y+100, width=1, outline='black')
##        self.canvas.create_text(x+50, y+50, font='arial 50 bold', fill='blue', text=cislo)


            
    def volne(self): #vracia policka, ktorymi sa da hybat a smer kde je nula vzhladom k nim
        self.dic = {}
        for i in range(4):
            
            if self.nula()[1] > 0: #policko vlavo od nuly
                policko = self.nula()[0], self.nula()[1]-1
                self.dic[policko] = 100, 0

            if self.nula()[1] < 3: #policko vpravo od nuly
                policko = self.nula()[0], self.nula()[1]+1
                self.dic[policko] = -100, 0

            if self.nula()[0] > 0: #policko hore od nuly
                policko = self.nula()[0]-1, self.nula()[1]
                self.dic[policko] = 0, 100

            if self.nula()[0] < 3: #policko dole od nuly
                policko = self.nula()[0]+1, self.nula()[1]
                self.dic[policko] = 0, -100

        return self.dic

    def mouse_click(self, event): #stara vymen_obr
        dic = self.volne()
        if 0 <= event.x <= 400 and 0 <= event.y <= 400:
            j = event.x // 100 #stlpec
            i = event.y // 100 #riadok

            print(self.poz_nuly)
            if (i,j) in dic:
                volne_policko = i + int(dic[(i,j)][1] / 100), j + int(dic[(i,j)][0] / 100)
                Stvorec.move(self.stvorce[self.indexy[i][j][0]][self.indexy[i][j][1]], *dic[(i,j)])

                self.poz_nuly[0] -= int(dic[(i,j)][1] / 100)
                
                self.poz_nuly[1] -= int(dic[(i,j)][0] / 100)  
              
                self.indexy[volne_policko[0]][volne_policko[1]] = self.indexy[i][j][0], self.indexy[i][j][1] #volne_policko[1], volne_policko[0] ########

                self.indexy[i][j] = (3,3)  

                self.pocet_tahov()



#PRE CISLA: 
##    def posun_dole(self, event):
##        if 'd' in self.volne():
##            self.vymen_obr('d')            
##
##            self.poz_nuly[0] -= 1
##            self.volne()
##
##    def posun_hore(self, event):
##        if 'h' in self.volne():
##            self.vymen_obr('h') 
##
##            self.poz_nuly[0] += 1
##            self.volne()
##      
##    def posun_vpravo(self, event):
##        
##        if 'p' in self.volne():
##            self.vymen_obr('p') 
##
##            self.poz_nuly[1] -= 1
##            self.volne()
##            
##    def posun_vlavo(self, event):
##        if 'l' in self.volne():
##            self.vymen_obr('l') 
##
##            self.poz_nuly[1] += 1
##            self.volne()


    def zisti_vyhru(self):
        ...

##    def napoveda(self):




class Stvorec:
    def __init__(self, x, y, image_zdroj):
        self.x, self.y = x, y
        if image_zdroj != 0:
            self.id = self.canvas.create_image(x, y, image=image_zdroj, anchor='nw') #outline tu nefunguje!

    def move(self, x, y):
        cas = 20
        for i in range(cas):
            self.canvas.move(self.id, x/cas, y/cas)
            self.canvas.after(15)
            self.canvas.update()

##    def vnutri(self, x, y):
##        return abs(self.x-x) <= 100 and abs(self.y-y) <= 100
        
            

####################################################################################
class Program:
    def __init__(self):
        
        self.okno = tkinter.Tk() # vytv. graf. okno
        plocha = Plocha('obr/tesla.jpg')
        
        self.menu()

        # NAPOVEDA napravo:
        napoveda = plocha.obrazok_original.resize((150, 150)) #napoveda = maly obrazok vpravo
        napoveda = ImageTk.PhotoImage(napoveda)
        plocha.canvas.create_image(410, 10, image=napoveda, anchor='nw')

        print(plocha.volne())

##        s = Stvorec(0,0, plocha.pole[plocha.indexy[0][2][0]][plocha.indexy[0][2][1]])
##        Stvorec.move(s, 50, 100)


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

