import pygame
import os, sys
import system as sys_info


class Player:
    def __init__(self, x, y, map, width = 32, height = 32, fps = 60):
        self.x = x
        self.y = y
        print(sys_info.get_player_loc((x,y),map.offset))
        self.width = width
        self.height = height
        self.num_frames = 4
        self.frame_duration = fps/self.num_frames
        self.frame = 0
        self.movement_speed = 10
        self.last_dir = "Down", False
        self.exceeding_y = False
        self.exceeding_x = False
        self.map = map
        # [0] = Up
        # [1] = Down
        # [2] = Right
        # [3] = Left
        self.direction = [False , False, True, False]
        self.action = "Idle"
    def update_anim(self, new_action):
        if new_action == "Idle":
            self.num_frames = 4
            self.action = "Idle"
        elif new_action == "Walk":
            self.num_frames = 6
            self.action = "Walk"
        self.frame = 0
        self.frame_duration = 60/self.num_frames

    def get_direction(self):
        if self.direction[1] == True:
            self.last_dir = 'Sides', True
            return "Sides", True
        elif self.direction[3] == True:
            self.last_dir = 'Sides', False
            return "Sides", False
        elif self.direction[0] == True:
            self.last_dir = 'Up', False
            return "Up", False
        elif self.direction[2] == True:
            self.last_dir = 'Down', False
            return "Down", False
        else:
            return self.last_dir
        
    def check_run(self):
        if self.action !="Walk":
            self.update_anim("Walk")
    def check_idle(self):
        if self.direction == [False,False,False,False] and self.action!="Idle":
            self.update_anim("Idle")
    def update_input(self):
        keys = pygame.key.get_pressed()
        
        self.direction = [False, False, False, False] 

        if keys[pygame.K_w]:
            self.direction[0] = True
        if keys[pygame.K_s]:
            self.direction[2] = True
        if keys[pygame.K_d]:
            self.direction[1] = True
        if keys[pygame.K_a]:
            self.direction[3] = True

        if self.direction != [False, False, False, False]:
            self.check_run()
        else:
            self.check_idle()
    def update_exceeding(self):
        positions = []
        atts = []
        if .75 < self.x/sys_info.game_width:
            self.exceeding_x = True
            positions.append("x")
            atts.append("greater")
        elif .25 > self.x/sys_info.game_width:
            self.exceeding_x = True
            positions.append("x")
            atts.append("less")
        else:
            self.exceeding_x = False
        if .75 < self.y/sys_info.game_height:
            self.exceeding_y = True
            positions.append("y")
            atts.append("greater")
        elif .25 > self.y/sys_info.game_height:
            self.exceeding_y = True
            positions.append("y")
            atts.append("less")
        else:
            self.exceeding_y = False
        return (positions, atts)

    def map_offset_change(self, delta_x, delta_y):
        self.map.offset[0] += delta_x*sys_info.screen_width/sys_info.game_width
    
        self.map.offset[1] += delta_y*sys_info.screen_height/sys_info.game_height

    def delta_movement(self):
        info = self.update_exceeding()
        delta_x = 0
        delta_y = 0
        canrun = True

        for obj in self.map.collisions:
            player_loc = sys_info.get_player_loc((self.x,self.y),self.map.offset)

            obj_world_x = obj.x*sys_info.get_scale_mult()
            obj_world_y = obj.y*sys_info.get_scale_mult()
            obj_width = self.map.tmx_data.tilewidth
            obj_height = self.map.tmx_data.tileheight

            param = [(obj_world_x,obj_world_y,obj_width,obj_height),(player_loc[0], player_loc[1],player_loc[0]+16)]
            if self.map.isColliding(param[0],param[1]):
                canrun = False
        if canrun:
            if self.action == "Walk":
                if self.direction[0] == True:
                    delta_y-=self.movement_speed/10
                if self.direction[1] == True:
                    delta_x+=self.movement_speed/10
                if self.direction[2] == True:
                    delta_y+= self.movement_speed/10
                if self.direction[3] == True:
                    delta_x-= self.movement_speed/10
            for i,pos in enumerate(info[0]):
                sync_att = info[1][i]
                if pos =="x":
                    if sync_att =="greater" and delta_x<= 0:
                        self.x += delta_x
                    elif sync_att =="less" and delta_x >= 0:
                        self.x += delta_x
                    else:
                        self.map_offset_change(delta_x, 0)
                elif pos == "y":
                    if sync_att =="greater" and delta_y <= 0:
                        self.y += delta_y
                    elif sync_att == "less" and delta_y >= 0:
                        self.y += delta_y
                    else:
                        self.map_offset_change(0, delta_y)
            if not self.exceeding_x:
                self.x += delta_x
            if not self.exceeding_y:
                self.y += delta_y

                    

    def draw(self, screen):
        if self.frame >= self.frame_duration*self.num_frames:
            self.frame = 0
        frame = pygame.image.load(os.path.join("Resources", "Animations","Player", self.action,self.get_direction()[0], str(int(self.frame//self.frame_duration))+".png"))
        scaled_frame = pygame.transform.scale(frame,(sys_info.convert_rel_to_abs(self.width, self.height)))
        flipped_frame = pygame.transform.flip(scaled_frame, self.get_direction()[1],False)
        self.frame += 1
        screen.blit(flipped_frame, sys_info.convert_rel_pos_to_abs_pos(self.x,self.y))
