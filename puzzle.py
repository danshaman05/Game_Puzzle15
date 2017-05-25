#v2

import tkinter
import sqlite3
from tkinter import Menu
from random import randrange as rr
from PIL import Image, ImageTk
import json
import time

##BUGY:
#Load game nech nahra aj obrazok konkretny!

##DOROBIT:

#DB:
#- bude obsahovat obrazky?
#- bude obsahovat zaznamy o najlepsich hracoch
#- chcel som urobit ju ako triedu

#Tahanie (miesto klikania)
#
#Animacia - viaz obrazkov v poli
# - mohla by byt na zaciatku, ako zapnes hru, tak ukazuje tam ako sa sklada puzzle.


#LOGO GameSlide Puzzle! alebo ram naokolo!

#po vyhre -vyskoci okno - tam sa zapise meno a vek
# - potom sa to zapise do tabulky
#zapisat do tabulky (cez label)  svoje meno .. a zapise sa skore


# sipky - posun
#casomieru dorobit
#Vitazna animacia - vsetky stvorce prebliknu a doplni sa posledny !
#pridat tabulku score - vitazov..
#new game- nacita rozne obrazky
#BUG: po vyhre sa neda dat hned LOAD_game, treba dat najprv New_game
#dorobit HELP - o tvorcovi hry, atd..
    

#HOTOVE:
#unhide (show)
#Matfyzak nezmizne
#LOAD game musi zmenit aj pocet tahov!
## ak 2x kliknem na stvorcek, kt. sa da hybat, tak mi ho vysunie prec a prekryje iny stvorcek alebo vyjde mimo plochu
# chybna hlaska na konci hry - unbind - deletecommand() argument must be str, not method


class WinnersWindow: #okno vybehne ak hrac vyhral hru - ziada od neho meno
    def __init__(self, parent, moves): #moves = pocet tahov
##        self.root = parent
##        self.cursor = cursor
        self.moves = moves
        self.top = tkinter.Toplevel(parent)
##        self.canvas = tkinter.Canvas
##        self.canvas.pack()
        
        player_input_label = tkinter.Label(self.top, text='Zadaj meno:').grid(row=1, column=1)
        self.player_name_e = tkinter.Entry(self.top)
        self.player_name_e.grid(row=2, column=1)
        player_input_submit = tkinter.Button(self.top, text="OK", command=self.zrus).grid(row=3, column=1)
        

##        tkinter.Label(self.top, text='Table of winners').grid(row=0, column=1, columnspan=4)
        

##    def print_winners(self):
##        l = tkinter.Listbox(self.top)#
##        l.insert(1, 'AHOJ')
##        print(l[1]).grid(row=4, column=0)
##        l.place(x=450, y=500)
##        l.pack()
        
      
    def zrus(self):
        name = self.player_name_e.get() #meno hraca kt. prave vyhral
        print(repr(name))

        
        conn = sqlite3.connect('db/database.db')
        conn.execute("INSERT INTO Winners (NAME, MOVES) VALUES (?, ?)", (name, self.moves))
        conn.commit()
        print ("Records created successfully. Zatvaram okno")
         
        self.top.destroy()
        


class Plocha:

################ __init__ ##############################

    def __init__(self, parrent):   #parrent je okno, v ktorom sidli Plocha
        self.root = parrent    ### TEST, funguje
        self.canvas = tkinter.Canvas(width=600, height=100*4+50, bg='white')
        self.canvas.pack()
        Stvorec.canvas = Message.canvas = self.canvas

##        ##### Tlacidlo zadaj meno:
##        zadaj_meno_popis = tkinter.Label(self.root, text='Zadaj meno:') ##### TEST
##        zadaj_meno_popis.place(x=420, y=300)
##
##        zadaj_meno = tkinter.Entry(self.root)
##        zadaj_meno.place(x=420, y=320)
##
##        zadaj_meno = tkinter.Button(self.root, text="OK")
##        zadaj_meno.place(x=480, y=340)
##        #####
        

        self.info_save_game = Message(110,420, 'Hra bola ulozena do rozohrata.txt', weight='normal')
        self.info_load_game = Message(130,420, 'Hra bola nahrana zo suboru rozohrata.txt', weight='normal')
        self.matfyzak = Message(500,200, 'Si super\n Matfyzák!', 'gold', 20) #vitazna sprava
        
        self.vyhral = False
        
        self.new_game()
        self.poz_nuly = list(self.nula())

        
        
        ####TEST:
        
##        self.root = Program().root
##        w = WinnersWindow(self.) #### TEST

        

        ####DB:
        self.database_connect() #metoda sa napoji na /vytvori/ databazu a nacita udaje. Vytvori tiez 2 atributy self.connection a self.cursor

        #tabulka vitazov:
        sql = '''CREATE TABLE IF NOT EXISTS Winners
          (ID             INTEGER PRIMARY KEY,
           NAME           TEXT    NOT NULL,
           TIME           INT,
           MOVES          INT     NOT NULL);'''
        self.cursor.execute(sql) #spusti sql dopyt

        self.cursor.execute("INSERT INTO Winners (ID, NAME, TIME, MOVES) VALUES (1, 'danko', 30, 10)")
        
        self.connection.close()
##        self.conn.commit()
        
        ####

##        self.print_winners() #### TEST - POTOM VYMAZAT!! ######################################################

        

# ######  PRE KLAVESY:
##        self.canvas.bind_all('<Up>', self.posun_hore)
##        self.canvas.bind_all('<Down>', self.posun_dole)
##        self.canvas.bind_all('<Right>', self.posun_vpravo)
##        self.canvas.bind_all('<Left>', self.posun_vlavo)


        #Nastavenie rychlosti posunu stvorcov - DOROBIT mozno
##        self.rychlo = False
##        Stvorec.rychlo = self.rychlo

# VLASTNY TEST:
    def print_indexy(self):
        print()
        print('self.indexy: ')
        for i in self.indexy:
            print(i)      

################ KONIEC __init__ ####################



    def database_connect(self): #vytvori databazu alebo sa pripoji k existujucej
        self.connection = sqlite3.connect('db/database.db')
        self.cursor = self.connection.cursor()
        




    def input_name(self): #pole na zadanie mena po vyhre
        ##### Tlacidlo zadaj meno:
        zadaj_meno_popis = tkinter.Label(self.root, text='Tabulka vi:') ##### TEST
        zadaj_meno_popis.place(x=420, y=300)

        zadaj_meno = tkinter.Entry(self.root)
        zadaj_meno.place(x=420, y=320)

        zadaj_meno = tkinter.Button(self.root, text="OK")
        zadaj_meno.place(x=480, y=340)
        #####



    def new_game(self):
        self.newgame = True
         
        obrazky = ['earth.jpg', 'bees.jpg', 'tesla.jpg']
        jpg_subor = 'obr/' + str(obrazky[rr(3)])


        # NACITA OBR:
        self.obrazok_original = Image.open(jpg_subor)
        obrazok = self.obrazok_original.resize((400, 400)) #format Image

        #MINIATURA (obrazok vpravo):
        self.miniatura_img = self.obrazok_original.resize((120, 120)) #miniatura = maly obrazok vpravo
        prazdny = Image.new('RGB', (30, 30), 'white')
        self.miniatura_img.paste(prazdny, (90,90))
        self.miniatura_img = ImageTk.PhotoImage(self.miniatura_img)
        self.canvas.create_image(430, 10, image=self.miniatura_img, anchor='nw')


        #SELF.POLE - self.obrazok rozdeleny po kuskoch:        
        self.pole = []
        for i in range(0, 400, 100):
            riadok = []
            for j in range(0, 400, 100):
                stvorcek = obrazok.crop((j, i, j+100, i+100))
                stvorcek.load() #kvoli lazy vyhodnocovaniu
                stvorcek = ImageTk.PhotoImage(stvorcek)
                riadok.append(stvorcek)
            self.pole.append(riadok)


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
    
        #INDEXY_riesenie (kopia self.indexy - kvoli overeniu vitazstva): 
        self.indexy_riesenie = [x[:] for x in self.indexy]
        
        self.poc_tahov = 0
        self.pridaj_stvorce()
        
        #Zmaze pocitadlo:
        self.poc_tahov = 0
        try:
            self.canvas.delete(self.pocitadlo)
        except AttributeError:
            pass

        #Vytvori pocitadlo:
##        a = tkinter.Label(self.canvas, 'AHOJTEEEE') #### TEST
        self.pocitadlo = self.canvas.create_text(300, 430, font='arial 12', text='pocet tahov: '+str(self.poc_tahov))
        
        self.load_game()
        

    def save_game(self):
        with open('rozohrata.txt', 'w') as file:
            json.dump(self.indexy, file)

        #textove info naspodku o ulozeni hry:
        self.info_save_game.show()


    def load_game(self):
        self.canvas.bind('<Button-1>', self.mouse_click)
##        self.mozes_tah = True
        levels = 3 #pocet pripravenych levelov hry
        if self.newgame == True: #ak sa zacina new game
            filename = 'new_game/game{}.txt'.format(rr(1,levels+1)) #nahra nahodny subor z 5tich
        else:
            filename = 'rozohrata.txt'
            self.indexy = []
        
        self.indexy = json.load(open(filename))
        print('nahral som subor: ', filename)
        
        self.usporiadaj_stvorce()
        if self.newgame == False:
            self.info_load_game.show()
        self.matfyzak.hide()
        self.newgame = False
        Stvorec.hide(self.stvorce[-1][-1])
        
        

    def zisti_vyhru(self):
        '''vrati True ak je vyhra'''
        for i in range(len(self.indexy)):
            if self.indexy[i] != self.indexy_riesenie[i]:
                return False
        self.stvorce[-1][-1].show()

        
        self.canvas.unbind('<Button-1>')
        self.matfyzak.show()

        w = WinnersWindow(self.root, self.poc_tahov) #zobrazi okno
        self.root.wait_window(w.top) #caka kym sa zavrie okno
        

        self.print_winners() # vypise vitazov



    def print_winners(self):

        self.database_connect()
        cursor = self.cursor
        
        sql = "SELECT * FROM Winners"
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        self.connection.close()

##        self.input_name()


##        return True
     

    def pridaj_stvorce(self):
        '''pridava zaradom stvorce kazdy podla mriezky... To, kt. stvorec sa prida, je urcene v self.indexy'''
        y = 0
        for i in range(4):
            x =0
            riadok = []
            for j in range(4):
                s = Stvorec(x+10, y+10, self.pole[i][j])
                riadok.append(s)
                x += 100
            y += 100
            self.stvorce.append(riadok)


    def usporiadaj_stvorce(self):
        #Skryje posledny stvorec:
        Stvorec.hide(self.stvorce[-1][-1])
        
        for i in range((4)):
            for j in range(4):
                x, y = self.indexy[i][j]
                self.stvorce[x][y].move_to(j*100+10, i*100+10)
                self.canvas.after(70)
                self.canvas.update()

        self.poz_nuly = list(self.nula())
        
    def pocet_tahov(self): #zmenit na return a pridat label
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
        dic = {}
        for i in range(4):
            
            if self.nula()[1] > 0: #policko vlavo od nuly
                policko = self.nula()[0], self.nula()[1]-1
                dic[policko] = 100, 0

            if self.nula()[1] < 3: #policko vpravo od nuly
                policko = self.nula()[0], self.nula()[1]+1
                dic[policko] = -100, 0

            if self.nula()[0] > 0: #policko hore od nuly
                policko = self.nula()[0]-1, self.nula()[1]
                dic[policko] = 0, 100

            if self.nula()[0] < 3: #policko dole od nuly
                policko = self.nula()[0]+1, self.nula()[1]
                dic[policko] = 0, -100

        return dic

    def mouse_click(self, event):       
        dic = self.volne()
        if 0 <= event.x <= 400 and 0 <= event.y <= 400 and self.mozes_tah == True:

            print('volne policka a smer kde sa daju hybat:')
            print(self.volne())
            j = event.x // 100 #stlpec
            i = event.y // 100 #riadok
            
            
            if (i,j) in dic:
                a = int(dic[(i,j)][1] / 100)
                b = int(dic[(i,j)][0] / 100)
                
                pozicia_nuly = i + a, j + b

                kliknute1 = self.indexy[i][j][0] #indexy kliknuteho policka
                kliknute2 = self.indexy[i][j][1]

                nula1 = self.indexy[pozicia_nuly[0]][pozicia_nuly[1]][0] #indexy nuly
                nula2 = self.indexy[pozicia_nuly[0]][pozicia_nuly[1]][1]

                Stvorec.move(self.stvorce[kliknute1][kliknute2], *dic[(i,j)])
                Stvorec.move(self.stvorce[nula1][nula2], -(dic[(i,j)][0]), -(dic[(i,j)][1]))

                self.poz_nuly[0] -= int(dic[(i,j)][1] / 100)
                self.poz_nuly[1] -= int(dic[(i,j)][0] / 100)  
              
                self.indexy[pozicia_nuly[0]][pozicia_nuly[1]] = [ self.indexy[i][j][0], self.indexy[i][j][1] ] #volne_policko[1], volne_policko[0] ########
                self.indexy[i][j] = [3,3]
                
                self.pocet_tahov()
                self.vyhral = self.zisti_vyhru()
                self.info_save_game.hide()
                self.info_load_game.hide()

                self.newgame == False


#PRE Klavesy: - dorobit
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

    def napoveda(self):
        ...



##    def create_table(self, name):
##    def database_insert
        


###################################################### STVOREC #############
class Stvorec:
    def __init__(self, x, y, image_zdroj):
        self.x, self.y = x, y
        if image_zdroj != 0:
            self.id = self.canvas.create_image(x, y, image=image_zdroj, anchor='nw') #outline tu nefunguje!
        self.mozes_tah = True
        Plocha.mozes_tah = self.mozes_tah

    def move(self, x, y):
        Plocha.mozes_tah = False
##        if self.rychlo == True:
##            self.cas = 1
##        else:
        self.cas = 20 #kolko posunuti vykona
        for i in range(self.cas):
            self.canvas.move(self.id, x/self.cas, y/self.cas)
            self.canvas.after(10)
            self.canvas.update()
        Plocha.mozes_tah = True
        
    def move_to(self, x, y):
        self.canvas.coords(self.id, x, y)

    def hide(self): #skryje stvorcek
        self.canvas.itemconfig(self.id, state='hidden')
        
    def show(self): 
        self.canvas.itemconfig(self.id, state='')     


class Message:
    ''' message moze byt zapnuta, alebo vypnuta - show/hidden '''
    
    def __init__(self, x, y, text, color='black', size=10, weight='normal'): #weight = bold alebo normal
        self.id = self.canvas.create_text(x, y, text=text, fill=color, font='arial {} {}'.format(size, weight))
        self.hide()

    def show(self):
        self.canvas.itemconfig(self.id, state='')

    def hide(self):
        self.canvas.itemconfig(self.id, state='hidden')

    def __setitem__(self): #vyuzijem pri nastaveni suboru kde sa uklada / zkade sa nahrava
        ...

   

######################################################### PROGRAM ##############
class Program:
    def __init__(self):
        self.root = tkinter.Tk() # vytv. graf. okno # root je teraz okno (win u Blaha)
        self.plocha = Plocha(self.root)

        #toto sa overi len raz:
##        if self.plocha.zisti_vyhru():
##            print('vyhral')
##        else:
##            print('nevyhral')
        
        self.menu()      
        tkinter.mainloop()

    def newgame(self):
        ...

    def menu(self):   
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New game", command=self.plocha.new_game)
        filemenu.add_command(label="Save game", command=self.plocha.save_game)
        filemenu.add_command(label="Load game", command=self.plocha.load_game)
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_separator()
        self.root.config(menu=menubar)


p = Program()

