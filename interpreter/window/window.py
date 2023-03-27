from tkinter import *
import os
import time
from PIL import ImageTk, Image
from enum import Enum
import sys

class Rot(Enum):
    W = 0,
    N = 1,
    E = 2,
    S = 3

class KrecikWindow():

    __field_size = 0

    __WT = 0.5 # wait time [s]

    __root = None

    __cmd_label = None

    __krecik_field = None
    __krecik_rot = Rot.S

    __images = dict()

    # ---------------------------------------------------------------------------- #
    #                                     init                                     #
    # ---------------------------------------------------------------------------- #

    def __init__(self, w, h, waiting_time = 0.5):

        # ----------------------------------- basic ---------------------------------- #

        mi = 100 # min
        mx = 1000 # max
        n = max(w,h)
        self.__field_size = mi if n*mi < mx else mx//n # px

        self.__WT = waiting_time

        # ----------------------------- tkinter - window ----------------------------- #

        self.__root = Tk()
        self.__root.title("Krecik")
        # self.__root.geometry("1200x800")
        self.__root.resizable(width=False, height=False)

        # ----------------------------- tkinter - images ----------------------------- #

        self.__formImages()

        # ----------------------------- tkinter - fields ----------------------------- #

        for i in range(w):
            for j in range(h):
                l = Label(self.__root, image=self.__images["dirt"], bd=0)
                l.grid(row=j, column=i, sticky=W)

        # ----------------------------- tkinter - objects ---------------------------- #

        # @FIXME: implement object loading

        # ------------------------ tkinter - objects - krecik ------------------------ #

        _k = Label(self.__root, image="", bd=0, bg='black')
        _k.grid(row=0, column=0, sticky=W)
        _k.config(image=self.__images["krecik_idle_S"])
        self.__krecik_field = _k
        # # l4.grid_forget() # usuwanie

        # ---------------------------- tkinter - log label --------------------------- #

        _l = Label(self.__root, text="Starting...", font="none 12 bold")
        _l.grid(row=h+1, column=0, columnspan=w, sticky=W)
        self.__cmd_label = _l

        # -------------------------- tkinter - window cont. -------------------------- #

        # self.__root.mainloop()
        # self.__root.update_idletasks()
        self.__root.update()
        self.__root.protocol("WM_DELETE_WINDOW", self.__on_closing)

    # ---------------------------------------------------------------------------- #
    #                              tkinter funny stuff                             #
    # ---------------------------------------------------------------------------- #

    def __on_closing(self):
        # @FIXME: closing window by x button generates exception
        self.__root.destroy()
        sys.exit()

    # ---------------------------------------------------------------------------- #
    #                                    assets                                    #
    # ---------------------------------------------------------------------------- #

    def __formImages(self):

        # ---------------------------------- obiekty --------------------------------- #

        self.__images.update( {"dirt" :
            ImageTk.PhotoImage( Image.open(os.path.join("assets", "dirt.png"))
            .resize((self.__field_size, self.__field_size), Image.ANTIALIAS))
            })

        # ---------------------------------- krecik ---------------------------------- #

        self.__images.update( {"krecik_idle_W" :
            ImageTk.PhotoImage( Image.open(os.path.join("assets", "krecik_W.png"))
            .resize((self.__field_size, self.__field_size), Image.ANTIALIAS))
            })

        self.__images.update( {"krecik_idle_N" :
            ImageTk.PhotoImage( Image.open(os.path.join("assets", "krecik_N.png"))
            .resize((self.__field_size, self.__field_size), Image.ANTIALIAS))
            })

        self.__images.update( {"krecik_idle_E" :
            ImageTk.PhotoImage( Image.open(os.path.join("assets", "krecik_E.png"))
            .resize((self.__field_size, self.__field_size), Image.ANTIALIAS))
            })

        self.__images.update( {"krecik_idle_S" :
            ImageTk.PhotoImage( Image.open(os.path.join("assets", "krecik_S.png"))
            .resize((self.__field_size, self.__field_size), Image.ANTIALIAS))
            })

    # ---------------------------------------------------------------------------- #
    #                                 command_label                                #
    # ---------------------------------------------------------------------------- #

    def __setCommandLabelText(self, _cmd):
        k = self.__krecik_field
        info = k.grid_info()
        new_txt = f"At: ({info['row']},{info['column']}), Facing: {self.__krecik_rot.name}, Doing: {_cmd}"
        self.__cmd_label.config(text = new_txt)

    # ---------------------------------------------------------------------------- #
    #                                    krecik                                    #
    # ---------------------------------------------------------------------------- #

    def __moveN(self, n = 1):
        if n < 1:
            return
        for i in range(n):
            info = self.__krecik_field.grid_info()
            dx, dy = 0, -1
            try:
                self.__krecik_field.grid(row=info["row"]+dy, column=info["column"]+dx, sticky=W)
            except:
                pass
            time.sleep(self.__WT)
            self.__root.update()
        
    def __moveS(self, n = 1):
        if n < 1:
            return
        for i in range(n):
            info = self.__krecik_field.grid_info()
            dx, dy = 0, 1
            try:
                self.__krecik_field.grid(row=info["row"]+dy, column=info["column"]+dx, sticky=W)
            except:
                pass
            time.sleep(self.__WT)
            self.__root.update()

    def __moveE(self, n = 1):
        if n < 1:
            return
        for i in range(n):
            info = self.__krecik_field.grid_info()
            dx, dy = 1, 0
            try:
                self.__krecik_field.grid(row=info["row"]+dy, column=info["column"]+dx, sticky=W)
            except:
                pass
            time.sleep(self.__WT)
            self.__root.update()
        

    def __moveW(self, n = 1):
        if n < 1:
            return
        for i in range(n):
            info = self.__krecik_field.grid_info()
            dx, dy = -1, 0
            try:
                self.__krecik_field.grid(row=info["row"]+dy, column=info["column"]+dx, sticky=W)
            except:
                pass
            time.sleep(self.__WT)
            self.__root.update()

    def moveForward(self, n=1):
        self.__setCommandLabelText(f"Move forward ({n})")
        if ( self.__krecik_rot == Rot.W ):
            self.__moveW(n)
        elif ( self.__krecik_rot == Rot.N ):
            self.__moveN(n)
        elif ( self.__krecik_rot == Rot.E ):
            self.__moveE(n)
        elif ( self.__krecik_rot == Rot.S ):
            self.__moveS(n)

    def moveBackward(self, n=1):
        self.__setCommandLabelText(f"Move backward ({n})")
        if ( self.__krecik_rot == Rot.W ):
            self.__moveE(n)
        elif ( self.__krecik_rot == Rot.N ):
            self.__moveS(n)
        elif ( self.__krecik_rot == Rot.E ):
            self.__moveW(n)
        elif ( self.__krecik_rot == Rot.S ):
            self.__moveN(n)

    def moveLeft(self, n=1):
        self.__setCommandLabelText(f"Move left ({n})")
        if ( self.__krecik_rot == Rot.W ):
            self.__moveS(n)
        elif ( self.__krecik_rot == Rot.N ):
            self.__moveW(n)
        elif ( self.__krecik_rot == Rot.E ):
            self.__moveN(n)
        elif ( self.__krecik_rot == Rot.S ):
            self.__moveE(n)

    def moveRight(self, n=1):
        self.__setCommandLabelText(f"Move right ({n})")
        if ( self.__krecik_rot == Rot.W ):
            self.__moveN(n)
        elif ( self.__krecik_rot == Rot.N ):
            self.__moveE(n)
        elif ( self.__krecik_rot == Rot.E ):
            self.__moveS(n)
        elif ( self.__krecik_rot == Rot.S ):
            self.__moveW(n)

    def rotateLeft(self):
        self.__setCommandLabelText(f"Rotate left")
        if ( self.__krecik_rot == Rot.W ):
            self.__krecik_rot = Rot.S
            self.__krecik_field.config(image=self.__images["krecik_idle_S"])
        elif ( self.__krecik_rot == Rot.N ):
            self.__krecik_rot = Rot.W
            self.__krecik_field.config(image=self.__images["krecik_idle_W"])
        elif ( self.__krecik_rot == Rot.E ):
            self.__krecik_rot = Rot.N
            self.__krecik_field.config(image=self.__images["krecik_idle_N"])
        elif ( self.__krecik_rot == Rot.S ):
            self.__krecik_rot = Rot.E
            self.__krecik_field.config(image=self.__images["krecik_idle_E"])
        time.sleep(self.__WT)
        self.__root.update()

    def rotateRight(self):
        self.__setCommandLabelText(f"Rotate right")
        if ( self.__krecik_rot == Rot.W ):
            self.__krecik_rot = Rot.N
            self.__krecik_field.config(image=self.__images["krecik_idle_N"])
        elif ( self.__krecik_rot == Rot.N ):
            self.__krecik_rot = Rot.E
            self.__krecik_field.config(image=self.__images["krecik_idle_E"])
        elif ( self.__krecik_rot == Rot.E ):
            self.__krecik_rot = Rot.S
            self.__krecik_field.config(image=self.__images["krecik_idle_S"])
        elif ( self.__krecik_rot == Rot.S ):
            self.__krecik_rot = Rot.W
            self.__krecik_field.config(image=self.__images["krecik_idle_W"])
        time.sleep(self.__WT)
        self.__root.update()

# ---------------------------------------------------------------------------- #
#                                 sample usage                                 #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":

    win = KrecikWindow(15,10)

    win.moveForward(5)
    win.rotateLeft()
    win.moveForward(5)

    exit = input("Pres enter to exit.\n")