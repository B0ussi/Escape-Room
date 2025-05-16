import pygame, os
from pytmx.util_pygame import load_pygame

pygame.init()

import system as sys_info 

screen = pygame.display.set_mode((sys_info.screen_width, sys_info.screen_height),pygame.FULLSCREEN)
pygame.display.set_caption("Escape Room")
import player
running = True


map_path = os.path.join("Map","CurrentMap", "map.tmx")
map_data = load_pygame(map_path)

import maploader
map = maploader.Map(map_data)
map.run()

player = player.Player(240-16, 135-16, 32, 32)

while running:
    screen.fill((0, 0, 0)) 
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    map.sprite_group.draw(screen)
    player.update_input()
    player.delta_movement()
    player.draw(screen)

    pygame.display.update()
     # RGB black background

    pygame.time.Clock().tick(sys_info.fps)


pygame.quit()