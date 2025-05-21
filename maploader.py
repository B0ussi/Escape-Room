import pygame
from pytmx.util_pygame import load_pygame
import pytmx
import system as sys_info

class Tile(pygame.sprite.Sprite):
    _tile_cache = {}  # Add this to fix runtime error

    def __init__(self, scale, x, y, surf, groups, tile_width, tile_height):
        super().__init__(groups)
        scaled_width = int(tile_width * scale)
        scaled_height = int(tile_height * scale)
        cache_key = (id(surf), scaled_width, scaled_height)

        if cache_key in Tile._tile_cache:
            self.image = Tile._tile_cache[cache_key]
        else:
            scaled_image = pygame.transform.scale(surf.convert_alpha(), (scaled_width, scaled_height))
            Tile._tile_cache[cache_key] = scaled_image
            self.image = scaled_image

        # Save world position
        self.world_x = x * scaled_width
        self.world_y = y * scaled_height
        # # print("Tile: "+"("+str(self.world_x)+","+str(self.world_y)+")")
        self.rect = self.image.get_rect(topleft=(self.world_x, self.world_y))
class ImageObject(pygame.sprite.Sprite):
    _tile_cache = {}
    def __init__(self, scale, x, y, surf, groups, width, height):
        super().__init__(groups)
        scaled_width = int(width *scale)
        scaled_height = int(height * scale)
        cache_key = (id(surf), scaled_width, scaled_height)
        self.width = scaled_width
        self.height = scaled_height
        if cache_key in ImageObject._tile_cache:
            self.image = ImageObject._tile_cache[cache_key]
        else:
            scaled_image = pygame.transform.scale(surf.convert_alpha(), (scaled_width, scaled_height))
            ImageObject._tile_cache[cache_key] = scaled_image
            self.image = scaled_image

        self.world_x = round(x*scale)
        self.world_y = round(y*scale)
        # # print("OBJ: "+"("+str(self.world_x)+","+str(self.world_y)+")")
        self.rect = self.image.get_rect(topleft=(self.world_x,self.world_y))        

class Map:
    def __init__(self, data):
        self.collisions = []
        self.tmx_data = data
        self.sprite_group = pygame.sprite.Group()
        self.obj_group = pygame.sprite.Group()
        self.tiles = []
        self.offset = ()
        self.objs = []
        self._load_map()  
    def center_offset(self):
        self.offset[0] -= sys_info.screen_width/2
        self.offset[1] -= sys_info.screen_height/2


    def offset_from_tile(self,tile_x, tile_y):
        offset_x = tile_x*self.tmx_data.tilewidth*(sys_info.get_scale_mult()/1.25)
        # print("OFFSET:"+ str(offset_x-sys_info.screen_width))
        offset_y = tile_y*self.tmx_data.tileheight*(sys_info.get_scale_mult()/1.25)
        return ([offset_x,offset_y])
    
    def _load_map(self):
        tile_width = self.tmx_data.tilewidth
        tile_height = self.tmx_data.tileheight
        scale = sys_info.get_scale_mult()/1.25

        scaled_width = tile_width*scale
        scaled_height = tile_height*scale

        self.map_width = scaled_width*self.tmx_data.width
        self.map_height = scaled_height*self.tmx_data.height
        tiled_layers = {
            'Floor', 'Walls', 'UnlockableLadder', 'AnimatedTiles',
            'Objects1', 'Objects2', 'Jars', 'books',
            'tableDetails1', 'appliances', 'tableDetails2'
        }
        object_layers = {"Borders", "Stone", "Wood", "doorObjs", "bookshelfSensors","Test"}
        
        self.offset = self.offset_from_tile(66,32)
        self.center_offset()
        for layer in self.tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name in tiled_layers:
                for x, y, surf in layer.tiles():

                    tile = Tile(scale, x, y, surf, self.sprite_group, tile_width, tile_height)
                    self.tiles.append(tile)
            elif isinstance(layer, pytmx.TiledObjectGroup) and layer.name in object_layers:
                # # # print(layer)
                # # # print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
                for obj in layer:
                    x = obj.x
                    y = obj.y

                    # Scale width and height properly
                    obj_width = obj.width * scale
                    obj_height = obj.height * scale

                    if obj.name == "Test":
                        pass
                        # print(f"OBJ X: {round(x*scale)}")

                    # Handle tile image objects
                    if hasattr(obj, "image") and obj.image:
                        img_obj = ImageObject(scale, x, y, obj.image, self.obj_group, tile_width, tile_height)
                        img_obj.width = obj_width
                        img_obj.height = obj_height
                        img_obj.world_x = round(x * scale)
                        img_obj.world_y = round(y * scale)
                        self.objs.append(img_obj)
                        if obj.properties.get("collision") is True:
                            self.collisions.append(img_obj)
                            # print("ADDED:", obj.name)

                    # Also support invisible rectangles with no image
                    elif obj.properties.get("collision") is True:
                        # Create a dummy surface for collision if needed
                        dummy_surf = pygame.Surface((obj_width, obj_height), pygame.SRCALPHA)
                        dummy_surf.fill((255, 0, 0, 100))  # Optional: semi-transparent red box for debugging
                        rect_obj = ImageObject(scale, x, y, dummy_surf, self.obj_group, obj.width, obj.height)
                        rect_obj.width = obj_width
                        rect_obj.height = obj_height
                        rect_obj.world_x = round(x * scale)
                        rect_obj.world_y = round(y * scale)
                        self.objs.append(rect_obj)
                        self.collisions.append(rect_obj)

    def isColliding(self, obj, plr):
        obj_x, obj_y, obj_width, obj_height = obj
        plr_x, plr_y, plr_dimmensions = plr
        plr_width = plr_dimmensions[0]

        plr_height = 10  # Assuming square player; if not, adjust accordingly
        # print("ran")
        # print("PLAYER WIDTH: "+str(plr_width), "OBJECT WIDTH: "+str(obj_width))
        # print("PLAYER HEIGHT: "+str(plr_height), "OBJECT_HEIGHT: "+str(obj_height))
        if (plr_x < obj_x + obj_width and
            plr_x + plr_width > obj_x and
            plr_y < obj_y + obj_height and
            plr_y + plr_height > obj_y):
            # print("COLLISION")
            # print(plr_x,obj_x)
            # print(plr_y,obj_y)
            return True
        # print("notta")
        # print(plr_x,obj_x)
        # print(plr_y,obj_y)
        return False


    def draw_collisions(self, camera_offset, screen):
        for obj in self.collisions:
            rect = pygame.Rect(obj.world_x - camera_offset[0], obj.world_y - camera_offset[1], obj.width, obj.height)
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)  # Red outline

    def draw_map(self, camera_offset, screen):
        for tile in self.tiles:
            tile.rect.topleft = (tile.world_x - camera_offset[0], tile.world_y - camera_offset[1])
        self.sprite_group.draw(screen)
    def draw_objs(self, camera_offset, screen):
        for obj in self.objs:
            obj.rect.topleft = (obj.world_x - camera_offset[0], obj.world_y-camera_offset[1])
        self.obj_group.draw(screen)


