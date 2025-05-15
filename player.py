import pygame
import os, sys
class Player:
    def __init__(self, x, y, width = 32, height = 32, fps = 60):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.num_frames = 4
        self.frame_duration = fps/self.num_frames
        
        self.frame = 0

        # [0] = Up
        # [1] = Down
        # [2] = Right
        # [3] = Left
        self.direction = [False , False, True, False]
        self.action = "Idle"
    def update_anim(self, new_action):
        self.frame = 0
        if new_action == "Idle":
            self.num_frames = 4
        elif new_action == "Walk":
            self.num_frames = 6
        self.frame = 0
        self.frame_duration = 60/self.num_frames

    def get_direction(self):
        match self.direction:
            case [True, False, False, False]:
                return "Up", False
            case [False, True, False, False]:
                return "Sides", False
            case [False, False, True, False]:
                return "Down", False
            case [False, False, False, True]:
                return "Sides",True
    
    def draw(self, screen):
        if self.frame >= self.frame_duration*self.num_frames:
            self.frame = 0
        frame = pygame.image.load(os.path.join("Resources", "Animations","Player", self.action,self.get_direction()[0], str(int(self.frame//self.frame_duration))+".png"))
        self.frame += 1
        screen.blit(frame, (self.x, self.y))

