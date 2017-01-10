SlidePuzzle - Puzzle 15
famous game!


#HOTOVE / NOVINKY::
#Na konci sa ukaze obrazok cely, message 'matfyzak' je na boku.
#Nacitavaju sa uz aj ine obrazky - striedaju sa nahodne.
## ak 2x kliknem na stvorcek, kt. sa da hybat, tak mi ho vysunie prec a prekryje iny stvorcek alebo vyjde mimo plochu - hotove
# chybna hlaska na konci hry - unbind - deletecommand() argument must be str, not method - hotove
#Matfyzak hlaska nezmizne - hotove
#LOAD game musi zmenit aj pocet tahov! - hotove


BUGY:
(none)

DOROBIT:
#Load game nech nahra aj obrazok konkretny!
#po vyhre - zapisat do tabulky (cez label)  svoje meno .. a zapise sa skore
# sipky - posun
#casomieru dorobit
#Vitazna animacia - vsetky stvorce prebliknu a doplni sa posledny !
#pridat tabulku score - vitazov..
#new game- nacita rozne obrazky
#BUG: po vyhre sa neda dat hned LOAD_game, treba dat najprv New_game
#dorobit HELP - o tvorcovi hry, atd..
    

Moje pozn.:
# itemconfig nesluzi na presun suradnic utvaru! (ale canvas.coords)
time.sleep() nie je dobre pouzit na kratke zastavenie programu
