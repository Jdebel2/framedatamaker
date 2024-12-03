

class Flag():
    def __init__(self, box, type, animLen):
        self.box = box
        self.type = type
        self.frame_changes = []
        for i in range(animLen):
            self.frame_changes.append({})
        self.frame_changes[0]['enabled'] = False
    

    def update_position_change_at_frame(self, frame, n_position):
        self.frame_changes[frame]['position'] = n_position


    def update_scale_change_at_frame(self, frame, n_scale):
        self.frame_changes[frame]['scale'] = n_scale
    

    def update_is_enabled_change_at_frame(self, frame, is_enabled):
        self.frame_changes[frame]['enabled'] = is_enabled