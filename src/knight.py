import os
from time import time
import pygame
from settings import CELL_HEIGHT, CELL_WIDTH, INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME, MAZE_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, screen
from game_data import *
from support import grid_2_pix_pos, import_and_cut_tileset_into_tiles, pix_2_grid_pos

vec = pygame.math.Vector2

class Knight(pygame.sprite.Sprite):
    def __init__(self, level, pos, knight_gender):
        pygame.sprite.Sprite.__init__(self)

        self.level = level
        self.knight_gender = knight_gender
        
        self.starting_pos = [pos[0],pos[1]]
        self.grid_pos = pos
        self.pix_pos = grid_2_pix_pos(self.grid_pos)

        self.speed = specs["step_{}".format(self.level.main.step)]["knight_speed"]
        self.direction = vec(1,0)
        self.stored_direction = None
        self.last_right_or_left_direction = vec(1, 0)
        self.able_to_move = 1

        self.time_prey = 0
        self.num_flash = specs["step_{}".format(self.level.main.step)]["number_of_flashes"]
        self.action_mode = "prey"
        
        self.curr_score = 0

        self.hp_point = 2

        self.load_knight_sprite()

        self.monster_mode_flash = 1
        self.curr_sprite = 0
        self.image = self.knight_right_sprites[self.curr_sprite]

        self.rect = pygame.Rect(0, 0, self.knight_width, self.knight_height)

    def load_knight_sprite(self):
        self.knight_width, self.knight_height = 16, 28
        
        path_knight_right = os.path.join(base_path["path_knight"],"{}/".format(self.knight_gender), "knight_{}_run_right.png".format(self.knight_gender))
        path_knight_left = os.path.join(base_path["path_knight"],"{}/".format(self.knight_gender),"knight_{}_run_left.png".format(self.knight_gender))

        self.knight_left_sprites = import_and_cut_tileset_into_tiles(path_knight_left, self.knight_width, self.knight_height, self.starting_pos)
        self.knight_right_sprites = import_and_cut_tileset_into_tiles(path_knight_right, self.knight_width, self.knight_height, self.starting_pos)

    def update(self):
        if self.direction == vec(-1, 0) or self.last_right_or_left_direction == vec(-1, 0):
            self.image = self.knight_left_sprites[int(self.curr_sprite)]
        elif self.direction == vec(1, 0) or self.last_right_or_left_direction == vec(1, 0):
            self.image = self.knight_right_sprites[int(self.curr_sprite)]

        '''if self.action_mode == "chaser":
            self.event_knight_chaser()'''

        self.speed = self.set_speed()

        if self.able_to_move:
            self.pix_pos[0] += self.direction.x * self.speed
            self.pix_pos[1] += self.direction.y * self.speed

            self.in_tunnel()

            self.rect.x = self.pix_pos[0]
            self.rect.y = self.pix_pos[1]

        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.verify_collision()

        self.on_item()

        self.curr_sprite += 0.1
        if self.curr_sprite >= len(self.knight_left_sprites): self.curr_sprite = 0

        # Set a posição do grid em referência a posição do pixel
        self.grid_pos = pix_2_grid_pos(self.pix_pos)
    
    def in_tunnel(self):
        if self.pix_pos[0] > SCREEN_WIDTH:
            self.pix_pos[0] = 0
        elif self.pix_pos[0] < 0:
            self.pix_pos[0] = SCREEN_WIDTH
        elif self.pix_pos[1] < 32:
            self.pix_pos[1] = SCREEN_HEIGHT - 31
        elif self.pix_pos[1] > MAZE_HEIGHT + 32:
            self.pix_pos[1] = 32

    def activate_mode_chaser(self):
        self.action_mode = "chaser"
        self.time = time()

    def event_knight_chaser(self):
        # self.time_prey += self.level.delta_time()
        if self.time >= specs["step_{}".format(self.level.main.step)]["fright_time_in_sec"]:
            self.time = time.time()
            self.time = 0
            if self.num_flash <= 0:
                self.monster_mode_flash = 0
                self.time_prey = 0
                self.num_flash = specs["step_{}".format(self.level.main.step)]["knight_speed"]
                self.action_mode = "prey"
            else:
                self.monster_mode_flash = 1
                self.num_flash -= 1


    def draw(self):
        '''self.knight_list = pygame.sprite.Group()
        tileset = pygame.image.load(self.path_knight).convert_alpha(screen)
        x, y = 4 * self.knight_width, 1 * self.knight_height

        for img in self.knight_images:
            img.blit(tileset, (0,0), pygame.Rect(x, y, self.knight_width, self.knight_height))
        
        # self.knight_list.draw(screen)'''

        self.image.blit(screen, self.pix_pos)

        '''# Drawing player lives
        for x in range(self.hp_point):
            pygame.draw.circle(screen, WHITE, (30 + 20*x, SCREEN_HEIGHT - 15), 7)'''

        # Drawing the grid pos rect
        # pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                         self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

    def set_speed(self):
        if self.action_mode == "chaser":
            return specs["step_{}".format(self.level.main.step)]["fright_knight_speed"]
        elif self.action_mode == "prey":
            return specs["step_{}".format(self.level.main.step)]["knight_speed"]

    def move(self, direction):
        if direction == vec(-1, 0) or direction == vec(1, 0):
            self.last_right_or_left_direction = direction
        self.stored_direction = direction

    def time_to_move(self):
        if int(self.pix_pos[0] + CELL_WIDTH) % CELL_WIDTH == 0: 
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0): return 1
        if int(self.pix_pos[1] + CELL_HEIGHT) % CELL_HEIGHT == 0: 
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0): return 1
        return 0

    def verify_collision(self):
        # collision_tolerance = 10

        for gate in self.level.coord_monster_house_gate:
            if self.rect.collidepoint(((gate[0] - self.direction.x) * CELL_WIDTH) + INITIAL_POSITION_X_GAME, ((gate[1] - self.direction.y) * CELL_HEIGHT) + INITIAL_POSITION_Y_GAME):
                print("Não passarão")
                return 0

        for wall in self.level.coord_wall:
            if self.rect.collidepoint(((wall[0] - self.direction.x) * CELL_WIDTH) + INITIAL_POSITION_X_GAME, ((wall[1] - self.direction.y) * CELL_HEIGHT) + INITIAL_POSITION_Y_GAME):
                print("Não passarão")
                return 0

        return 1

    def on_item(self):
        for i_gem in range(len(self.level.rect_gem)):
            if self.rect.colliderect(self.level.rect_gem[i_gem]):
                # self.activate_mode_chaser()
                self.get_item(i_gem, self.level.rect_gem, 50)
                break
        
        for i_pill in range(len(self.level.rect_pill)):
            if self.rect.colliderect(self.level.rect_pill[i_pill]):
                self.get_item(i_pill, self.level.rect_pill, 10)
                break

    def get_item(self, index_item, list_rect_item, item_point):
        del list_rect_item[index_item]
        self.curr_score += item_point

    def set_action_mode(self):
        pass