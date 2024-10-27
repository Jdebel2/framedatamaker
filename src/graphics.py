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
        self.__root.resizable(width=False, height=False)
        self.__canvas = Canvas(self.__root, {"bg": "black"}, height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.width = width
        self.height = height
        self.__root.protocol("WM_DELETE_WINDOW", self.__root.destroy)


    def get_root(self):
        return self.__root


    def draw_sprite(self, sprite):
        sprite.img = ImageTk.PhotoImage(sprite.img)
        self.__canvas.create_image(sprite.x,sprite.y,anchor=NW,image=sprite.img)
        self.__canvas.pack()


    def draw_button(self, btn, x, y):
        btn.place(x=x, y=y)
    

    def mainloop(self):
        self.__root.mainloop()
        print("window closed...")


class FDMSprite():
    def __init__(self, img, x, y, win):
        self.img = img
        self.x = x
        self.y = y
        self.win = win
    

    def draw(self):
        self.win.draw_sprite(self)
        

class FDMButton():
    def __init__(self,text, x, y, width, height, mode, win, anim=None):
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
        self.anim = anim
    

    def draw(self):
        self.win.draw_button(self.btn, self.x, self.y)
    

    def create_new(self):
        filename = askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png")])
        img = Image.open(filename)
        self.anim.load_info(img, filename)
        self.anim.create_sprites()