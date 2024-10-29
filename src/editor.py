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
    

    def jump_to(self, frame):
        self.jump_to_unintrusive(frame)
        self.animation.current_sprite = self.animation.sprites[frame]
        self.animation.draw()
        self.timeline.draw_frame_indicator()
    

    def jump_to_unintrusive(self, frame):
        self.timeline.current_index = frame
        if self.timeline.update_index_range():
            self.timeline.draw()