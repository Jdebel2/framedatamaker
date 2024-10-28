from animation import Animation
from timeline import Timeline

class Editor():
    def __init__(self, win):
        self.animation = Animation(win)
        self.timeline = Timeline(self, win)
        self.win = win
    

    def load_data(self, spritesheet, path):
        self.animation.load_data(spritesheet, path)
        self.timeline.load_data(self.animation)