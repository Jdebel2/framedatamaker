from animation import Animation
from timeline import Timeline
from graphics import FDMButton, ButtonFunction
from box import Hitbox, Hurtbox

class Editor():
    def __init__(self, win):
        self.animation = Animation(win)
        self.timeline = Timeline(self, win)
        self.win = win
        self.boxes = []
        self.create_mode = 'hitbox'
        self.adjust_mode = 'all'
        self.switch_btn = None
        self.moving_box = False
        self.moving_box_corner = False
        self.moving_box_corner_origin_diff = [0,0]
        self.moving_box_origin_diff = [0,0]
        self.current_selected_box = None
        self.current_selected_box_corner = None
        self.ghost_index = -1
        self.ghost_box = None
    

    def load_data(self, spritesheet, path):
        self.animation.load_data(spritesheet, path)
        self.timeline.load_data(self.animation)
        self.win.get_canvas().bind("<Button-1>", self.left_click_event)
        self.win.get_canvas().bind("<ButtonRelease-1>", self.left_click_release_event)
        self.win.get_canvas().bind("<B1-Motion>", self.left_click_hold_event)
        self.win.get_canvas().bind("<Button-2>", self.right_click_event)
        self.win.get_canvas().bind("<Button-3>", self.right_click_event)
        self.win.get_canvas().bind("<Key>", self.s_key_release_event)
        self.switch_btn = FDMButton("Create Hitbox", 20, 40, 12, 1, ButtonFunction.SWITCH_BOX_TYPE, self.win, self)
        self.switch_btn.draw()
    

    def s_key_release_event(self, event):
        if event.char == 'q':
            self.adjust_mode = 'all'
            print('Adjust mode set: all')
        elif event.char == 'w':
            self.adjust_mode = 'position'
            print('Adjust mode set: position')
        elif event.char == 'e':
            self.adjust_mode = 'scale'
            print('Adjust mode set: scale')


    def right_click_event(self, event):
        if event.y < self.timeline.timeline_height-50:
            n_box = None
            match self.create_mode:
                case 'hitbox':
                    n_box = Hitbox(event.x,event.y, 50, 50, self.win)
                case 'hurtbox':
                    n_box = Hurtbox(event.x,event.y, 50, 50, self.win)
            if n_box != None:
                self.boxes.append(n_box)
                n_box.draw()
                return
            raise Exception("Error - box object not added")
    

    def left_click_event(self, event):
        if event.y >= self.timeline.timeline_height-50:
            return
        items = self.win.get_canvas().find_overlapping(event.x-1,event.y-1, event.x+1, event.y+1)
        box_corner_target = None
        box_target = None
        self.moving_box = False
        if len(items) != 0:
            if self.current_selected_box != None and self.adjust_mode != 'position':
                box_corner_target = self.get_box_corner_by_canvas_id(self.current_selected_box, items)
                if box_corner_target != None:
                    self.current_selected_box_corner = box_corner_target
                    self.moving_box_corner = True
                    self.moving_box_corner_origin_diff[0] = event.x - box_corner_target.x
                    self.moving_box_corner_origin_diff[1] = event.y - box_corner_target.y
                    print(self.moving_box_corner_origin_diff)
                    return
            target = items[-1]
            box_target = self.get_box_by_canvas_id(target)
            if box_target != None:
                if (not box_target.can_move):
                    for hb in self.boxes:
                        if hb.box_id != box_target.box_id:
                            hb.set_can_move(False)
                    box_target.set_can_move(True)
                    self.current_selected_box = box_target
                else:
                    if self.adjust_mode != 'scale':
                        print("Time to change position!")
                        self.moving_box = True
                        self.moving_box_origin_diff[0] = event.x - box_target.x
                        self.moving_box_origin_diff[1] = event.y - box_target.y
                        print(self.moving_box_origin_diff)
        else:
            if self.current_selected_box != None:
                self.current_selected_box.set_can_move(False)
                self.current_selected_box = None
            if self.current_selected_box_corner != None:
                self.moving_box_corner = False
                self.current_selected_box_corner = None
    

    def left_click_release_event(self, event):
        if event.y >= self.timeline.timeline_height-50:
            return
        if self.current_selected_box == None and self.current_selected_box_corner == None:
            return
        if not self.moving_box and not self.moving_box_corner:
            return

        if self.moving_box_corner and self.current_selected_box != None:
            corner_ref = None
            match self.current_selected_box_corner.type:
                case 'tl':
                    corner_ref = self.current_selected_box.border_corner_br
                case 'tr':
                    corner_ref = self.current_selected_box.border_corner_bl
                case 'bl':
                    corner_ref = self.current_selected_box.border_corner_tr
                case 'br':
                    corner_ref = self.current_selected_box.border_corner_tl
            release_x = event.x - self.moving_box_corner_origin_diff[0]
            release_y = event.y - self.moving_box_corner_origin_diff[1]
            new_x = min(release_x, corner_ref.x)
            new_y = min(release_y, corner_ref.y)
            new_width = max(release_x, corner_ref.x) - min(release_x, corner_ref.x)
            if new_width == 0:
                return
            new_height = max(release_y, corner_ref.y) - min(release_y, corner_ref.y)
            if new_height == 0:
                return
            self.current_selected_box.set_position(new_x, new_y)
            self.current_selected_box.set_scale(new_width, new_height)
            self.current_selected_box.draw()
            self.moving_box_corner = False
            print(f"new scale: {new_width}, {new_height}")
            return

        if self.moving_box:
            self.ghost_box = None
            self.win.get_canvas().delete(self.ghost_index)
            self.ghost_index = -1
            new_x = event.x - self.moving_box_origin_diff[0]
            new_y = event.y - self.moving_box_origin_diff[1]
            print(f"new position: {new_x}, {new_y}")
            self.current_selected_box.set_position(new_x, new_y)
            self.current_selected_box.draw()


    def left_click_hold_event(self, event):
        if event.y >= self.timeline.timeline_height-50:
            return
        if self.current_selected_box == None and self.current_selected_box_corner == None:
            return
        if not self.moving_box and not self.moving_box_corner:
            return

        if self.moving_box:
            if self.ghost_index != -1:
                self.win.get_canvas().delete(self.ghost_index)
            ghost_x = event.x - self.moving_box_origin_diff[0]
            ghost_y = event.y - self.moving_box_origin_diff[1]
            if self.ghost_box == None:
                self.ghost_box = self.current_selected_box.copy()
            self.ghost_box.x = ghost_x
            self.ghost_box.y = ghost_y
            self.ghost_box.can_move = False
            self.ghost_index = self.ghost_box.draw()

    
    def get_box_by_canvas_id(self, canvas_id):
        box_target = None
        for hb in self.boxes:
            if hb.box_id == canvas_id:
                box_target = hb 
                break
        return box_target


    def get_box_corner_by_canvas_id(self, box, ids):
        corner_target = None
        for canvas_id in ids:
            if box.border_corner_tl.id == canvas_id:
                corner_target = box.border_corner_tl
                break
            if box.border_corner_tr.id == canvas_id:
                corner_target = box.border_corner_tr
                break
            if box.border_corner_bl.id == canvas_id:
                corner_target = box.border_corner_bl
                break
            if box.border_corner_br.id == canvas_id:
                corner_target = box.border_corner_br
                break
        return corner_target 


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
        for box in self.boxes:
            box.draw()
    

    def jump_to_unintrusive(self, frame):
        self.timeline.current_index = frame
        if self.timeline.update_index_range():
            self.timeline.draw()