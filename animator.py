class Animation:
    def __init__(self, anim_type, obj_frames = False):
        self.anim_type = anim_type
        if anim_type == "char":
            self.walk_length = 6
            self.idle_length = 4

        elif anim_type == "obj":
            self.frames = obj_frames
        self.num_frame = 0

    def run_frame(self):
        pass
    
    