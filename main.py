# main.py

import pygame
import pytmx
from moving_object import MovingObject  # Импорт класса MovingObject

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))

# Загрузка карты
tmx_data = pytmx.load_pygame("game/mapa.tmx")  # Убедитесь, что путь правильный

# Получение слоя Path
path_layer = None
for layer in tmx_data.layers:
    if layer.name == "Path":
        path_layer = layer
        break

if path_layer is None:
    raise ValueError("Слой 'Path' не найден!")

# Функция для проверки свойств тайлов
def get_tile_properties(tile_x, tile_y):
    tile_gid = path_layer.data[tile_y][tile_x]
    if tile_gid == 0:
        return None, None  # Нет тайла
    tile_props = tmx_data.get_tile_properties_by_gid(tile_gid)
    if tile_props:
        direction = tile_props.get("Direction", "none")
        walkable = tile_props.get("Walkable", 0) == 1
        return direction, walkable
    return None, None

# Функция для подсветки траектории
def draw_trajectory():
    for y in range(tmx_data.height):
        for x in range(tmx_data.width):
            direction, _ = get_tile_properties(x, y)
            if direction:
                # Подсвечиваем тайлы траектории
                pygame.draw.rect(screen, (200, 200, 200), (x * 16, y * 16, 16, 16))

# Создание объекта MovingObject
moving_object = MovingObject(3, 0, path_layer, tmx_data)  # Начинаем с координат (0, 0)

# Основной цикл игры
running = True
while running:
    screen.fill((255, 255, 255))  # Очистка экрана (белый фон)

    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Подсветка всей траектории
    draw_trajectory()

    # Перемещаем объект
    moving_object.move()

    # Отображаем объект
    screen.blit(moving_object.image, moving_object.rect)

    # Обновляем экран
    pygame.display.flip()

    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Задержка для "плавного" движения
    pygame.time.delay(100)

# Закрытие игры
pygame.quit()
