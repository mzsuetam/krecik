from tkinter import *
import os
import time
from PIL import ImageTk, Image
from enum import Enum
import threading
import sys
from antlr4 import *
from KrecikLexer import KrecikLexer
from KrecikParser import KrecikParser
from KrecikVisitor import KrecikVisitor
from MyVisitor import MyVisitor


BG_C = "#ffffff"
TEXT_C = "white"

WT = 0.5 # wait time [ms]

# ---------------------------------- clases ---------------------------------- #

class Rot(Enum):
    W = 0,
    N = 1,
    E = 2,
    S = 3

class Krecik:
    def __init__(self, _field):
        self.field : Label = _field
        self.rot = Rot.S
        self.field.config(image=k_pi_S)
        
    def moveN(self, n = 1):
        if n < 1:
            return
        for i in range(n):
            info = self.field.grid_info()
            dx, dy = 0, -1
            try:
                self.field.grid(row=info["row"]+dy, column=info["column"]+dx, sticky=W)
            except:
                pass
            time.sleep(0.5)
            root.update()
        
    def moveS(self, n = 1):
        if n < 1:
            return
        for i in range(n):
            info = self.field.grid_info()
            dx, dy = 0, 1
            try:
                self.field.grid(row=info["row"]+dy, column=info["column"]+dx, sticky=W)
            except:
                pass
            time.sleep(0.5)
            root.update()

    def moveE(self, n = 1):
        if n < 1:
            return
        for i in range(n):
            info = self.field.grid_info()
            dx, dy = 1, 0
            try:
                self.field.grid(row=info["row"]+dy, column=info["column"]+dx, sticky=W)
            except:
                pass
            time.sleep(0.5)
            root.update()
        

    def moveW(self, n = 1):
        if n < 1:
            return
        for i in range(n):
            info = self.field.grid_info()
            dx, dy = -1, 0
            try:
                self.field.grid(row=info["row"]+dy, column=info["column"]+dx, sticky=W)
            except:
                pass
            time.sleep(0.5)
            root.update()

    def moveForward(self, n=1):
        board.setCommandLabelText(f"Move forward ({n})")
        if ( self.rot == Rot.W ): 
            self.moveW(n)
        elif ( self.rot == Rot.N ): 
            self.moveN(n)
        elif ( self.rot == Rot.E ): 
            self.moveE(n)
        elif ( self.rot == Rot.S ): 
            self.moveS(n)

    def moveBackward(self, n=1):
        board.setCommandLabelText(f"Move backward ({n})")
        if ( self.rot == Rot.W ): 
            self.moveE(n)
        elif ( self.rot == Rot.N ): 
            self.moveS(n)
        elif ( self.rot == Rot.E ): 
            self.moveW(n)
        elif ( self.rot == Rot.S ): 
            self.moveN(n)

    def moveLeft(self, n=1):
        board.setCommandLabelText(f"Move left ({n})")
        if ( self.rot == Rot.W ): 
            self.moveS(n)
        elif ( self.rot == Rot.N ): 
            self.moveW(n)
        elif ( self.rot == Rot.E ): 
            self.moveN(n)
        elif ( self.rot == Rot.S ): 
            self.moveE(n)

    def moveRight(self, n=1):
        board.setCommandLabelText(f"Move right ({n})")
        if ( self.rot == Rot.W ): 
            self.moveN(n)
        elif ( self.rot == Rot.N ): 
            self.moveE(n)
        elif ( self.rot == Rot.E ): 
            self.moveS(n)
        elif ( self.rot == Rot.S ): 
            self.moveW(n)

    def rotateLeft(self):
        board.setCommandLabelText(f"Rotate left")
        if ( self.rot == Rot.W ): 
            self.rot = Rot.S
            self.field.config(image=k_pi_S)
        elif ( self.rot == Rot.N ): 
            self.rot = Rot.W
            self.field.config(image=k_pi_W)
        elif ( self.rot == Rot.E ): 
            self.rot = Rot.N
            self.field.config(image=k_pi_N)
        elif ( self.rot == Rot.S ): 
            self.rot = Rot.E
            self.field.config(image=k_pi_E)
        time.sleep(0.5)
        root.update()

    def rotateRight(self):
        board.setCommandLabelText(f"Rotate right")
        if ( self.rot == Rot.W ): 
            self.rot = Rot.N
            self.field.config(image=k_pi_N)
        elif ( self.rot == Rot.N ): 
            self.rot = Rot.E
            self.field.config(image=k_pi_E)
        elif ( self.rot == Rot.E ): 
            self.rot = Rot.S
            self.field.config(image=k_pi_S)
        elif ( self.rot == Rot.S ): 
            self.rot = Rot.W
            self.field.config(image=k_pi_W)
        time.sleep(0.5)
        root.update()
            
class Board:
    def __init__(self, _w, _h):
        self.w = _w
        self.h = _h

        mi = 100 # min
        mx = 1000 # max
        n = max(_w,_h)
        self.field_size = mi if n*mi < 1000 else 1000//n # px
        self.fields = [[None] * _h] * _w

        self.krecik = None

        self.command_label = None
    
    def setField(self, _i, _j, _field):
        self.fields[_i][_j] = _field

    def getField(self, _i,_j)  :
        return self.fields[_i][_j]
    
    def addKrecik(self, _krecik : Label):
        if self.krecik is None:
            self.krecik = Krecik(_krecik)

    def getKrecik(self):
        return self.krecik
    
    def addCommandLabel(self, _label: Label):
        self.command_label = _label
    
    def setCommandLabelText(self, _cmd):
        k = self.krecik
        info = k.field.grid_info()
        new_txt = f"At: ({info['row']},{info['column']}), Facing: {k.rot.name}, Doing: {_cmd}" 
        self.command_label.config(text = new_txt)
    
# ---------------------------------------------------------------------------- #
#                                      app                                     #
# ---------------------------------------------------------------------------- #

# ---------------------------------- window ---------------------------------- #

root = Tk()
root.title("Krecik")
# root.geometry("1200x800")
root.resizable(width=False, height=False)
# root.configure(background=BG_C)
board = Board(15,10)

# ---------------------------------- assets ---------------------------------- #

dirt_pi = ImageTk.PhotoImage(
    Image.open(os.path.join("assets", "dirt.png"))
    .resize((board.field_size, board.field_size), Image.ANTIALIAS))

k_pi_W = ImageTk.PhotoImage(
    Image.open(os.path.join("assets", "krecik_W.png"))
    .resize((board.field_size, board.field_size), Image.ANTIALIAS))

k_pi_N = ImageTk.PhotoImage(
    Image.open(os.path.join("assets", "krecik_N.png"))
    .resize((board.field_size, board.field_size), Image.ANTIALIAS))

k_pi_E = ImageTk.PhotoImage(
    Image.open(os.path.join("assets", "krecik_E.png"))
    .resize((board.field_size, board.field_size), Image.ANTIALIAS))

k_pi_S = ImageTk.PhotoImage(
    Image.open(os.path.join("assets", "krecik_S.png"))
    .resize((board.field_size, board.field_size), Image.ANTIALIAS))

# ------------------------------ forming board ------------------------------ #

for i in range(board.w):
    for j in range(board.h):
        l = Label(root, image=dirt_pi, bd=0)
        l.grid(row=j, column=i, sticky=W)
        board.setField(i,j,l)

_k = Label(root, image="", bd=0, bg='black')
_k.grid(row=0, column=0, sticky=W)
board.addKrecik(_k)
# # l4.grid_forget() # usuwanie

_l = Label(root, text="Starting...", font="none 12 bold")
_l.grid(row=board.h+1, column=0, columnspan=board.w, sticky=W)
board.addCommandLabel(_l)

# ---------------------------------------------------------------------------- #
#                                     start                                    #
# ---------------------------------------------------------------------------- #

def worker():
    # f = [ board.getKrecik().rotateLeft ]
    # for foo in f:
    #     foo()
    # time.sleep(2)
    # board.getKrecik().moveForward(4)
    board.getKrecik().rotateRight()

    data = None  # InputStream(input(">>> "))
    with open("inputs/simple.krecik", "r") as file:
         data = InputStream(file.read())

    # lexer
    lexer = KrecikLexer(data)
    stream = CommonTokenStream(lexer)
    # parser
    parser = KrecikParser(stream)
    tree = parser.primary_expression()
    # evaluator
    visitor = MyVisitor(board)
    output = visitor.visit(tree)
    # print(output)

    
t = threading.Thread(target=worker, args=[])
t.start()

# root.after(500, start)
root.mainloop()