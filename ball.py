import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, hero_rect):
        super().__init__()
        self.image = pygame.image.load(f"assets/images/balls/{color}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = hero_rect.centerx
        self.rect.bottom = hero_rect.top + 19

    def update(self, hero_rect):
        self.rect.centerx = hero_rect.centerx
        self.rect.bottom = hero_rect.top + 19
