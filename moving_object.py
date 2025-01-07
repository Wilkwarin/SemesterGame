import pygame
import random

TILE_SIZE = 16

class MovingObject(pygame.sprite.Sprite):
    next_id = 1

    def __init__(self, start_x, start_y, path_layer, tmx_data):
        super().__init__()
        self.id = MovingObject.next_id
        MovingObject.next_id += 1
        self.color = random.randint(1, 5)
        image_path = f"assets/images/balls/{self.color}.png"
        self.image = pygame.image.load(image_path).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (start_x * TILE_SIZE, start_y * TILE_SIZE)

        self.path_layer = path_layer
        self.tmx_data = tmx_data
        self.x, self.y = start_x * TILE_SIZE, start_y * TILE_SIZE
        self.direction = self.get_direction(int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))

        self.speed = 2

    def get_direction(self, x, y):
        if 0 <= y < len(self.path_layer.data) and 0 <= x < len(self.path_layer.data[0]):
            tile_gid = self.path_layer.data[y][x]
            tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
            if tile_props:
                return tile_props.get("Direction", None)
        return None

    def move(self):
        if self.direction is None or self.direction == 0:
            return

        if self.direction in [1, 5, 7]:
            self.y += self.speed
        elif self.direction in [2, 4]:
            self.x += self.speed
        elif self.direction in [3, 6]:
            self.x -= self.speed

        self.rect.topleft = (int(self.x), int(self.y))

        if self.check_for_exit():
            return "exit"

        if int(self.x) % TILE_SIZE == 0 and int(self.y) % TILE_SIZE == 0:
            self.direction = self.get_direction(int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))

    def check_for_exit(self):
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)

        if 0 <= tile_y < len(self.path_layer.data) and 0 <= tile_x < len(self.path_layer.data[0]):
            tile_gid = self.path_layer.data[tile_y][tile_x]
            tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)

            if tile_props and tile_props.get("Exit") == 1:
                return True
        return False

