import pygame
from pytmx.util_pygame import load_pygame
import system as sys_info

class Tile(pygame.sprite.Sprite):
    _tile_cache = {}

    def __init__(self, scale, x, y, surf, groups, tile_width, tile_height):
        super().__init__(groups)
        scale = scale/1.25
        # Calculate target dimensions as integers
        scaled_width = int(tile_width * scale)
        scaled_height = int(tile_height * scale)

        # Cache key based on the original surface and scale
        cache_key = (id(surf), scaled_width, scaled_height)

        if cache_key in Tile._tile_cache:
            self.image = Tile._tile_cache[cache_key]
        else:
            # Scale and cache the tile surface
            scaled_image = pygame.transform.scale(surf.convert_alpha(), (scaled_width, scaled_height))
            Tile._tile_cache[cache_key] = scaled_image
            self.image = scaled_image

        # Set integer-aligned rect
        self.rect = self.image.get_rect(topleft=(x * scaled_width, y * scaled_height))


class Map:
    def __init__(self, data):
        self.tmx_data = data
        self.sprite_group = pygame.sprite.Group()

    def run(self):
        tile_width = self.tmx_data.tilewidth
        tile_height = self.tmx_data.tileheight
        scale = sys_info.get_scale_mult()

        included_layers = {
            'Background', 'Floor', 'Walls', 'UnlockableLadder', 'AnimatedTiles',
            'Objects1', 'Objects2', 'Stone', 'Wood', 'Jars', 'books',
            'tableDetails1', 'appliances', 'tableDetails2'
        }

        for layer in self.tmx_data.layers:
            if layer.name in included_layers:
                for x, y, surf in layer.tiles():
                    Tile(scale, x, y, surf, self.sprite_group, tile_width, tile_height)
