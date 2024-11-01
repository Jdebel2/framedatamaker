from animation import Animation
from timeline import Timeline
from graphics import FDMButton, ButtonFunction
from box import Hitbox, Hurtbox

class Editor():
    def __init__(self, win):
        self.animation = Animation(win)
        self.timeline = Timeline(self, win)
        self.win = win
        self.hitboxes = []
        self.hurtboxes = []
        self.create_mode = 'hitbox'
        self.switch_btn = None
    

    def load_data(self, spritesheet, path):
        self.animation.load_data(spritesheet, path)
        self.timeline.load_data(self.animation)
        self.win.get_canvas().bind("<Button-1>", self.get_box)
        self.win.get_canvas().bind("<Button-2>", self.callback)
        self.win.get_canvas().bind("<Button-3>", self.callback)
        self.switch_btn = FDMButton("Create Hitbox", 20, 40, 12, 1, ButtonFunction.SWITCH_BOX_TYPE, self.win, self)
        self.switch_btn.draw()
    

    def callback(self, event):
        if event.y < self.timeline.timeline_height-50:
            match self.create_mode:
                case 'hitbox':
                    n_hitbox = Hitbox(event.x,event.y, 50, 50, self.win)
                    self.hitboxes.append(n_hitbox)
                    n_hitbox.draw()
                case 'hurtbox':
                    n_hurtbox = Hurtbox(event.x,event.y, 50, 50, self.win)
                    self.hitboxes.append(n_hurtbox)
                    n_hurtbox.draw()
    

    def get_box(self, event):
        if event.y >= self.timeline.timeline_height-50:
            return
        items = self.win.get_canvas().find_overlapping(event.x-1,event.y-1, event.x+1, event.y+1)
        if len(items) != 0:
            print(items[-1])
    

    def switch_create_mode(self, new_mode):
        if new_mode != 'hitbox' and new_mode != 'hurtbox':
            return
        self.create_mode = new_mode
        match new_mode:
            case 'hitbox':
                self.switch_btn.btn.configure(text='Create Hitbox')
            case 'hurtbox':
                self.switch_btn.btn.configure(text='Create Hurtbox')


    def jump_to(self, frame):
        self.jump_to_unintrusive(frame)
        self.animation.current_sprite = self.animation.sprites[frame]
        self.animation.draw()
        self.timeline.draw_frame_indicator()
    

    def jump_to_unintrusive(self, frame):
        self.timeline.current_index = frame
        if self.timeline.update_index_range():
            self.timeline.draw()