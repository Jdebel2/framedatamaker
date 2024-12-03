from tkinter import Label
from PIL import Image, ImageTk

class Box():
    def __init__(self, x, y, width, height, color, win):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.win = win
        self.color = color
        self.img = Image.new("RGBA", (self.width, self.height), color=color)
        self.render = ImageTk.PhotoImage(self.img)
        self.border = Image.new("RGBA", (self.width+6, self.height+6), color=(200, 200, 0, 100))
        self.border_render = ImageTk.PhotoImage(self.border)
        self.border_corner_tl = BoxCorner(0,0,10,10,color,'tl',win)
        self.border_corner_tr = BoxCorner(0,0,10,10,color,'tr',win)
        self.border_corner_bl = BoxCorner(0,0,10,10,color,'bl',win)
        self.border_corner_br = BoxCorner(0,0,10,10,color,'br',win)
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
            self.border_corner_tl.set_position(self.x-3, self.y-3)
            self.border_corner_tr.set_position(self.x+self.width-3, self.y-3)
            self.border_corner_bl.set_position(self.x-3, self.y+self.height-3)
            self.border_corner_br.set_position(self.x+self.width-3, self.y+self.height-3)
            self.border_corner_tl.draw()
            self.border_corner_tr.draw()
            self.border_corner_bl.draw()
            self.border_corner_br.draw()
            self.img = Image.new("RGBA", (self.width, self.height), color=self.color)
            self.render = ImageTk.PhotoImage(self.img)
            self.box_id, self.border_id = self.win.draw_box(self, draw_border=True)
        else:
            self.border_corner_tl.remove()
            self.border_corner_tr.remove()
            self.border_corner_bl.remove()
            self.border_corner_br.remove()
            self.box_id = self.win.draw_box(self)


class BoxCorner():
    def __init__(self, x, y, width, height, color, type, win):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.type = type
        self.win = win
        self.image = Image.new("RGB", (width, height), color=color)
        self.render = ImageTk.PhotoImage(self.image)
        self.id = -1
    

    def set_position(self, x, y):
        self.x = x
        self.y = y


    def draw(self):
        if self.id != -1:
            self.win.get_canvas().delete(self.id)
        self.id = self.win.draw_box_corner(self.x, self.y, self.render)


    def remove(self):
        if self.id != -1:
            self.win.get_canvas().delete(self.id)
        self.id = -1


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