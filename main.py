import pygame, sys, os, player
from pytmx.util_pygame import load_pygame
pygame.init()

import system 

sys_info = system.System()

screen = pygame.display.set_mode((sys_info.screen_width, sys_info.screen_height),pygame.FULLSCREEN)
pygame.display.set_caption("Escape Room")

running = True
        
map_path = os.path.join("Map","CurrentMap", "map.tmx")
map_data = load_pygame(map_path)

import maploader
map = maploader.Map(map_data)
player = player.Player(50, 50, 50, 50)

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    player.draw(screen)
    pygame.time.Clock().tick(sys_info.fps)
    pygame.display.update()
    


pygame.quit()