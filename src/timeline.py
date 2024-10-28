from graphics import FDMSprite
from PIL import Image

class Timeline():
    def __init__(self, editor, win):
        self.sprites = []
        self.start_index = 0
        self.end_index = 0
        self.subdivisions = None
        self.width = None
        self.height = None
        self.max_timeline_sprites = 5
        self.timeline_height = win.height - 50
        self.editor = editor
        self.win = win
    

    def load_data(self, anim):
        self.subdivisions = anim.subdivisions
        self.width = anim.width
        self.height = anim.height
        for idx in range(len(anim.sprites)):
            spr = anim.sprites[idx]
            self.sprites.append(TimelineSprite(self.editor, spr.copy(), idx))
        self.create_timeline_sprites()
    

    def create_timeline_sprites(self):
        for idx in range(self.subdivisions):
            self.sprites[idx].sprite.img = self.sprites[idx].sprite.img.resize((int(self.width/1.5), int(self.height//1.5)), Image.NEAREST)
            self.sprites[idx].sprite.update_render()
        self.max_timeline_sprites = min(5, self.subdivisions)
        self.end_index = self.max_timeline_sprites
        self.update_timeline_sprite_positions()
        for spr in self.sprites:
            spr.sprite.add_button(spr)

        
    def update_timeline_sprite_positions(self):
        start_pos = self.win.width - self.width
        dist_between = 1/(self.max_timeline_sprites+1)
        curr_dist = dist_between

        for idx in range(self.start_index, self.end_index):
            self.sprites[idx].sprite.set_position(int(start_pos * curr_dist), self.timeline_height)
            self.sprites[idx].sprite.update_render()
            curr_dist += dist_between


    def draw(self):
        for idx in range(self.start_index, self.end_index):
            self.sprites[idx].sprite.draw()


class TimelineSprite():
    def __init__(self, editor, sprite, index):
        self.editor = editor
        self.sprite = sprite
        self.index = index