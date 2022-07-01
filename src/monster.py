from os import path
import pygame

from settings import screen
from game_data import *
from support import grid_2_pix_pos, import_and_cut_tileset_into_tiles, pix_2_grid_pos

vec = pygame.math.Vector2

class Monster(pygame.sprite.Sprite):
    def __init__(self, level, pos, monster_number, monster_type):
        pygame.sprite.Sprite.__init__(self)

        self.level = level

        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = grid_2_pix_pos(pos)

        self.monster_number = str(monster_number)
        self.monster_type = monster_type
        self.action_mode = "scatter"
        self.monster_personality = self.set_monster_personality()

        self.direction = vec(0, 0)
        self.speed = self.set_speed()
        self.target = None
        self.last_right_or_left_direction = vec(1, 0)
        self.able_to_move = 1

        self.load_monster_sprite()

        self.curr_sprite = 0
        self.image = self.monster_right_sprites[self.curr_sprite]

        self.rect = pygame.Rect(self.pix_pos.x, self.pix_pos.y, self.monster_width, self.monster_height)

    def update(self):
        '''self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()'''

        self.image = self.monster_right_sprites[int(self.curr_sprite)]

        self.curr_sprite += 0.1
        if self.curr_sprite >= len(self.monster_left_sprites): self.curr_sprite = 0

        self.grid_pos = pix_2_grid_pos(self.pix_pos)
    
    def draw(self):
        self.image.blit(screen, self.pix_pos)
        pass

    def set_speed(self):
        if self.action_mode in ["speedy","defeated"]:
            speed = 2
        else:
            speed = 1
        return speed

    def set_target(self):

        pass

    def load_monster_sprite(self):
        if self.monster_type == "zombie":
            self.monster_width, self.monster_height = 32, 34

            path_monster_left = path.join(base_path["path_monster"], "zombie/","zombie_"+self.monster_number+"_run_left.png")
            path_monster_right = path.join(base_path["path_monster"], "zombie/","zombie_"+self.monster_number+"_run_right.png")
        elif self.monster_type == "ogre":
            self.monster_width, self.monster_height = 32, 32
            
            path_monster_left = path.join(base_path["path_monster"], "ogre/","ogre_"+self.monster_number+"_run_left.png")
            path_monster_right = path.join(base_path["path_monster"], "ogre/","ogre_"+self.monster_number+"_run_right.png")
        elif self.monster_type == "dark_knight":
            self.monster_width, self.monster_height = 32, 32
            
            path_monster_left = path.join(base_path["path_monster"], "dark_knight/", "dark_knight_"+self.monster_number+"_run_left.png")
            path_monster_right = path.join(base_path["path_monster"], "dark_knight/", "dark_knight_"+self.monster_number+"_run_right.png")
        else:
            self.monster_width, self.monster_height = 32, 36

            path_monster_left = path.join(base_path["path_monster"], "hades/", "hades_"+self.monster_number+"_run_left.png")
            path_monster_right = path.join(base_path["path_monster"], "hades/", "hades_"+self.monster_number+"_run_right.png")
            pass

        self.monster_left_sprites = import_and_cut_tileset_into_tiles(path_monster_left, self.monster_width, self.monster_height, self.starting_pos)
        self.monster_right_sprites = import_and_cut_tileset_into_tiles(path_monster_right, self.monster_width, self.monster_height, self.starting_pos)

    def set_monster_personality(self):
        if self.monster_number == '1':
            return "blinky"
        elif self.monster_number == '2':
            return "pinky"
        elif self.monster_number == '3':
            return "inky"
        else:
            return "clyde"
    
    def set_action_mode(self):
        if self.action_number == 0:
            return "speedy"
        elif self.action_number == 1:
            return "chaser"
        elif self.action_number == 2:
            return "prey"
        elif self.action_number == 3:
            return "defeated"
        else:
            return "scatter"
