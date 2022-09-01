from os import DirEntry
import pygame
from support import import_csv_layout, import_cut_graphics, import_folder
from settings import tile_size, screen_width, screen_height
from tiles import Tile, StaticTile
from player import Player
from particles import ParticleEffect

class Level:
    def __init__(self, level_data, surface):
        #general setup
        self.display_surface = surface
        self.world_shift_x = 0
        self.world_shift_y = 0 
        self.current_x = 0
        self.gravity = 0.6

        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        #import sprite group bg in this case
        bg_layout = import_csv_layout(level_data['bg'])
        self.bg_sprites = self.create_tile_group(bg_layout, 'bg')

        #player
        self.player = pygame.sprite.GroupSingle()
        player_sprite = Player((120,40), self.display_surface, self.create_jump_particles)
        self.player.add(player_sprite)

    #create tile paints the background map for the non null values using the cut up graphic tileset
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'bg':
                        bg_tile_list = import_cut_graphics('tiles/bg2.png')
                        tile_surface = bg_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)
                

        return sprite_group
    
    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)

    def apply_gravity(self):
        player = self.player.sprite
        player.speed_y = 0
        player.speed_y += self.gravity
        player.direction.y += player.speed_y
        player.rect.y += player.direction.y + self.world_shift_y

        #print(player.direction.y)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/4 and direction_x < 0:
            self.world_shift_x = 2
            player.speed_x = 0
        elif player_x > (screen_width - screen_width/4) and direction_x > 0:
            self.world_shift_x = -2
            player.speed_x = 0
        else:
            self.world_shift_x = 0
            player.speed_x = 2
    
    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_y < screen_height/4 and direction_y < 0:
            self.world_shift_y = -direction_y
        elif player_y > (screen_height - screen_height/4) and direction_y > 0:
            self.world_shift_y = -direction_y
        else:
            self.world_shift_y = 0
            #player.speed_y = 0
        
        
        #print(self.world_shift_y)
        print(player.direction.y)
            


    def horizontal_movement_collision(self):
        player = self.player.sprite 
        player.rect.x += player.direction.x * player.speed_x
        
        for sprite in self.bg_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x and player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x and player.direction.x <= 0):\
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        self.apply_gravity()

        for sprite in self.bg_sprites.sprites():
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

    def move(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed_x

        player.rect.y += player.direction.y

        



    def run(self):
        #dust particles
        self.dust_sprite.update(self.world_shift_x, self.world_shift_y)
        self.dust_sprite.draw(self.display_surface) 

        #will run the level
        
        self.bg_sprites.update(self.world_shift_x, self.world_shift_y)
        self.bg_sprites.draw(self.display_surface)
        #self.scroll_x()

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.scroll_x()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.scroll_y()
        self.create_landing_dust()
        self.player.draw(self.display_surface)