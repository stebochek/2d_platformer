import pygame
from settings import screen_width, screen_height
from tiles import AnimatedTile

class Background:
    def __init__(self):
        self.background_1 = pygame.image.load('./graphics/background/sky/Background_1.png').convert_alpha()
        self.background_2 = pygame.image.load('./graphics/background/sky/Background_2.png').convert_alpha()

        # editing
        self.background_1 = pygame.transform.scale(self.background_1, (screen_width, screen_height))
        self.background_2 = pygame.transform.scale(self.background_2, (screen_width, screen_height))

    def draw(self, surface):
        surface.blit(self.background_2, (0, 0))
        surface.blit(self.background_1, (0, 0))


class Water:
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 192
        amount_of_tiles = int((level_width + screen_width) / water_tile_width) * 2
        self.water_sprites = pygame.sprite.Group()

        for tile in range(amount_of_tiles):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192, x, y, './graphics/background/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)