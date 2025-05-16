import pygame

fps = 60
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

def convert_rel_to_abs(rel_px_w, rel_px_h):
        #Base Res = 480x270
        mult_x = screen_width/480
        mult_y =  screen_height/270
        abs_px_w = rel_px_w * mult_x
        abs_px_h = rel_px_h * mult_y
        return abs_px_w, abs_px_h

def convert_rel_pos_to_abs_pos(rel_pos_x, rel_pos_y):
        mult_x = screen_width/480
        mult_y =  screen_height/270
        abs_pos_x = rel_pos_x * mult_x
        abs_pos_y = rel_pos_y *mult_y
        return abs_pos_x, abs_pos_y

def convert_scale_to_abs(scale_x,scale_y):
        abs_pos_x = scale_x*screen_width
        abs_pos_y = scale_y*screen_height
        return abs_pos_x, abs_pos_y
def get_scale_mult():
        return screen_width/480