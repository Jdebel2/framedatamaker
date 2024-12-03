from tkinter import Label
from PIL import Image, ImageTk

class Box():
    def __init__(self, x, y, width, height, color, win):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.win = win
        self.img = Image.new("RGBA", (self.width, self.height), color=color)
        self.render = ImageTk.PhotoImage(self.img)
        self.border = Image.new("RGB", (self.width+6, self.height+6), color=(200, 200, 0))
        self.border_render = ImageTk.PhotoImage(self.border)
        self.box_id = -1
        self.border_id = -1
        self.can_move = False
        

    def copy(self):
        raise NotImplementedError("Copy function not implemented in base class")


    def set_position(self,x,y):
        self.x = x
        self.y = y


    def set_scale(self, width, height):
        self.width = width
        self.height = height


    def set_can_move(self, value):
        self.can_move = value
        print(f"{self.x}, {self.y} movable = {self.can_move}")
        self.draw()


    def draw(self):
        if self.box_id != -1:
            self.win.get_canvas().delete(self.box_id)
        if self.border_id != -1:
            self.win.get_canvas().delete(self.border_id)
        if self.can_move:
            self.box_id, self.border_id = self.win.draw_box(self, draw_border=True)
        else:
            self.box_id = self.win.draw_box(self)


class Hitbox(Box):
    def __init__(self, x, y, width, height, win):
        super().__init__(x, y, width, height, (255, 0, 0, 100), win)
    

    def copy(self):
        return Hitbox(self.x, self.y, self.width, self.height, self.win)
    

class Hurtbox(Box):
    def __init__(self, x, y, width, height, win):
        super().__init__(x, y, width, height, (0,255,0,100), win)
    

    def copy(self):
        return Hurtbox(self.x, self.y, self.width, self.height, self.win)