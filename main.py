# main.py

import pygame
import pytmx
from moving_object import MovingObject

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))

# Загрузка карты
tmx_data = pytmx.load_pygame("game/mapa.tmx")  # Убедитесь, что путь правильный

# Получение слоёв Path, Terrain, и MovingObjects
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
    raise ValueError("Один или несколько слоёв Path, Terrain или MovingObjects не найдены!")

# Функция для отрисовки слоя
def draw_layer(layer):
    """
    Отрисовка заданного слоя.
    """
    for y in range(tmx_data.height):
        for x in range(tmx_data.width):
            tile_gid = layer.data[y][x]
            if tile_gid != 0:
                tile_image = tmx_data.get_tile_image_by_gid(tile_gid)
                if tile_image:
                    screen.blit(tile_image, (x * 16, y * 16))  # Позиция тайла в пикселях

# Загрузка изображения для MovingObject
moving_object_image = pygame.image.load("assets/images/balls/1.png").convert_alpha()

# Создание объектов MovingObject
moving_objects = []
for obj in object_layer:
    if obj.type == "MovingObject":
        start_x = int(obj.x / 16)  # Перевод из пикселей в тайловые координаты
        start_y = int(obj.y / 16)
        moving_objects.append(MovingObject(start_x, start_y, path_layer, tmx_data, moving_object_image))

# Основной цикл игры
running = True
while running:
    screen.fill((255, 255, 255))  # Очистка экрана (белый фон)

    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отрисовка слоя Terrain
    draw_layer(terrain_layer)

    # Перемещение и отображение объектов
    for moving_object in moving_objects:
        moving_object.move()
        screen.blit(moving_object.image, moving_object.rect)

    # Обновляем экран
    pygame.display.flip()

    # Задержка для "плавного" движения
    pygame.time.delay(100)

# Закрытие игры
pygame.quit()
