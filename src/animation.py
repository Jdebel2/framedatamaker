from graphics import FDMSprite
from PIL import Image

class Animation():
    def __init__(self, win):
        self.sprite = None
        self.subdivisions = None
        self.width = None
        self.height = None
        self.sprites = []
        self.current_sprite = None
        self.win = win
    
    
    def load_info(self, spritesheet, path):
        self.sprite = spritesheet
        self.subdivisions = int(path.split('strip',1)[-1].split('.',1)[0])
        self.width, self.height = spritesheet.size
        self.width //= self.subdivisions
    

    def create_sprites(self):
        for idx in range(self.subdivisions):
            n_image = self.sprite.crop((self.width*idx,0,self.width*(idx+1),self.height)).resize((self.width, self.height), Image.NEAREST)
            sprite = FDMSprite(n_image, 20, 75, self.win)
            self.sprites.append(sprite)
        self.current_sprite = self.sprites[0]
        self.current_sprite.draw()