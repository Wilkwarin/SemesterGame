import pygame
import pytmx
from moving_object import MovingObject
from hero import Hero

pygame.init()
screen = pygame.display.set_mode((800, 800))

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
                    screen.blit(tile_image, (x * 16, y * 16))

hero = Hero(42, 3, terrain_layer, tmx_data)

moving_objects = []
start_positions = []
for obj in object_layer:
    if obj.type == "MovingObject":
        start_x = int(obj.x / 16)
        start_y = int(obj.y / 16)
        start_positions.append((start_x, start_y))
        moving_objects.append(MovingObject(start_x, start_y, path_layer, tmx_data, "assets/images/balls"))

steps_to_add_ball = 2
max_balls = 40
step_counter = 0

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    draw_layer(terrain_layer)

    hero.update(keys)
    screen.blit(hero.image, hero.rect)

    # for moving_object in moving_objects:
    #     moving_object.move()
    #     screen.blit(moving_object.image, moving_object.rect)
    #
    # step_counter += 1
    # if step_counter >= steps_to_add_ball and len(moving_objects) < max_balls:
    #     start_x, start_y = start_positions[0]
    #     moving_objects.append(MovingObject(start_x, start_y, path_layer, tmx_data, "assets/images/balls"))
    #     step_counter = 0

    pygame.display.flip()

    pygame.time.delay(50)

pygame.quit()
