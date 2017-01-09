import tkinter
from random import randrange as rr

class Zaklad:
    canvas = None
    sirka = 0
    vyska = 0
    def __init__(self, x, y, dx=0, dy=0, sirka=0, vyska=0):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.w2, self.h2 = sirka//2, vyska//2
        self.id = None

    def vnutri(self, x, y):
        return abs(self.x-x) <= self.w2 and abs(self.y-y) <= self.h2

    def mouse_move(self, x, y):
        if self.id is not None:
            self.canvas.move(self.id, x-self.x, y-self.y)
        self.x, self.y = x, y

    def mouse_down(self):
        pass

    def mouse_up(self):
        pass

    def timer(self):
        if self.dx!=0 or self.dy!=0:
            if self.x+self.dx < self.w2: self.dx = abs(self.dx)
            if self.y+self.dy < self.h2: self.dy = abs(self.dy)
            if self.x+self.dx > self.sirka - self.w2: self.dx = -abs(self.dx)
            if self.y+self.dy > self.vyska - self.h2: self.dy = -abs(self.dy)
            self.x += self.dx
            self.y += self.dy
            if self.id is not None:
                self.canvas.move(self.id, self.dx, self.dy)

#-----------------------------------------------------------------------

class Ramik(Zaklad):
    def __init__(self, x, y, dx=0, dy=0, sirka=30, vyska=30, farba=''):
        super().__init__(x, y, dx, dy, sirka, vyska)
        if farba == 'random':
            farba = '#{:06x}'.format(rr(256**3))
        self.id = self.canvas.create_rectangle(
            x-self.w2, y-self.h2, x+self.w2, y+self.h2, fill=farba)

    def mouse_down(self):
        self.canvas.itemconfig(self.id, width=3, outline='red')

    def mouse_up(self):
        self.canvas.itemconfig(self.id, width=1, outline='black')


#-----------------------------------------------------------------------

class Obrazok(Zaklad):
    def __init__(self, obr, x, y, dx=0, dy=0):
        if not isinstance(obr, list):
            obr = [obr]
        self.pole = obr
        self.faza = 0
        super().__init__(x, y, dx, dy, obr[0].width(), obr[0].height())
        self.id = self.canvas.create_image(x, y, image=obr[0])

    def timer(self):
        if len(self.pole) > 1:
            self.canvas.itemconfig(self.id, image=self.pole[self.faza])
            self.faza = (self.faza + 1) % len(self.pole)
        super().timer()

#################################################

class Plocha(tkinter.Canvas):
    def __init__(self, *param, **pparam):
        super().__init__(*param, **pparam)
        self.pack()
        Zaklad.canvas = self
        Zaklad.sirka = int(self['width'])
        Zaklad.vyska = int(self['height'])
        self.bind('<Button-1>', self.mouse_down)
        self.bind('<B1-Motion>', self.mouse_move)
        self.bind('<ButtonRelease-1>', self.mouse_up)
        self.pole = []
        self.tahany = None
        self.timer()

    def timer(self):
        for obj in self.pole:
            obj.timer()
        self.after(100, self.timer)

    def mouse_down(self, event):
        for obj in reversed(self.pole):
            if obj.vnutri(event.x, event.y):
                self.tahany = obj
                self.dx, self.dy = event.x - obj.x, event.y - obj.y
                obj.mouse_down()
                return
        self.tahany = None

    def mouse_move(self, event):
        if self.tahany is not None:
            self.tahany.mouse_move(event.x-self.dx, event.y-self.dy)

    def mouse_up(self, event):
        if self.tahany is not None:
            self.tahany.mouse_up()
            self.tahany = None

    def pridaj(self, obj):
        self.pole.append(obj)

p = Plocha(width=800, height=500, bg='green')
for i in range(10):
    p.pridaj(Ramik(rr(0,800), rr(0, 500), rr(-2, 2), rr(-2, 2), 60, 40, farba='random'))
##zemegula = [tkinter.PhotoImage(file='a3/z{}.png'.format(i)) for i in range(21)]
##for i in range(5):
##    p.pridaj(Obrazok(zemegula, rr(0,800), rr(0, 500), rr(-2, 2), rr(-2, 2)))
