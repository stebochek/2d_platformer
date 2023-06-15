import pygame
from tiles import Tile, StaticTile, Coin, Goal
from settings import tile_size, screen_height, screen_width
from player import Player
from particles import ParticleEffect
from support import import_from_csv, import_tiles
from enemy import Enemy
from background import Background, Water
from game_data import levels


def create_tile_group(layout, type_of_lay):
    global sprite
    sprite_group = pygame.sprite.Group()

    # tile lists
    building = import_tiles('./graphics/building/building.png')
    terrain_tile_list = import_tiles('./graphics/terrain/terrain.png')

    for row_index, row in enumerate(layout):
        for col_index, val in enumerate(row):
            if val != '-1':
                x = col_index * tile_size
                y = row_index * tile_size

                if type_of_lay == 'terrain':
                    tile_surface = terrain_tile_list[int(val)]
                    sprite = StaticTile(tile_size, x, y, tile_surface)

                if type_of_lay == 'grass':
                    tile_surface = building[int(val)]
                    sprite = StaticTile(tile_size, x, y, tile_surface)

                if type_of_lay == 'building0':
                    tile_surface = building[int(val)]
                    sprite = StaticTile(tile_size, x, y, tile_surface)

                if type_of_lay == 'building1':
                    tile_surface = building[int(val)]
                    sprite = StaticTile(tile_size, x, y, tile_surface)

                if type_of_lay == 'fence':
                    tile_surface = building[int(val)]
                    sprite = StaticTile(tile_size, x, y, tile_surface)

                if type_of_lay == 'coins':
                    if val == '0':
                        sprite = Coin(tile_size, x, y, './graphics/coins/gold', 3, 0.15)
                    if val == '1':
                        sprite = Coin(tile_size, x, y, './graphics/coins/silver', 1, 0.15)

                if type_of_lay == 'enemies':
                    sprite = Enemy(tile_size, x, y, 0.15)

                if type_of_lay == 'constraints':
                    sprite = Tile(tile_size, x, y)

                sprite_group.add(sprite)

    return sprite_group


class Level:
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = 0

        # audio
        self.coin_sound = pygame.mixer.Sound('./sounds/effects/coin.mp3')
        self.coin_sound.set_volume(0.1)

        self.chiken_death = pygame.mixer.Sound('./sounds/effects/chiken_death.mp3')
        self.chiken_death.set_volume(0.1)

        self.splash_sound = pygame.mixer.Sound('./sounds/effects/splash.mp3')
        self.splash_sound.set_volume(0.1)

        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        # player
        player_layout = import_from_csv(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)
        self.ch_death = False

        # user interface
        self.change_coins = change_coins

        # terrain setup
        terrain_layout = import_from_csv(level_data['terrain'])
        self.terrain_sprites = create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_from_csv(level_data['grass'])
        self.grass_sprites = create_tile_group(grass_layout, 'grass')

        # building
        building_layout = import_from_csv(level_data['building0'])
        self.building0_sprites = create_tile_group(building_layout, 'building0')

        building_layout = import_from_csv(level_data['building1'])
        self.building1_sprites = create_tile_group(building_layout, 'building1')

        # fence setup
        fence_layout = import_from_csv(level_data['fence'])
        self.fence_sprites = create_tile_group(fence_layout, 'fence')

        # coins
        coin_layout = import_from_csv(level_data['coins'])
        self.coin_sprites = create_tile_group(coin_layout, 'coins')

        # enemy
        enemy_layout = import_from_csv(level_data['enemies'])
        self.enemy_sprites = create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraints_layout = import_from_csv(level_data['constraints'])
        self.constraints_sprite = create_tile_group(constraints_layout, 'constraints')

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # death particles
        self.death_sprites = pygame.sprite.Group()

        # background
        self.sky = Background()
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(sprite)
                if val == '1':
                    sprite = Goal(tile_size, x, y, f'./graphics/character/end_of_level/{self.current_level}', 0.07)
                    self.goal.add(sprite)

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 5.6
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = - 5.6
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5.6

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def enemy_collision(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprite, False):
                enemy.reverse()

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.ch_death = True
            self.splash_sound.play()

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collision(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)

    def check_enemy_collision(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.status == 'fall':
                    self.chiken_death.play()
                    self.player.sprite.direction.y = -16
                    self.change_coins(1)
                    death_sprite = ParticleEffect(enemy.rect.center, 'death')
                    self.death_sprites.add(death_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):

        # background
        self.sky.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # buildings
        self.building0_sprites.update(self.world_shift)
        self.building0_sprites.draw(self.display_surface)
        self.building1_sprites.update(self.world_shift)
        self.building1_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraints_sprite.update(self.world_shift)
        self.enemy_collision()
        self.enemy_sprites.draw(self.display_surface)
        self.death_sprites.update(self.world_shift)
        self.death_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()

        # fence
        self.fence_sprites.update(self.world_shift)
        self.fence_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()

        self.check_coin_collision()
        self.check_enemy_collision()
