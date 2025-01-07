import pygame
from ball import Ball

TILE_SIZE = 16

TELEPORT_PAIRS = {
    11: 12,
    21: 22,
    31: 32,
}

class Hero(pygame.sprite.Sprite):
    GRAVITY = 10
    MAX_FALL_SPEED = 16
    JUMP_SPEED = -64
    WALK_SPEED = 16
    ANIMATION_SPEED = 5

    def __init__(self, x, y, terrain_layer, path_layer, tmx_data):
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
        self.path_layer = path_layer
        self.tmx_data = tmx_data
        self.dy = 0
        self.dx = 0
        self.on_ground = False
        self.facing = "right"
        self.walk_frame = 0
        self.animation_counter = 0
        self.held_ball_color = None
        self.ball = None

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

    def check_teleport(self, tile_x, tile_y):
        tile_gid = self.terrain_layer.data[tile_y][tile_x]
        if tile_gid == 0:
            return None

        tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
        if tile_props:
            return tile_props.get("Teleport", None)
        return None

    def apply_teleport(self):
        tile_x = self.rect.centerx // TILE_SIZE
        tile_y = self.rect.bottom // TILE_SIZE

        teleport_id = self.check_teleport(tile_x, tile_y)
        if teleport_id and teleport_id in TELEPORT_PAIRS:
            destination_id = TELEPORT_PAIRS[teleport_id]
            for y in range(len(self.terrain_layer.data)):
                for x in range(len(self.terrain_layer.data[y])):
                    dest_gid = self.terrain_layer.data[y][x]
                    dest_props = self.tmx_data.get_tile_properties_by_gid(dest_gid)
                    if dest_props and dest_props.get("Teleport") == destination_id:
                        self.rect.topleft = (x * TILE_SIZE, (y + 1) * TILE_SIZE)
                        self.dy = 0
                        return

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
            current_top = self.rect.top
            next_top = current_top + self.dy

            current_tile_y = current_top // TILE_SIZE
            next_tile_y = next_top // TILE_SIZE

            collision_detected = False
            for tile_y in range(current_tile_y + 3, next_tile_y - 1, -1):  # Двигаемся вверх
                walk_status_top_left = self.can_walk(self.rect.left // TILE_SIZE, tile_y)
                walk_status_top_right = self.can_walk((self.rect.right - 1) // TILE_SIZE, tile_y)

                if walk_status_top_left == "Border" or walk_status_top_right == "Border":
                    self.rect.top = (tile_y + 1) * TILE_SIZE
                    self.dy = 0
                    collision_detected = True
                    break

            if collision_detected:
                break
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

    def check_ball_point(self):
        tile_x = self.rect.centerx // TILE_SIZE
        tile_y = self.rect.bottom // TILE_SIZE

        tile_gid = self.terrain_layer.data[tile_y][tile_x]
        if tile_gid == 0:
            return

        tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
        if tile_props and "BallColor" in tile_props:
            ball_color = tile_props["BallColor"]
            self.held_ball_color = ball_color
            self.ball = Ball(ball_color, self.rect)

    def handle_input(self, keys):
        if keys[pygame.K_DOWN]:
            self.check_ball_point()

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
        self.apply_teleport()
        self.apply_gravity()
        self.move(keys)
        self.jump(keys)
        self.handle_input(keys)
        self.update_sprite()

        if self.ball:
            self.ball.update(self.rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

        if self.ball:
            surface.blit(self.ball.image, self.ball.rect.topleft)

    def check_trajectory(self, path_data):
        tile_x = self.rect.centerx // TILE_SIZE
        tile_y = self.rect.centery // TILE_SIZE

        neighbours = [
            (tile_x, tile_y),
            (tile_x - 1, tile_y),
            (tile_x + 1, tile_y),
            (tile_x, tile_y - 1),
            (tile_x, tile_y + 1),
        ]

        matched_id = None
        neighbours_to_change = []

        for neighbour in neighbours:
            if neighbour in path_data:
                for obj_id, color in path_data[neighbour]:
                    if color == self.held_ball_color:
                        matched_id = obj_id
                        break
                    else:
                        neighbours_to_change.append(neighbour)


        # Преобразуем path_data в линейный список
        linear_path_data = [(obj_id, color, tile) for tile, objs in path_data.items() for obj_id, color in objs]

        def remove_consecutive(data_list, start_index, color, direction):
            indices_to_remove = []
            index = start_index
            while 0 <= index < len(data_list):
                obj_id, obj_color, tile = data_list[index]
                if obj_color == color:
                    indices_to_remove.append(index)
                    index += direction
                else:
                    break
            return indices_to_remove

        matched_index = next(
            (i for i, (obj_id, _, _) in enumerate(linear_path_data) if obj_id == matched_id),
            None,
        )

        deleted_ids = set()

        if matched_index is not None:
            left_indices = remove_consecutive(linear_path_data, matched_index - 1, self.held_ball_color, -1)
            right_indices = remove_consecutive(linear_path_data, matched_index + 1, self.held_ball_color, 1)
            all_indices_to_remove = set(left_indices + right_indices + [matched_index])

            if len(all_indices_to_remove) >= 2:
                for index in sorted(all_indices_to_remove, reverse=True):
                    obj_id, _, tile = linear_path_data[index]
                    path_data[tile] = [(id, color) for id, color in path_data[tile] if id != obj_id]
                    deleted_ids.add(obj_id)

                # print(f"Айди для удаления: {deleted_ids}")
                return deleted_ids
            else:
                if neighbours_to_change:
                    tile = neighbours_to_change[0]
                    for obj_id, color in path_data.get(tile, []):
                       return obj_id

        return set()
        # if neighbours_to_change:
        #     tile = neighbours_to_change[0]
        #     for obj_id, color in path_data.get(tile, []):
        #         return obj_id

