from tkinter import Tk, Canvas, BOTH, PhotoImage, Label, NW, Button
from enum import Enum


class ButtonFunction(Enum):
    NEW=1
    LOAD=2


class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Frame Data Maker")
        self.__canvas = Canvas(self.__root, {"bg": "black"}, height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)


    def get_root(self):
        return self.__root


    def draw_image(self, image, x, y):
        self.__canvas.create_image(x,y,anchor=NW,image=image)


    def draw_button(self, btn, x, y):
        btn.place(x=x, y=y)


    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")
    

    def close(self):
        self.__running = False


class FDMImage():
    def __init__(self, spr_path, x, y, win):
        self.img = PhotoImage(file=spr_path)
        self.x = x
        self.y = y
        self.win = win
    

    def draw(self):
        self.win.draw_image(self.img, self.x, self.y)
        

class FDMButton():
    def __init__(self,text, x, y, width, height, mode, win):
        command=None
        match (mode): 
            case ButtonFunction.NEW:
                command=self.create_new
            case _:
                raise NotImplementedError("Only NEW is implemented")
        self.btn = Button(win.get_root(), text=text, width=width, height=height, bd='1', command=command)
        self.x = x
        self.y = y
        self.win=win
    

    def draw(self):
        self.win.draw_button(self.btn, self.x, self.y)
    

    def create_new(self):
        print("We are making frame data!")