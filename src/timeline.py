from graphics import FDMButton, ButtonFunction
from tkinter import Label
from PIL import Image, ImageTk

class Timeline():
    def __init__(self, editor, win):
        self.sprites = []
        self.start_index = 0
        self.end_index = 0
        self.current_index = 0
        self.subdivisions = None
        self.width = None
        self.height = None
        self.max_timeline_sprites = 5
        self.timeline_height = win.height - 50
        self.editor = editor
        self.win = win
        self.win.draw_rect(0,self.timeline_height - 25, win.width,win.height, '#222222')
        self.frame_indicator = Label(self.win.get_root(), text=f'Frame: 0', foreground='white', background='#222222')
        self.left_chevron = Image.open('assets/Left_chevron.png')
        self.left_chevron_render = ImageTk.PhotoImage(self.left_chevron)
        self.right_chevron = Image.open('assets/Right_chevron.png')
        self.right_chevron_render = ImageTk.PhotoImage(self.right_chevron)
        self.left_button = None
        self.right_button = None
        self.frame_labels = []


    def load_data(self, anim):
        self.left_button = FDMButton("",10, self.timeline_height,32,32,ButtonFunction.CLICK_LEFT_BUTTON_TIMELINE, self.win, self.editor, image=self.left_chevron_render)
        self.right_button = FDMButton("",self.win.width-42, self.timeline_height,32,32,ButtonFunction.CLICK_RIGHT_BUTTON_TIMELINE, self.win, self.editor, image=self.right_chevron_render)
        self.left_button.draw()
        self.right_button.draw()
        self.subdivisions = anim.subdivisions
        self.max_timeline_sprites = min(5, self.subdivisions)
        self.end_index = self.max_timeline_sprites-1
        self.width = anim.width
        self.height = anim.height
        for idx in range(len(anim.sprites)):
            spr = anim.sprites[idx]
            self.sprites.append(TimelineSprite(self.editor, spr.copy(), idx))
        self.create_timeline_sprites()
        self.draw_frame_indicator()
        self.left_button.btn.configure(state='disabled')
    

    def create_timeline_sprites(self):
        for idx in range(self.start_index, self.end_index+1):
            self.sprites[idx].sprite.img = self.sprites[idx].sprite.img.resize((int(self.width/1.5), int(self.height//1.5)), Image.NEAREST)
            self.sprites[idx].sprite.update_render()
        self.update_timeline_sprite_positions()
        for spr in self.sprites:
            spr.sprite.add_button(spr)

        
    def update_timeline_sprite_positions(self):
        start_pos = self.win.width - self.width
        dist_between = 1/(self.max_timeline_sprites+1)
        curr_dist = dist_between

        for idx in range(self.start_index, self.end_index+1):
            self.sprites[idx].sprite.set_position(int(start_pos * curr_dist), self.timeline_height)
            self.sprites[idx].sprite.update_render()
            curr_dist += dist_between


    def render_frame_labels(self):
        start_pos = self.win.width - self.width
        dist_between = 1/(self.max_timeline_sprites+1)
        curr_dist = dist_between

        if (len(self.frame_labels) == 0):
            for idx in range(self.max_timeline_sprites):
                self.frame_labels.append(Label(self.win.get_root(), text=f'{idx}', foreground='white', background='#222222'))
        else:
            frame_index = 0
            for idx in range(self.start_index, self.end_index+1):
                self.frame_labels[frame_index].configure(text=f'{idx}')
                frame_index+=1
        for label in self.frame_labels:
            self.win.draw_text(int(start_pos * curr_dist), self.timeline_height-20, label)
            curr_dist += dist_between


    def update_index_range(self):
        if self.subdivisions < 5:
            return False
        
        if self.current_index >= self.start_index and self.current_index <= self.end_index:
            return False
        
        if self.current_index < 0 or self.current_index >= len(self.sprites):
            return False

        if self.current_index < self.start_index:
            self.start_index = self.current_index
            self.end_index = self.start_index+4
        elif self.current_index > self.end_index:
            self.end_index = self.current_index
            self.start_index = self.end_index-4
        else:
            raise ValueError("how the hell did you manange to throw this?")
        self.create_timeline_sprites()
        if self.start_index == 0:
            self.left_button.btn.configure(state='disabled')
        elif self.left_button.btn['state']=='disabled':
            self.left_button.btn.configure(state='normal')
        
        if self.end_index == len(self.sprites)-1:
            self.right_button.btn.configure(state='disabled')
        elif self.right_button.btn['state']=='disabled':
            self.right_button.btn.configure(state='normal')

        return True


    def draw(self):
        for idx in range(self.start_index, self.end_index+1):
            self.sprites[idx].sprite.draw()
        self.render_frame_labels()
    

    def draw_frame_indicator(self):
        self.frame_indicator.configure(text=f'Frame: {self.current_index}')
        self.win.draw_text(10,self.timeline_height-25,self.frame_indicator)


class TimelineSprite():
    def __init__(self, editor, sprite, index):
        self.editor = editor
        self.sprite = sprite
        self.index = index