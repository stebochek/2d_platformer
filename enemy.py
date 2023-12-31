import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    def __init__(self, size, x, y, animation_speed):
        super().__init__(size, x, y, './graphics/enemies/run', animation_speed)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(1, 2)
        self.animation_speed = animation_speed

    def move(self):
        self.rect.x += self.speed

    def flip_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()
        self.move()
        self.flip_image()
