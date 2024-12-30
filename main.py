import pygame
import pytmx

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((960, 960))

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


# Функция для проверки направлений и проходимости
def get_tile_properties(tile_x, tile_y):
    # Получаем GID тайла
    tile_gid = path_layer.data[tile_y][
        tile_x]  # Примечание: координаты (x, y) в Tiled идут как (x, y), но в pytmx: [y][x]

    # Если GID равен 0, то тайл отсутствует, пропускаем
    if tile_gid == 0:
        return None, None  # Нет тайла

    # Получаем свойства по GID
    tile_props = tmx_data.get_tile_properties_by_gid(tile_gid)
    if tile_props:
        direction = tile_props.get("Direction", "none")  # По умолчанию "none"

        # Теперь проверяем Walkable как целое число
        walkable = tile_props.get("Walkable", 0)  # Если нет свойства, по умолчанию 0 (непроходимо)
        walkable = walkable == 1  # Преобразуем в булево значение (1 - True, 0 - False)

        return direction, walkable
    return None, None  # Если свойств нет, возвращаем None


# Пример проверки карты
print("Проверка направлений и проходимости:")
for y in range(tmx_data.height):
    for x in range(tmx_data.width):
        direction, walkable = get_tile_properties(x, y)
        if direction or walkable is not None:  # Проверяем только если есть направление или проходимость
            print(f"Точка ({x}, {y}) имеет направление: {direction}, проходимость: {walkable}")
        # else:
        #     print(f"Точка ({x}, {y}) не имеет кастомных свойств.")
