# moving_object.py

import pygame

class MovingObject(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, path_layer, tmx_data, image):
        super().__init__()
        self.image = image  # Используем переданное изображение
        self.rect = self.image.get_rect()
        self.rect.topleft = (start_x * 16, start_y * 16)  # Переводим координаты в пиксели

        # Слой и данные для получения направлений
        self.path_layer = path_layer
        self.tmx_data = tmx_data
        self.x, self.y = start_x, start_y  # Начальные координаты
        self.direction = self.get_direction(self.x, self.y)  # Направление

    def get_direction(self, x, y):
        tile_gid = self.path_layer.data[y][x]
        tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
        if tile_props:
            return tile_props.get("Direction", None)
        return None

    def move(self):
        """ Перемещение объекта по траектории """
        direction = self.direction

        if direction == 0 or direction is None:
            return

        if direction == 1:  # Вниз
            self.y += 1
        elif direction == 2:  # Направо
            self.x += 1
        elif direction == 3:  # Налево
            self.x -= 1
        elif direction == 4:  # Вниз-направо
            self.x += 1
        elif direction == 5:  # Направо-вниз
            self.y += 1
        elif direction == 6:  # Вниз-налево
            self.x -= 1
        elif direction == 7:  # Налево-вниз
            self.y += 1

        # Обновляем позицию
        self.rect.topleft = (self.x * 16, self.y * 16)

        # Обновляем направление
        self.direction = self.get_direction(self.x, self.y)
