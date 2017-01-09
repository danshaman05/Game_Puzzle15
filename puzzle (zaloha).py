import tkinter
from tkinter import Menu
import random
from PIL import Image, ImageTk
import json



class Plocha:

#Vitazna animacia - vsetky stvorce prebliknu a doplni sa posledny !
#pridat tabulku score - vitazov..
# chybna hlaska na konci hry - unbind - deletecommand() argument must be str, not method
#LOAD game musi zmenit aj pocet tahov!
#Matfyzak nezmizne
#po vyhre - zapisat do tabulky (cez label)  svoje meno .. a zapise sa skore
    
# itemconfig nesluzi na presun zmenu suradnic utvaru!




#PROBLEM:
# new game - po spusteni ide 
#po load_game hra nejde dobre

#Problem je asi v usporiadaj_stvorce - ak prida na index (3,3) v self.indexy, tak to preskoci -
#lenze malo by asi

#ak dam load_game tak sa objavia 2 policka (3,3) v self.indexy - niekedy je to vporiadku
#AK pouzijem LOAD_GAME 1x, tak je vsetko OK, ale ak pouzijem dalsi krat, nejde hra...


 
##zaujimave, ze objekt self.stvorce[3][3] je "Stvorec objekt" ale nema id, neda sa s nim nic robit.

   
################ __init__ ##############################
    def __init__(self, jpg_subor):
        self.canvas = tkinter.Canvas(width=600, height=100*4+50, bg='white')
        self.canvas.pack()

        Stvorec.canvas = self.canvas

        
        # NACITA OBR:
        self.obrazok_original = Image.open(jpg_subor)
        obrazok = self.obrazok_original.resize((400, 400)) #format Image


        #Prazdny stvorcek:
        self.prazdny_stv = ImageTk.PhotoImage(Image.new('RGB', (100,100), 'white'))


        #SELF.POLE - self.obrazok rozdeleny po kuskoch:        
        self.pole = []
        for i in range(0, 400, 100):
            riadok = []
            for j in range(0, 400, 100):

##                if (i, j) == (300, 300):
##                    break
                
                stvorcek = obrazok.crop((j, i, j+100, i+100))
                stvorcek.load() #kvoli lazy vyhodnocovaniu
                stvorcek = ImageTk.PhotoImage(stvorcek)
                riadok.append(stvorcek)
            self.pole.append(riadok)


#### PRINTUJE SELF.POLE:
        pocet= 0
        print('printujem self.pole:')
        for i in self.pole:
            print(i)
            pocet += len(i)
        print('pocet: ', pocet)


        

        #SELF.STVORCE - pole objektov triedy Stvorec:
        self.stvorce = []


        #SELF.INDEXY - pole indexov pre self.pole:
        #self.indexy =[[(0,0),(0,1)...]]
        self.indexy =[]
        for i in range(4):
            riadok = []
            for j in range(4):
                riadok.append([i,j])
            self.indexy.append(riadok)

              
        #INDEXY_riesenie (kvoli overeniu vitazstva): 
        self.indexy_riesenie = [x[:] for x in self.indexy] #OK

##        self.pole[3].append(0)

        
##        self.poz_nuly = [3, 3] #pozicia prazdneho policka
        
        self.poc_tahov = 0


        self.pridaj_stvorce()

        #Skryje posledny stvorec:
        Stvorec.hide(self.stvorce[-1][-1])


        self.new_game()
        

# ######  PRE KLAVESY:
##        self.canvas.bind_all('<Up>', self.posun_hore)
##        self.canvas.bind_all('<Down>', self.posun_dole)
##        self.canvas.bind_all('<Right>', self.posun_vpravo)
##        self.canvas.bind_all('<Left>', self.posun_vlavo)


        self.canvas.bind('<Button-1>', self.mouse_click)
        
        #Pocitadlo:
##        self.canvas.create_rectangle(270,420,340,430, fill='grey')
        

        self.poz_nuly = list(self.nula())

        #Nastavenie rychlosti posunu stvorcov
##        self.rychlo = False
##        Stvorec.rychlo = self.rychlo

        self.info_save_game = None


    def print_indexy(self):
        print()
        print('self.indexy: ')
        for i in self.indexy:
            print(i)

        

################ KONIEC __init__ ####################

    def new_game(self):
        self.newgame = True
        

        #Zmaze pocitadlo:
        self.poc_tahov = 0
        try:
            self.canvas.delete(self.pocitadlo)
        except AttributeError:
            pass

        #Vytvori pocitadlo:
        self.pocitadlo = self.canvas.create_text(300, 430, font='arial 12', text='pocet tahov: '+str(self.poc_tahov))
        
        self.load_game()
        

    def save_game(self):
##        filename = input('zadaj meno suboru na save:')
##        filename += '.txt'
        with open('rozohrata.txt', 'w') as file:
            json.dump(self.indexy, file)

        #textove info naspodku o ulozeni hry:
        self.info_save_game = self.canvas.create_text(110,410, text='Hra bola ulozena do rozohrata.txt')



    def load_game(self):
        if self.newgame == True: #ak sa zacina new game
            filename = 'new_game/game1.txt'
        else:
            filename = 'rozohrata.txt'
            self.indexy = []
        
        self.indexy = json.load(open(filename))
        print('printujem self.indexy: ', self.indexy)
        print('nahral som subor: ', filename)
        self.print_indexy()
##        print('self.indexy su typu: ', type(self.indexy))
        
        print('stvorce: ', self.stvorce)
        self.usporiadaj_stvorce()
        self.newgame = False

##        self.print_indexy()


##    def save_game(self):
##        with open('rozohrata.txt', 'w') as f:
##            for riadok in self.indexy:
##                for dvojica in riadok:
##                    print(dvojica, end=' ', file=f)
##                print(file=f)
##        self.info_save_game = self.canvas.create_text(110,410, text='Hra bola ulozena do rozohrata.txt')
##
##    def load_game(self):
##        if self.newgame == True: #ak sa zacina new game
##            filename = 'new_game/game1.txt'
##        else:
##            filename = 'rozohrata.txt'
##            self.indexy = []
##        with open(filename, 'r') as f:
##            for riadok in f:
##                r = []
##                print('idem to vypisat')
##                for dvojica in riadok.split():
####                    r.append(
##                    
##                    print(dvojica, end=' ')
##                print()

    def zisti_vyhru(self):
        '''vrati True ak je vyhra'''
        for i in range(len(self.indexy)):
            if self.indexy[i] != self.indexy_riesenie[i]:
                return False
        self.canvas.create_text(300,200, font='arial 40 bold',text='Si super Matfyzák!', fill='gold')
        self.canvas.unbind('<Button-1>', self.mouse_click)
        return True


    def pridaj_stvorce(self):
        '''pridava zaradom stvorce kazdy podla mriezky... To, kt. stvorec sa prida, je urcene v self.indexy'''
        ...
        y = 0
        for i in range(4):
            x =0
            riadok = []
            for j in range(4):
                s = Stvorec(x, y, self.pole[i][j])
                riadok.append(s)
                x += 100
            y += 100
            self.stvorce.append(riadok)

        


    def usporiadaj_stvorce(self):
        for i in range((4)):
            for j in range(4):
                
##                print('index:', self.indexy[i][j])
##                if 3 == self.indexy[i][j][0] and 3 == self.indexy[i][j][1]:
####                    print('3 3')
##                    continue
                x, y = self.indexy[i][j]
                self.stvorce[x][y].move_to(j*100, i*100)

        self.poz_nuly = list(self.nula())
                   


    def pocet_tahov(self): #ZMENIT NA RETURN! a pridat label
        self.poc_tahov += 1
        self.canvas.itemconfig(self.pocitadlo, text='pocet tahov: '+str(self.poc_tahov))
        
        
    def nula(self):
##        if self.poc_tahov > 0:
##            return list(self.poz_nuly)
##        else:
        for i in range(len(self.indexy)):
            for j in range(len(self.indexy[i])):
                x, y = self.indexy[i][j]
                if x == 3 and y == 3:
                    self.poz_nuly = list((i, j))
                    return list(self.poz_nuly)
        

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

        # pohni polickom, kt. je v self.stvorce na poz. 0,1.
        # DIC vratil, ze volne policko je na pozicii 1,0 v self.indexy
        #hodnota toho policka v self.indexy je (0,1)
        
        dic = self.volne()
        
        if 0 <= event.x <= 400 and 0 <= event.y <= 400:
            print()
            print()
            self.print_indexy()
            print()
            print('DIC:', self.volne())
            j = event.x // 100 #stlpec
            i = event.y // 100 #riadok
            
            
            if (i,j) in dic: # and self.indexy[i][j] != [3,3]:
                #print('rovnaju sa?', self.indexy[i][j] != [3,3])

                

                a = int(dic[(i,j)][1] / 100)
                b = int(dic[(i,j)][0] / 100)
                
                pozicia_nuly = i + a, j + b
##                print('pozicia_nuly:', pozicia_nuly)
##                print('poz_nuly: ', self.poz_nuly)

##                ax = self.poz_nuly[0]- int(dic[(i,j)][1] / 100) #vysledok je 1
##                bx = self.poz_nuly[1]-int(dic[(i,j)][0]/ 100) #vysl 0

##                print(ax == i)

                nula = self.indexy[i][j][0]
                jedna = self.indexy[i][j][1]
                Stvorec.move(self.stvorce[nula][jedna], *dic[(i,j)])

                self.poz_nuly[0] -= int(dic[(i,j)][1] / 100)
                self.poz_nuly[1] -= int(dic[(i,j)][0] / 100)  
              
                self.indexy[pozicia_nuly[0]][pozicia_nuly[1]] = [ self.indexy[i][j][0], self.indexy[i][j][1] ] #volne_policko[1], volne_policko[0] ########
                self.indexy[i][j] = [3,3]

                self.pocet_tahov()

                self.zisti_vyhru()

                self.canvas.delete(self.info_save_game)

                self.newgame == False
                


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



##    def napoveda(self):


###################################################### STVOREC #############
class Stvorec:
    def __init__(self, x, y, image_zdroj):
        self.x, self.y = x, y
        if image_zdroj != 0:
            self.id = self.canvas.create_image(x, y, image=image_zdroj, anchor='nw') #outline tu nefunguje!
##            canvas.create_text(x+50, y+50, text=)

    def move(self, x, y):
##        if self.rychlo == True:
##            self.cas = 1
##        else:
        self.cas = 18
        for i in range(self.cas):
            self.canvas.move(self.id, x/self.cas, y/self.cas)
            self.canvas.after(15)
            self.canvas.update()

    def move_to(self, x, y):
        self.canvas.coords(self.id, x, y)

    def hide(self): #skryje stvorcek
        self.canvas.itemconfig(self.id, state='hidden')
        
    def unhide(self):
        ...
        

##    def vnutri(self, x, y):
##        return abs(self.x-x) <= 100 and abs(self.y-y) <= 100
        
            

######################################################### PROGRAM ##############
class Program:
    def __init__(self):

        self.okno = tkinter.Tk() # vytv. graf. okno

        self.plocha = Plocha('obr/tesla.jpg')
        self.menu()

        # NAPOVEDA napravo:
        self.napoveda = self.plocha.obrazok_original.resize((150, 150)) #napoveda = maly obrazok vpravo
        self.napoveda = ImageTk.PhotoImage(self.napoveda)
        self.plocha.canvas.create_image(410, 10, image=self.napoveda, anchor='nw')

##        print(self.plocha.indexy)
        print()
        print('DIC:', self.plocha.volne())
        print()
 
        
        tkinter.mainloop()


    def menu(self):
        
        def donothing():
           filewin = tkinter.Toplevel(self.okno)
           button = tkinter.Button(filewin, text="Do nothing button")
           button.pack()
           
        menubar = Menu(self.okno)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New game", command=self.plocha.new_game)
        filemenu.add_command(label="Save game", command=self.plocha.save_game)
        filemenu.add_command(label="Load game", command=self.plocha.load_game)
##        filemenu.add_command(label="Save as...", command=donothing)
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



p = Program()
