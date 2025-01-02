import pygame
import random

class MovingObject(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, path_layer, tmx_data, images_path):
        super().__init__()
        self.color = random.randint(1, 5)
        image_path = f"{images_path}/{self.color}.png"
        self.image = pygame.image.load(image_path).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (start_x * 16, start_y * 16)

        self.path_layer = path_layer
        self.tmx_data = tmx_data
        self.x, self.y = start_x, start_y
        self.direction = self.get_direction(self.x, self.y)

    def get_direction(self, x, y):
        tile_gid = self.path_layer.data[y][x]
        tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
        if tile_props:
            return tile_props.get("Direction", None)
        return None

    def move(self):
        direction = self.direction

        if direction == 0:
            return

        if direction == 1 or direction == 5 or direction == 7:
            self.y += 1
        elif direction == 2 or direction == 4:
            self.x += 1
        elif direction == 3 or direction == 6:
            self.x -= 1

        self.rect.topleft = (self.x * 16, self.y * 16)
        self.direction = self.get_direction(self.x, self.y)
