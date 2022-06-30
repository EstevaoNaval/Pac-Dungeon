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

        self.action_number = 4
        self.monster_number = str(monster_number)
        self.monster_type = monster_type
        self.action_mode = self.set_action_mode()

        self.direction = vec(0, 0)
        self.speed = self.set_speed()
        self.target = None
        self.last_right_or_left_direction = vec(1, 0)
        self.able_to_move = 1

        self.load_monster_sprite()

        self.curr_sprite = 0
        self.image = self.monster_right_sprites[self.curr_sprite]

        self.rect = pygame.Rect(0, 0, self.monster_width, self.monster_height)

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
