from animation import Animation
from timeline import Timeline

class Editor():
    def __init__(self, win):
        self.animation = Animation(win)
        self.timeline = Timeline(self, win)
        self.win = win
        self.win.get_root().bind("<Return>", lambda e: self.jump_to(6))
    

    def load_data(self, spritesheet, path):
        self.animation.load_data(spritesheet, path)
        self.timeline.load_data(self.animation)
    

    def jump_to(self, frame):
        self.timeline.current_index = frame
        self.animation.current_sprite = self.animation.sprites[frame]
        self.animation.draw()
        if self.timeline.update_index_range():
            self.timeline.draw()
        else:
            self.timeline.draw_frame_indicator()