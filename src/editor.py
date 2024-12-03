from animation import Animation
from timeline import Timeline
from graphics import FDMButton, ButtonFunction
from box import Hitbox, Hurtbox
from flag import Flag
from tkinter import Label
from origin_point import OriginPoint

class Editor():
    def __init__(self, win):
        self.is_editor_running = False
        self.animation = Animation(win)
        self.timeline = Timeline(self, win)
        self.win = win
        self.boxes = []
        self.flags = []
        self.origin_point = OriginPoint(20, 120, win)
        self.create_mode = 'hitbox'
        self.hitbox_modify_mode = 'create'
        self.adjust_mode = 'all'
        self.switch_btn = None
        self.moving_box = False
        self.moving_box_corner = False
        self.moving_origin_point = False
        self.moving_origin_point_diff = [0,0]
        self.moving_box_corner_origin_diff = [0,0]
        self.moving_box_origin_diff = [0,0]
        self.current_selected_box = None
        self.current_selected_box_corner = None
        self.ghost_index = -1
        self.ghost_box = None
        self.left_click_label = Label(self.win.get_root(), text=f'Left Click - Hitbox Adjust Properties: All', foreground='white', background='#000000')
        self.right_click_label = Label(self.win.get_root(), text=f'Right Click - Hitbox Modify Mode: Create', foreground='white', background='#000000')
        self.image_file_path = ""


    def load_data(self, spritesheet, path):
        self.animation.load_data(spritesheet, path)
        self.timeline.load_data(self.animation)
        self.win.get_canvas().bind("<Button-1>", self.left_click_event)
        self.win.get_canvas().bind("<ButtonRelease-1>", self.left_click_release_event)
        self.win.get_canvas().bind("<B1-Motion>", self.left_click_hold_event)
        self.win.get_canvas().bind("<Button-2>", self.right_click_event)
        self.win.get_canvas().bind("<Button-3>", self.right_click_event)
        self.win.get_canvas().bind("<Key>", self.key_press_event)
        self.switch_btn = FDMButton("Create Hitbox", 20, 40, 12, 1, ButtonFunction.SWITCH_BOX_TYPE, self.win, self)
        self.switch_btn.draw()
        self.origin_point.draw()
        self.left_click_label_id = self.win.draw_text(300, 20, self.left_click_label)
        self.right_click_label_id = self.win.draw_text(300, 40, self.right_click_label)
        self.is_editor_running = True


    def key_press_event(self, event):
        if event.char == 'q':
            self.adjust_mode = 'all'
            self.left_click_label.configure(text='Left Click - Hitbox Adjust Properties: All')
            print('Adjust mode set: all')
        elif event.char == 'w':
            self.adjust_mode = 'position'
            self.left_click_label.configure(text='Left Click - Hitbox Adjust Properties: Position')
            print('Adjust mode set: position')
        elif event.char == 'e':
            self.adjust_mode = 'scale'
            self.left_click_label.configure(text='Left Click - Hitbox Adjust Properties: Scale')
            print('Adjust mode set: scale')
        elif event.char == 'r':
            self.adjust_mode = 'origin_point'
            self.moving_origin_point = not self.moving_origin_point
            self.moving_origin_point_diff[0] = 3
            self.moving_origin_point_diff[1] = 3
            self.left_click_label.configure(text='Left Click - Modify Origin Point Position')
            print('Adjust mode set: origin_point')
        elif event.char == 'a':
            self.hitbox_modify_mode = 'create'
            self.right_click_label.configure(text='Right Click - Hitbox Modify Mode: Create')
            print('Adjust hitbox modify mode set: create')
        elif event.char == 's':
            self.hitbox_modify_mode = 'disable'
            self.right_click_label.configure(text='Right Click - Hitbox Modify Mode: Disable')
            print('Adjust hitbox modify mode set: disable')
        elif event.char == 'd':
            self.hitbox_modify_mode = 'delete'
            self.right_click_label.configure(text='Right Click - Hitbox Modify Mode: Delete')
            print('Adjust hitbox modify mode set: delete')
        elif event.char == 'p':
            for flag in self.flags:
                print(flag.type)
                print(flag.frame_changes)


    def right_click_event(self, event):
        if event.y < self.timeline.timeline_height-50:
            if self.hitbox_modify_mode == 'create':
                n_box = None
                match self.create_mode:
                    case 'hitbox':
                        n_box = Hitbox(event.x,event.y, 50, 50, self.win)
                    case 'hurtbox':
                        n_box = Hurtbox(event.x,event.y, 50, 50, self.win)
                if n_box != None:
                    self.boxes.append(n_box)
                    self.flags.append(Flag(n_box, self.create_mode, len(self.animation.sprites)))
                    n_box.draw()
                    return
                raise Exception("Error - box object not added")
            elif self.hitbox_modify_mode == 'disable':
                items = self.win.get_canvas().find_overlapping(event.x-1,event.y-1, event.x+1, event.y+1)
                if len(items) != 0:
                    target = items[-1]
                    box_target = self.get_box_by_canvas_id(target)
                    if box_target != None:
                        if box_target.is_enabled:
                            box_target.disable_self()
                        else:
                            box_target.enable_self()
                        for flag in self.flags:
                            if flag.box == box_target:
                                flag.update_is_enabled_change_at_frame(self.timeline.current_index, box_target.is_enabled)
                                return
            elif self.hitbox_modify_mode == 'delete':
                items = self.win.get_canvas().find_overlapping(event.x-1,event.y-1, event.x+1, event.y+1)
                if len(items) != 0:
                    target = items[-1]
                    box_target = self.get_box_by_canvas_id(target)
                    if box_target != None:
                        for flag in self.flags:
                            if flag.box == box_target:
                                self.flags.remove(flag)
                                break
                        self.boxes.remove(box_target)
                        box_target.delete_self()
    

    def left_click_event(self, event):
        if event.y >= self.timeline.timeline_height-50:
            return
        self.origin_point.draw()
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
        if self.adjust_mode == 'origin_point' and self.moving_origin_point:
            new_x = event.x - self.moving_origin_point_diff[0]
            new_y = event.y - self.moving_origin_point_diff[1]
            print(f"new origin point position: {new_x}, {new_y}")
            self.origin_point.set_position(new_x, new_y)
            self.origin_point.draw()
            for flag in self.flags:
                for frame in range(len(flag.frame_changes)):
                    frame_ref = flag.frame_changes[frame]
                    if 'position' in frame_ref:
                        flag.recalculate_position_from_origin_point(frame, [self.origin_point.x, self.origin_point.y])
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
            for flag in self.flags:
                if flag.box == self.current_selected_box:
                    flag.update_position_change_at_frame(self.timeline.current_index, [new_x, new_y], [self.origin_point.x, self.origin_point.y])
                    flag.update_scale_change_at_frame(self.timeline.current_index, [new_width, new_height])
                    flag.update_is_enabled_change_at_frame(self.timeline.current_index, self.current_selected_box.is_enabled)
                    return
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
            for flag in self.flags:
                if flag.box == self.current_selected_box:
                    flag.update_position_change_at_frame(self.timeline.current_index, [new_x, new_y], [self.origin_point.x, self.origin_point.y])
                    flag.update_is_enabled_change_at_frame(self.timeline.current_index, self.current_selected_box.is_enabled)
                    return


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
        for flag in self.flags:
            if 'editor_position' in flag.frame_changes[frame]:
                change = flag.frame_changes[frame]['editor_position']
                flag.box.set_position(change[0], change[1])
            if 'scale' in flag.frame_changes[frame]:
                change = flag.frame_changes[frame]['scale']
                flag.box.set_scale(change[0], change[1])
            if 'enabled' in flag.frame_changes[frame]:
                change = flag.frame_changes[frame]['enabled']
                if change:
                    flag.box.enable_self()
                else:
                    flag.box.disable_self()
        for box in self.boxes:
            box.draw()
    

    def jump_to_unintrusive(self, frame):
        self.timeline.current_index = frame
        if self.timeline.update_index_range():
            self.timeline.draw()
    

    def create_box_on_load(self, x, y, type):
        n_box = None
        match type:
            case 'hitbox':
                n_box = Hitbox(x,y, 50, 50, self.win)
            case 'hurtbox':
                n_box = Hurtbox(x,y, 50, 50, self.win)
        if n_box != None:
            self.boxes.append(n_box)
            n_flag = Flag(n_box, self.create_mode, len(self.animation.sprites))
            self.flags.append(n_flag)
            return n_box, n_flag
        raise Exception("Error - box object not added")

    def get_flag_from_box(self, box):
        for flag in self.flags:
            if flag.box == box:
                return flag
        return None