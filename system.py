import pygame

fps = 80
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
game_width = 480
game_height = 270
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
def get_player_loc(player_cords, camera_offset):
        player_x_diff = (player_cords[0]-(480/2)+16)*(screen_width/480)
        player_y_diff = (player_cords[1]-(270/2)+16)*(screen_height/270)
        cam_midpoint = camera_offset[0]-screen_width/2, camera_offset[1]-screen_height/2
        x = cam_midpoint[0]+player_x_diff
        y = cam_midpoint[1]+player_y_diff
        return (x,y)
