import pygame

class Hero(pygame.sprite.Sprite):
    TILE_SIZE = 16
    GRAVITY = 8
    MAX_FALL_SPEED = 8
    JUMP_SPEED = -80
    WALK_SPEED = 16

    def __init__(self, x, y, terrain_layer, tmx_data):
        super().__init__()
        # Создаем героя как синий квадрат 32x32
        self.image = pygame.Surface((self.TILE_SIZE * 2, self.TILE_SIZE * 2))
        self.image.fill((0, 0, 255))  # Синий цвет
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * self.TILE_SIZE, y * self.TILE_SIZE)
        self.terrain_layer = terrain_layer
        self.tmx_data = tmx_data
        self.dy = 0  # Вертикальная скорость
        self.dx = 0  # Горизонтальная скорость
        self.on_ground = False

    def can_walk(self, tile_x, tile_y):
        tile_x = int(tile_x)
        tile_y = int(tile_y)

        if tile_y < 0 or tile_x < 0 or tile_y >= len(self.terrain_layer.data) or tile_x >= len(self.terrain_layer.data[0]):
            return "Border"  # Обрабатываем выход за границы карты

        tile_gid = self.terrain_layer.data[tile_y][tile_x]
        if tile_gid == 0:
            return False

        tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
        if tile_props and tile_props.get("Border", False):
            return "Border"
        return tile_props and tile_props.get("HeroWalk", False)

    def apply_gravity(self):
        if not self.on_ground:
            self.dy = min(self.dy + self.GRAVITY, self.MAX_FALL_SPEED)

        new_bottom = self.rect.bottom + self.dy
        tile_x_left = self.rect.left // self.TILE_SIZE
        tile_x_right = (self.rect.right - 1) // self.TILE_SIZE
        tile_y = new_bottom // self.TILE_SIZE

        walk_status_left = self.can_walk(tile_x_left, tile_y)
        walk_status_right = self.can_walk(tile_x_right, tile_y)

        if walk_status_left == "Border" or walk_status_right == "Border":
            if self.dy > 0:  # Падение
                self.rect.bottom = (tile_y * self.TILE_SIZE) - 1
            elif self.dy < 0:  # Прыжок
                self.rect.top = (tile_y) * self.TILE_SIZE
            self.dy = 0
        elif walk_status_left or walk_status_right:
            self.rect.bottom = tile_y * self.TILE_SIZE
            self.dy = 0
            self.on_ground = True
        else:
            self.rect.bottom = new_bottom
            self.on_ground = False

    def move(self, keys):
        self.dx = 0

        if keys[pygame.K_LEFT]:
            self.dx = -self.WALK_SPEED
        if keys[pygame.K_RIGHT]:
            self.dx = self.WALK_SPEED

        new_left = self.rect.left + self.dx
        tile_x = (new_left // self.TILE_SIZE if self.dx < 0
                  else (new_left + self.rect.width - 1) // self.TILE_SIZE)
        tile_y_top = self.rect.top // self.TILE_SIZE
        tile_y_bottom = (self.rect.bottom - 1) // self.TILE_SIZE

        walk_status_top = self.can_walk(tile_x, tile_y_top)
        walk_status_bottom = self.can_walk(tile_x, tile_y_bottom)

        if walk_status_top == "Border" or walk_status_bottom == "Border":
            self.dx = 0

        self.rect.left += self.dx

        tile_x_left = self.rect.left // self.TILE_SIZE
        tile_x_right = (self.rect.right - 1) // self.TILE_SIZE
        tile_y = self.rect.bottom // self.TILE_SIZE

        self.on_ground = self.can_walk(tile_x_left, tile_y) or self.can_walk(tile_x_right, tile_y)

        if not self.on_ground:
            self.apply_gravity()

    def jump(self, keys):
        if keys[pygame.K_UP] and self.on_ground:
            self.dy = self.JUMP_SPEED
            self.on_ground = False

    def update(self, keys):
        self.move(keys)
        self.jump(keys)
        self.apply_gravity()
