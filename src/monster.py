from os import path
import pygame

from game_data import *
from support import grid_2_pix_pos, import_and_cut_tileset_into_tiles

vec = pygame.math.Vector2

class Monster(pygame.sprite.Sprite):
    def __init__(self, level, pos, monster_number, monster_type):
        pygame.sprite.Sprite.__init__(self)

        self.level = level

        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = grid_2_pix_pos(pos)

        self.direction = vec(0, 0)
        self.speed = self.set_speed()
        self.target = None

        self.monster_number = monster_number
        self.monster_type = monster_type
        self.action_mode = self.set_action_mode()

    def update(self):
        pass
    
    def draw(self):
        pass

    def set_speed(self):
        if self.action_mode in ["speedy","defeated"]:
            speed = 2
        else:
            speed = 1
        return speed

    def load_monster_sprite(self):
        if self.monster_type == "zombie":
            monster_width, monster_height = 32, 34

            path_monster_left = path.join(base_path["path_monster"], "zombie/","zombie_"+self.monster_number+"_run_left.png")
            path_monster_right = path.join(base_path["path_monster"], "zombie/","zombie_"+self.monster_number+"_run_right.png")

            self.monster_left_sprites = import_and_cut_tileset_into_tiles(path_monster_left, monster_width, monster_height, self.starting_pos)
            self.monster_right_sprites = import_and_cut_tileset_into_tiles(path_monster_right, monster_width, monster_height, self.starting_pos)
        elif self.monster_type == "ogre":
            self.monster_width, self.monster_height = 32, 32
            pass
        elif self.monster_type == "dark_knight":
            self.monster_width, self.monster_height = 32, 32
            pass
        else:
            self.monster_width, self.monster_height = 32, 36
            pass

    
    def set_action_mode():
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "chaser"
        elif self.number == 2:
            return "prey"
        elif self.number == 3:
            return "defeated"
        else:
            return "scatter"
