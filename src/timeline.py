from graphics import FDMSprite
from PIL import Image

class Timeline():
    def __init__(self, win):
        self.sprites = []
        self.start_index = 0
        self.end_index = 0
        self.subdivisions = None
        self.width = None
        self.height = None
        self.max_timeline_sprites = 5
        self.timeline_height = win.height - 50
        self.win = win
    

    def load_data(self, anim):
        self.subdivisions = anim.subdivisions
        self.width = anim.width
        self.height = anim.height
        for spr in anim.sprites:
            self.sprites.append(spr.copy())
        self.create_timeline_sprites()
    

    def create_timeline_sprites(self):
        for idx in range(self.subdivisions):
            self.sprites[idx].img = self.sprites[idx].img.resize((int(self.width/1.5), int(self.height//1.5)), Image.NEAREST)
        self.max_timeline_sprites = min(5, self.subdivisions)
        self.end_index = self.max_timeline_sprites
        self.update_timeline_sprite_positions()

        
    def update_timeline_sprite_positions(self):
        start_pos = self.win.width - self.width
        dist_between = 1/(self.max_timeline_sprites+1)
        curr_dist = dist_between

        for idx in range(self.start_index, self.end_index):
            self.sprites[idx].set_position(int(start_pos * curr_dist), self.timeline_height)
            curr_dist += dist_between


    def draw(self):
        for idx in range(self.start_index, self.end_index):
            self.sprites[idx].draw()