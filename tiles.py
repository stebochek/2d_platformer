import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift):
        self.rect.x += x_shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path, animation_speed):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = animation_speed
        self.path = path


    def animate(self):
        self.frame_index += self.animation_speed
        if int(self.frame_index) >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        if './graphics/character/end_of_level' in self.path:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift


class Coin(AnimatedTile):
    def __init__(self, size, x, y, path, value, animation_speed):
        super().__init__(size, x, y, path, animation_speed)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.value = value
        self.animation_speed = animation_speed


class Goal(AnimatedTile):
    def __init__(self, size, x, y, path, animation_speed):
        super().__init__(size, x, y, path, animation_speed)
        self.animation_speed = animation_speed

