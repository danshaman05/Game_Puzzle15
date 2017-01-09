import tkinter

##
##class Plocha:
##    def __ini

plocha = tkinter.Canvas(width='500', height='500')
plocha.pack()

class Object:
    def __init__(self, x, y, sirka=0, vyska=0):
        self.x, self.y
        w2 = sirka //2
        h2 = vyska //2

    def vnutr(self, x, y):
        return abs(self.x-x) <= self.w2 and abs(self.y-y) <= self.h2
    
        

class Stvorec:
    def __init__(self, x, y, sirka=50, vyska=50, farba=''):
        self.id = plocha.create_rectangle(x,y,x+sirka, y+sirka, fill='white')

        def mouse_click(self, x, y):
##        if self.id is not None:
        self.canvas.move(self.id, x-self.x, y-self.y)
        self.x, self.y = x, y

a = Stvorec(50,50)


class Plocha(tkinter.Canvas):
    
