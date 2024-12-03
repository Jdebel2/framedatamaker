

class Flag():
    def __init__(self, box, type, animLen):
        self.box = box
        self.type = type
        self.frame_changes = []
        for i in range(animLen):
            self.frame_changes.append({})
        self.frame_changes[0]['enabled'] = False
    

    def update_position_change_at_frame(self, frame, n_position, origin_point_position):
        self.frame_changes[frame]['editor_position'] = n_position
        relative_x = max(n_position[0], origin_point_position[0]) - min(n_position[0], origin_point_position[0])
        relative_y = max(n_position[1], origin_point_position[1]) - min(n_position[1], origin_point_position[1])
        self.frame_changes[frame]['position'] = [relative_x, relative_y]


    def recalculate_position_from_origin_point(self, frame, origin_point_position):
        n_position = self.frame_changes[frame]['editor_position']
        relative_x = max(n_position[0], origin_point_position[0]) - min(n_position[0], origin_point_position[0])
        relative_y = max(n_position[1], origin_point_position[1]) - min(n_position[1], origin_point_position[1])
        self.frame_changes[frame]['position'] = [relative_x, relative_y]


    def update_scale_change_at_frame(self, frame, n_scale):
        self.frame_changes[frame]['scale'] = n_scale
    

    def update_is_enabled_change_at_frame(self, frame, is_enabled):
        self.frame_changes[frame]['enabled'] = is_enabled