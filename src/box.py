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
        self.can_move = False
        

    def set_position(self,x,y):
        self.x = x
        self.y = y


    def set_scale(self, width, height):
        self.width = width
        self.height = height


    def update_can_move(self):
        self.can_move = not self.can_move
        print(f"{self.x}, {self.y} movable = {self.can_move}")


    def draw(self):
        self.win.draw_box(self)


class Hitbox(Box):
    def __init__(self, x, y, width, height, win):
        super().__init__(x, y, width, height, (255, 0, 0, 100), win)
    

class Hurtbox(Box):
    def __init__(self, x, y, width, height, win):
        super().__init__(x, y, width, height, (0,255,0,100), win)