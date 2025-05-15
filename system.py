import pygame
class System:
    def __init__(self, fps = 60):
        self.fps = fps
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
