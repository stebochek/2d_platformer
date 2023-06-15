import pygame


class UI:
    def __init__(self, surface):
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('./graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft_first = (84, 36)
        self.health_bar_topleft_second = (84, 44)
        self.health_bar_topleft_third = (84, 47)
        self.bar_max_width = 188
        self.bar_height = 15

        # coins
        self.coin = pygame.image.load('./graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(85, 64))
        self.font = pygame.font.Font('./graphics/ui/ARCADEPI.TTF', 28)

    def show_health(self, current_health, max_health):
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current_health / max_health
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect_first = pygame.Rect(self.health_bar_topleft_first, (current_bar_width, 8))
        health_bar_rect_second = pygame.Rect(self.health_bar_topleft_second, (current_bar_width, 3))
        health_bar_rect_third = pygame.Rect(self.health_bar_topleft_third, (current_bar_width, 4))
        pygame.draw.rect(self.display_surface, '#a33838', health_bar_rect_first)
        pygame.draw.rect(self.display_surface, '#c04444', health_bar_rect_second)
        pygame.draw.rect(self.display_surface, '#dd5555', health_bar_rect_third)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, 'black')
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)
