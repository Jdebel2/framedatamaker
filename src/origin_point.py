from tkinter import Label
from PIL import Image, ImageTk

class OriginPoint():
    def __init__(self, x, y, win):
        self.x = x
        self.y = y
        self.win = win
        self.image = Image.new("RGBA", (5, 5), color=(255, 255, 255, 100))
        self.render = ImageTk.PhotoImage(self.image)
        self.id = -1
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        if self.id != -1:
            self.win.get_canvas().delete(self.id)
        self.id = self.win.draw_box_corner(self.x, self.y, self.render)