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
clock = pygame.time.Clock()
import maploader
map = maploader.Map(map_data)
player = player.Player(240-16, 135-16,map, 32, 32, sys_info.fps)

while running:
    screen.fill((17, 3, 32)) 
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    player.update_input()
    player.delta_movement()
    map.draw_map(map.offset,screen)
    map.draw_objs(map.offset, screen)
    map.draw_collisions(map.offset,screen)
    player.draw(screen)


    pygame.display.update()
     # RGB black background
    print(f"FPS: {clock.get_fps():.2f}")
    clock.tick(sys_info.fps)


pygame.quit()