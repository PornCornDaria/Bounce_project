import pygame
from pygame import *


PLATFORM_WIDTH = 35
PLATFORM_HEIGHT = 35


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load('C:/Users/Daria/PycharmProjects/bounce_project/wall.png')
        self.image = pygame.transform.scale(self.image1, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
