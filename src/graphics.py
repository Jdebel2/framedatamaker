from tkinter import Tk, Canvas, BOTH, NW, Label
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
from enum import Enum
import json

class ButtonFunction(Enum):
    NEW=1
    LOAD=2
    CLICK_TIMELINE=3
    CLICK_LEFT_BUTTON_TIMELINE=4
    CLICK_RIGHT_BUTTON_TIMELINE=5
    SWITCH_BOX_TYPE=6
    SAVE=7


class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Frame Data Maker")
        self.__root.resizable(width=False, height=False)
        self.__canvas = Canvas(self.__root, {"bg": "black"}, height=height, width=width, highlightcolor='black')
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__canvas.focus_set()
        self.width = width
        self.height = height
        self.__root.protocol("WM_DELETE_WINDOW", self.__root.destroy)


    def get_root(self):
        return self.__root


    def get_canvas(self):
        return self.__canvas


    def draw_sprite(self, sprite):
        x2 = sprite.x + sprite.img.width
        y2 = sprite.y + sprite.img.height
        self.__canvas.create_rectangle(sprite.x, sprite.y, x2, y2, fill='black', outline='black')
        self.__canvas.create_image(sprite.x,sprite.y,anchor=NW,image=sprite.render)
        self.__canvas.pack()
    

    def draw_box(self, box, draw_border=False):
        if draw_border:
            box.border = Image.new("RGBA", (box.width+6, box.height+6), color=(200, 200, 0, 100))
            box.border_render = ImageTk.PhotoImage(box.border)
            border_id = self.__canvas.create_image(box.x-3,box.y-3,anchor=NW,image=box.border_render)
            id = self.__canvas.create_image(box.x,box.y,anchor=NW,image=box.render)
            self.__canvas.pack()
            return id, border_id
        id = self.__canvas.create_image(box.x,box.y,anchor=NW,image=box.render)
        return id


    def draw_box_corner(self, x, y, render):
        id = self.__canvas.create_image(x, y,anchor=NW, image=render)
        return id


    def draw_button(self, btn, x, y):
        self.__canvas.create_window(x,y,window=btn, anchor=NW)
    

    def draw_rect(self, x1, y1, x2, y2, color):
        id = self.__canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        return id


    def draw_text(self,x,y,text_obj):
        self.__canvas.create_window(x,y,window=text_obj, anchor=NW)


    def mainloop(self):
        self.__root.mainloop()
        print("window closed...")


class FDMSprite():
    def __init__(self, img, x, y, win):
        self.id = -1
        self.img = img
        self.render = ImageTk.PhotoImage(img)
        self.x = x
        self.y = y
        self.button = None
        self.win = win
    

    def update_render(self):
        self.render = ImageTk.PhotoImage(self.img)
        if (self.button):
            self.add_button(self.render)


    def add_button(self, timelinesprite):
        self.button = FDMButton("",self.x, self.y, self.img.width, self.img.height, ButtonFunction.CLICK_TIMELINE, self.win, image=self.render, timelinesprite=timelinesprite)


    def copy(self):
        return FDMSprite(self.img, self.x, self.y, self.win)


    def set_position(self, x, y):
        self.x = x
        self.y = y


    def draw(self):
        if (self.button):
            self.button.draw()
        self.win.draw_sprite(self)
        

class FDMButton():
    def __init__(self,text, x, y, width, height, mode, win, editor=None, image=None, timelinesprite=None):
        cmnd=None
        match (mode): 
            case ButtonFunction.NEW:
                cmnd=self.create_new
            case ButtonFunction.CLICK_TIMELINE:
                cmnd=self.click_timeline
            case ButtonFunction.CLICK_LEFT_BUTTON_TIMELINE:
                cmnd=self.click_timeline_left_button
            case ButtonFunction.CLICK_RIGHT_BUTTON_TIMELINE:
                cmnd=self.click_timeline_right_button
            case ButtonFunction.SWITCH_BOX_TYPE:
                cmnd=self.switch_box_type
            case ButtonFunction.SAVE:
                cmnd=self.save_editor_progress
            case ButtonFunction.LOAD:
                cmnd=self.load_editor_progress
            case _:
                raise NotImplementedError("Not yet implemented")
            
        background = 'gray'
        foreground = 'white'
        border=1
        if image != None:
            background = 'black'
            foreground = 'black'
            border=3

        self.btn = Label(
            win.get_root(), 
            text=text, 
            width=width, 
            height=height,
            image=image,
            relief='raised',
            background=background,
            foreground=foreground,
            bd=border,
        )
        self.btn.bind("<Button-1>", lambda e: cmnd())
        self.x = x
        self.y = y
        self.editor = editor
        self.timelinesprite = timelinesprite
        self.win=win
    

    def draw(self):
        self.win.draw_button(self.btn, self.x, self.y)
    

    def create_new(self):
        filename = askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png")])
        if not filename:
            return
        self.editor.image_file_path = filename
        img = Image.open(filename)
        self.editor.load_data(img, filename)
        self.editor.animation.draw()
        self.editor.timeline.draw()
    
    
    def click_timeline(self):
        editor = self.timelinesprite.editor
        editor.jump_to(self.timelinesprite.index)


    def click_timeline_left_button(self):
        self.editor.jump_to_unintrusive(max(self.editor.timeline.start_index-1,0))


    def click_timeline_right_button(self):
        self.editor.jump_to_unintrusive(min(self.editor.timeline.end_index+1, len(self.editor.timeline.sprites)-1))


    def switch_box_type(self):
        if self.editor.create_mode == 'hitbox':
            self.editor.switch_create_mode('hurtbox')
        elif self.editor.create_mode == 'hurtbox':
            self.editor.switch_create_mode('hitbox')
    
    
    def save_editor_progress(self):
        if self.editor.is_editor_running:
            filename = asksaveasfilename(initialfile = "frame_data_editor_progress",title = "Select file",filetypes = (("JSON files","*.json"),("all files","*.*")))
            if not filename:
                return
            with open(filename, 'w') as f:
                f.write('{')
                f.write(f'\"img_path\":\"{self.editor.image_file_path}\",\n')
                f.write(f'\"origin_point\":[{self.editor.origin_point.x}, {self.editor.origin_point.y}],\n')
                f.write(f'\"hitbox_flag_data\": [')
                hitbox_flags = []
                hurtbox_flags = []
                for flag in self.editor.flags:
                    if flag.type == 'hitbox':
                        hitbox_flags.append(flag)
                for flag in self.editor.flags:
                    if flag.type == 'hurtbox':
                        hurtbox_flags.append(flag)
                is_first_flag = True
                for flag in hitbox_flags:
                    if is_first_flag:
                        is_first_flag = False
                    else:
                        f.write(',')
                    f.write('[')
                    is_first_change = True
                    for change in flag.frame_changes:
                        if is_first_change:
                            is_first_change = False
                        else:
                            f.write(',')
                        f.write('{')
                        if 'enabled' in change:
                            f.write(f'\"enabled\":\"{change['enabled']}\"')
                        if 'position' in change:
                            f.write(f',\"position\":{change['position']}')
                        if 'editor_position' in change:
                            f.write(f',\"editor_position\":{change['editor_position']}')
                        if 'scale' in change:
                            f.write(f',\"scale\":{change['scale']}')
                        f.write('}')
                    f.write(f']')
                f.write('],\n')
                f.write(f'\"hurtbox_flag_data\": [')
                is_first_flag = True
                for flag in hurtbox_flags:
                    if is_first_flag:
                        is_first_flag = False
                    else:
                        f.write(',')
                    f.write('[')
                    is_first_change = True
                    for change in flag.frame_changes:
                        if is_first_change:
                            is_first_change = False
                        else:
                            f.write(',')
                        f.write('{')
                        if 'enabled' in change:
                            f.write(f'\"enabled\":\"{change['enabled']}\"')
                        if 'position' in change:
                            f.write(f',\"position\":{change['position']}')
                        if 'editor_position' in change:
                            f.write(f',\"editor_position\":{change['editor_position']}')
                        if 'scale' in change:
                            f.write(f',\"scale\":{change['scale']}')
                        f.write('}')
                    f.write(f']')
                f.write(']')
                f.write('}')


    def load_editor_progress(self):
        filename = askopenfilename(title="Open Frame Data Progress File", filetypes=[("JSON files", "*.json")])
        if not filename:
            return
        with open(filename) as f:
            file_data = json.load(f)
            self.editor.image_file_path = file_data['img_path']
            img = Image.open(file_data['img_path'])
            self.editor.load_data(img, file_data['img_path'])
            self.editor.animation.draw()
            self.editor.timeline.draw()
            self.editor.origin_point.set_position(file_data['origin_point'][0], file_data['origin_point'][1])
            for hitbox_flags in file_data['hitbox_flag_data']:
                n_box, n_flag = self.editor.create_box_on_load(0,0,'hitbox')
                for change_idx in range(len(hitbox_flags)):
                    change = hitbox_flags[change_idx]
                    n_change = {}
                    if 'enabled' in change:
                        enable = True if change['enabled'] == 'True' else False
                        n_change['enabled'] = enable
                    if 'position' in change:
                        n_change['position'] = change['position']
                    if 'editor_position' in change:
                        n_change['editor_position'] = change['editor_position']
                    if 'scale' in change:
                        n_change['scale'] = change['scale']
                    n_flag.frame_changes[change_idx] = n_change
            for hurtbox_flags in file_data['hurtbox_flag_data']:
                n_box, n_flag = self.editor.create_box_on_load(0,0,'hurtbox')
                for change_idx in range(len(hurtbox_flags)):
                    change = hurtbox_flags[change_idx]
                    n_change = {}
                    if 'enabled' in change:
                        enable = True if change['enabled'] == 'True' else False
                        n_change['enabled'] = enable
                    if 'position' in change:
                        n_change['position'] = change['position']
                    if 'editor_position' in change:
                        n_change['editor_position'] = change['editor_position']
                    if 'scale' in change:
                        n_change['scale'] = change['scale']
                    n_flag.frame_changes[change_idx] = n_change
            self.editor.jump_to(0)