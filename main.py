import pygame
import pytmx
from moving_object import MovingObject
from hero import Hero

pygame.init()
screen = pygame.display.set_mode((800, 800))

TILE_SIZE = 16

tmx_data = pytmx.load_pygame("game/mapa.tmx")

path_layer = None
terrain_layer = None
object_layer = None
for layer in tmx_data.layers:
    if layer.name == "Path":
        path_layer = layer
    elif layer.name == "Terrain":
        terrain_layer = layer
    elif layer.name == "MovingObjects":
        object_layer = layer

if not path_layer or not terrain_layer or not object_layer:
    raise ValueError("Какой-то слой не найден!")

def draw_layer(layer):
    for y in range(tmx_data.height):
        for x in range(tmx_data.width):
            tile_gid = layer.data[y][x]
            if tile_gid != 0:
                tile_image = tmx_data.get_tile_image_by_gid(tile_gid)
                if tile_image:
                    screen.blit(tile_image, (x * TILE_SIZE, y * TILE_SIZE))

hero = Hero(42, 5, terrain_layer, path_layer, tmx_data)

moving_objects = []
start_positions = []
for obj in object_layer:
    if obj.type == "MovingObject":
        start_x = int(obj.x / TILE_SIZE)
        start_y = int(obj.y / TILE_SIZE)
        start_positions.append((start_x, start_y))
        moving_objects.append(MovingObject(start_x, start_y, path_layer, tmx_data))

steps_to_add_ball = 15 # если скорость = 2, шагов 15. Если скорость = 1, то шагов 30...
step_counter = 0
max_balls = 10

path_data = {}

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    draw_layer(terrain_layer)

    hero.update(keys)

    path_data.clear()

    new_moving_objects = []

    for moving_object in moving_objects:
        moving_object.move()

        tile_x = moving_object.rect.centerx // TILE_SIZE
        tile_y = moving_object.rect.centery // TILE_SIZE
        color = moving_object.color
        obj_id = moving_object.id

        if (tile_x, tile_y) not in path_data:
            path_data[(tile_x, tile_y)] = []
        path_data[(tile_x, tile_y)].append((obj_id, color))

        screen.blit(moving_object.image, moving_object.rect)

    step_counter += 1
    deleted_ids = []

    result = hero.check_trajectory(path_data)

    if isinstance(result, set):
        max_balls -= len(result)
        deleted_ids = result

    elif isinstance(result, int):
        neighbour_id = result
        for moving_object in moving_objects:
            if moving_object.id == neighbour_id:
                moving_object.color = hero.held_ball_color
                image_path = f"assets/images/balls/{moving_object.color}.png"
                moving_object.image = pygame.image.load(image_path).convert_alpha()
                break

    if step_counter >= steps_to_add_ball and len(moving_objects) < max_balls:
        start_x, start_y = start_positions[0]
        moving_objects.append(MovingObject(start_x, start_y, path_layer, tmx_data))
        step_counter = 0

    id_and_colour = []
    coords = []

    for obj in moving_objects:
        if obj.id not in deleted_ids:
            deletion_flag = 0
        else:
            deletion_flag = 1
        id_and_colour.append((obj, deletion_flag))
        coords.append((obj.rect.centerx, obj.rect.centery))

    id_and_colour = [entry for entry in id_and_colour if entry[1] == 0]

    for index, (obj, deletion_flag) in enumerate(id_and_colour):
        tile_x, tile_y = coords[index]
        obj.rect.centerx = tile_x
        obj.rect.centery = tile_y
        new_moving_objects.append(obj)

    moving_objects = new_moving_objects

    hero.draw(screen)

    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
