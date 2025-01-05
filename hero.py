import pygame

TILE_SIZE = 16

class Hero(pygame.sprite.Sprite):
    GRAVITY = 10
    MAX_FALL_SPEED = 16
    JUMP_SPEED = -64
    WALK_SPEED = 16
    ANIMATION_SPEED = 5

    def __init__(self, x, y, terrain_layer, tmx_data):
        super().__init__()

        self.sprites = {
            "jump_left": pygame.image.load("assets/images/girl/Rosette_Att_Jump1_L.png"),
            "jump_right": pygame.image.load("assets/images/girl/Rosette_Att_Jump1_R.png"),
            "stand_left": pygame.image.load("assets/images/girl/Rosette_Stand_L.png"),
            "stand_right": pygame.image.load("assets/images/girl/Rosette_Stand_R.png"),
            "walk_left": self.load_animation("assets/images/girl/Rosette_Att_Walk_Anim_L.png"),
            "walk_right": self.load_animation("assets/images/girl/Rosette_Att_Walk_Anim_R.png"),
        }

        self.image = self.sprites["stand_right"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

        self.terrain_layer = terrain_layer
        self.tmx_data = tmx_data
        self.dy = 0
        self.dx = 0
        self.on_ground = False
        self.facing = "right"
        self.walk_frame = 0
        self.animation_counter = 0

    @staticmethod
    def load_animation(image_path):
        sheet = pygame.image.load(image_path)
        frame_width = sheet.get_width() // 4
        frames = [sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, sheet.get_height())) for i in range(4)]
        return frames

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
            self.facing = "left"
        if keys[pygame.K_RIGHT]:
            self.dx = self.WALK_SPEED
            self.facing = "right"

        new_left = self.rect.left + self.dx
        tile_x_left = new_left // TILE_SIZE
        max_tile_x = len(self.terrain_layer.data[0]) - 1
        tile_x_left = max(0, tile_x_left)
        tile_x_right = (self.rect.right + self.dx - 1) // TILE_SIZE
        tile_x_right = min(max_tile_x, tile_x_right)

        max_tile_y = len(self.terrain_layer.data) - 1
        tile_y_bottom = (self.rect.bottom - 1) // TILE_SIZE
        tile_y_bottom = min(max(0, tile_y_bottom), max_tile_y)
        tile_y_top = self.rect.top // TILE_SIZE
        tile_y_top = min(max(0, tile_y_top), max_tile_y)

        # sverhu
        while self.dy < 0:
            next_top = self.rect.top + self.dy
            tile_y_top = (next_top // TILE_SIZE) + 1

            walk_status_top_left = self.can_walk(self.rect.left // TILE_SIZE, tile_y_top)
            walk_status_top_right = self.can_walk((self.rect.right - 1) // TILE_SIZE, tile_y_top)

            if (walk_status_top_left == "Border" or walk_status_top_right == "Border"
                    or walk_status_top_left == "HeroWalk" or walk_status_top_right == "HeroWalk"):
                self.rect.top = (tile_y_top + 1) * TILE_SIZE
                self.dy = 0
                break
            else:
                break

        # snizu
        walk_status_bottom_left = self.can_walk(self.rect.left // TILE_SIZE, tile_y_bottom)
        walk_status_bottom_right = self.can_walk((self.rect.right - 1) // TILE_SIZE, tile_y_bottom)

        if (((walk_status_bottom_left == "HeroWalk" or walk_status_bottom_right == "HeroWalk")
                or (walk_status_bottom_left == "Border" or walk_status_bottom_right == "Border"))
                and self.dy > 0):
            self.rect.bottom = tile_y_bottom * TILE_SIZE
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

    def update_sprite(self):
        if self.dy != 0:
            self.image = self.sprites["jump_left"] if self.facing == "left" else self.sprites["jump_right"]
        elif self.dx == 0:
            self.image = self.sprites["stand_left"] if self.facing == "left" else self.sprites["stand_right"]
        else:
            frames = self.sprites["walk_left"] if self.facing == "left" else self.sprites["walk_right"]

            self.animation_counter += 1
            if self.animation_counter >= self.ANIMATION_SPEED:
                self.animation_counter = 0
                self.walk_frame = (self.walk_frame + 1) % len(frames)
            self.image = frames[self.walk_frame]

    def update(self, keys):
        self.apply_gravity()
        self.move(keys)
        self.jump(keys)
        self.update_sprite()