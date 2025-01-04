import pygame

class Hero(pygame.sprite.Sprite):
    TILE_SIZE = 16
    GRAVITY = 10
    MAX_FALL_SPEED = 16
    JUMP_SPEED = -64
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
        self.dy = 0
        self.dx = 0
        self.on_ground = False

    def can_walk(self, tile_x, tile_y):
        tile_x = int(tile_x)
        tile_y = int(tile_y)

        tile_gid = self.terrain_layer.data[tile_y][tile_x]
        if tile_gid == 0:
            return False

        tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
        if tile_props:
            if tile_props.get("Border", False):
                return "Border"
            if tile_props.get("HeroWalk", False):
                return "HeroWalk"
        return False

    def apply_gravity(self):
        if not self.on_ground:
            self.dy = min(self.dy + self.GRAVITY, self.MAX_FALL_SPEED)
            self.rect.bottom += self.dy

    def move(self, keys):
        self.dx = 0
        if keys[pygame.K_LEFT]:
            self.dx = -self.WALK_SPEED
        if keys[pygame.K_RIGHT]:
            self.dx = self.WALK_SPEED

        new_left = self.rect.left + self.dx
        tile_x_left = new_left // self.TILE_SIZE
        max_tile_x = len(self.terrain_layer.data[0]) - 1
        tile_x_left = max(0, tile_x_left)
        tile_x_right = (self.rect.right + self.dx - 1) // self.TILE_SIZE
        tile_x_right = min(max_tile_x, tile_x_right)

        max_tile_y = len(self.terrain_layer.data) - 1
        tile_y_bottom = (self.rect.bottom - 1) // self.TILE_SIZE
        tile_y_bottom = min(max(0, tile_y_bottom), max_tile_y)
        tile_y_top = self.rect.top // self.TILE_SIZE
        tile_y_top = min(max(0, tile_y_top), max_tile_y)

        # sverhu
        walk_status_top_left = self.can_walk(self.rect.left // self.TILE_SIZE, tile_y_top)
        walk_status_top_right = self.can_walk((self.rect.right - 1) // self.TILE_SIZE, tile_y_top)

        if (walk_status_top_left == "Border" or walk_status_top_right == "Border") and self.dy < 0:
            self.rect.top = tile_y_top * self.TILE_SIZE
            self.dy = 0

        # snizu
        walk_status_bottom_left = self.can_walk(self.rect.left // self.TILE_SIZE, tile_y_bottom)
        walk_status_bottom_right = self.can_walk((self.rect.right - 1) // self.TILE_SIZE, tile_y_bottom)

        if (((walk_status_bottom_left == "HeroWalk" or walk_status_bottom_right == "HeroWalk")
                or (walk_status_bottom_left == "Border" or walk_status_bottom_right == "Border"))
                and self.dy > 0):
            self.rect.bottom = tile_y_bottom * self.TILE_SIZE
            self.dy = 0
            self.on_ground = True

        if not (walk_status_bottom_left or walk_status_bottom_right):
            self.on_ground = False

        # sleva
        walk_status_left_bottom = (self.can_walk(tile_x_left, tile_y_bottom) if 0 <= tile_x_left <= max_tile_x and 0 <= tile_y_bottom <= max_tile_y else "Border")
        walk_status_left_top = (self.can_walk(tile_x_left, tile_y_top) if 0 <= tile_x_left <= max_tile_x and 0 <= tile_y_top <= max_tile_y else "Border")

        if self.dx < 0 and (walk_status_left_bottom == "Border" or walk_status_left_top == "Border"):
            self.dx = 0

        # sprava
        walk_status_right_bottom = (self.can_walk(tile_x_right, tile_y_bottom) if 0 <= tile_x_right <= max_tile_x and 0 <= tile_y_bottom <= max_tile_y else "Border")
        walk_status_right_top = (self.can_walk(tile_x_right, tile_y_top) if 0 <= tile_x_right <= max_tile_x and 0 <= tile_y_top <= max_tile_y else "Border")

        if self.dx > 0 and (walk_status_right_bottom == "Border" or walk_status_right_top == "Border"):
            self.dx = 0

        self.rect.left += self.dx

    def jump(self, keys):
        if keys[pygame.K_UP] and self.on_ground:
            self.dy = self.JUMP_SPEED
            self.on_ground = False

    def update(self, keys):
        self.apply_gravity()
        self.move(keys)
        self.jump(keys)