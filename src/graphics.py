from tkinter import Tk, Canvas, BOTH, PhotoImage, NW, Button, Label
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
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
        self.__root.protocol("WM_DELETE_WINDOW", self.__root.destroy)


    def get_root(self):
        return self.__root


    def draw_image(self, fdmimage, x, y):
        width, height = fdmimage.img.size
        width /= 7
        idx = 0

        n_image = fdmimage.img.crop((width*idx,0,width*(idx+1),height))
        n_size = (width,height)
        n_image = n_image.resize(n_size, resample=Image.NEAREST)
        global n_render
        n_render = ImageTk.PhotoImage(n_image)
        self.__canvas.create_image(x,y,anchor=NW,image=n_render)
        self.__canvas.pack()


    def draw_button(self, btn, x, y):
        btn.place(x=x, y=y)
    

    def mainloop(self):
        self.__root.mainloop()
        print("window closed...")


class FDMImage():
    def __init__(self, spr_path, x, y, win):
        self.img = Image.open(spr_path)
        self.render = ImageTk.PhotoImage(self.img)
        self.x = x
        self.y = y
        self.win = win
    

    def draw(self):
        self.win.draw_image(self, self.x, self.y)
        

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
        filename = askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png")])
        global spr
        spr = FDMImage(filename, 100, 300, self.win)
        spr.draw()