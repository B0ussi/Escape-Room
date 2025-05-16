import pygame, sys, os
from pytmx.util_pygame import load_pygame
import system as sys_info
class Tile(pygame.sprite.Sprite):
    def __init__(self, mult, x, y, surf, groups, tile_width, tile_height):
        super().__init__(groups)
        mult = mult/1.5
        surf = surf.convert_alpha()
        self.image = pygame.transform.scale(surf, (tile_width * mult, tile_height * mult))
        self.rect = self.image.get_rect(topleft=(x * tile_width * mult, y * tile_height * mult))



class Map:
    def __init__(self, data):
        self.tmx_data = data
        self.sprite_group = pygame.sprite.Group()
    def run(self):
        tile_width = self.tmx_data.tilewidth
        tile_height = self.tmx_data.tileheight
        scale = sys_info.get_scale_mult()

        for layer in self.tmx_data.layers:
            if layer.name in ('Background', "Floor", "Walls", "UnlockableLadder", "AnimatedTiles", "Objects1", "Objects2", "Stone", "Wood", "Jars", "books", "tableDetails1", "appliances", "tableDetails2"):
                for x, y, surf in layer.tiles():
                    Tile(scale, x, y, surf, self.sprite_group, tile_width, tile_height)
