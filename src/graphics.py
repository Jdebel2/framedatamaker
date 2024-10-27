from tkinter import Tk, Canvas, BOTH, PhotoImage, Label, NW

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Frame Data Maker")
        self.__canvas = Canvas(self.__root, {"bg": "black"}, height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)


    def draw_image(self, image, x, y):
        self.__canvas.create_image(x,y,anchor=NW,image=image)


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


class Sprite():
    def __init__(self, spr_path, x, y, win):
        self.img = PhotoImage(file=spr_path)
        self.x = x
        self.y = y
        self.win = win
    

    def draw(self):
        self.win.draw_image(self.img, self.x, self.y)
        

