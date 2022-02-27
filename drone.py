import pygame

class Drone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("drone.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect[2] = 5
        self.rect[3] = 5
