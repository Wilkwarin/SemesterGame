# main.py

import pygame
import pytmx
from moving_object import MovingObject  # Импорт класса MovingObject

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))

# Загрузка карты
tmx_data = pytmx.load_pygame("game/mapa.tmx")  # Убедитесь, что путь правильный

# Получение слоёв Path и Terrain
path_layer = None
terrain_layer = None
for layer in tmx_data.layers:
    if layer.name == "Path":
        path_layer = layer
    elif layer.name == "Terrain":
        terrain_layer = layer

if not path_layer or not terrain_layer:
    raise ValueError("Один или оба слоя Path и Terrain не найдены!")

# Функция для проверки свойств тайлов
def get_tile_properties(layer, tile_x, tile_y):
    """
    Получить свойства тайла для указанного слоя.
    """
    tile_gid = layer.data[tile_y][tile_x]
    if tile_gid == 0:
        return None  # Нет тайла
    tile_props = tmx_data.get_tile_properties_by_gid(tile_gid)
    return tile_props

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

# Создание объекта MovingObject
moving_object = MovingObject(3, 0, path_layer, tmx_data)  # Начинаем с координат (3, 0)

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

    # Перемещаем объект
    moving_object.move()

    # Отображаем объект
    screen.blit(moving_object.image, moving_object.rect)

    # Обновляем экран
    pygame.display.flip()

    # Задержка для "плавного" движения
    pygame.time.delay(100)

# Закрытие игры
pygame.quit()