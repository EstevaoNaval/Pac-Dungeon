import os
import pygame
from settings import CELL_HEIGHT, CELL_WIDTH, INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME, SCREEN_HEIGHT, WHITE, screen
from game_data import *
from support import grid_2_pix_pos, import_and_cut_tileset_into_tiles, pix_2_grid_pos

vec = pygame.math.Vector2

class Knight(pygame.sprite.Sprite):
    def __init__(self, level, pos, knight_gender):
        pygame.sprite.Sprite.__init__(self)

        self.level = level
        self.knight_gender = knight_gender
        
        self.starting_pos = [pos.x,pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()

        self.speed = 1
        self.direction = vec(1,0)
        self.stored_direction = None
        self.last_right_or_left_direction = vec(1, 0)
        self.able_to_move = 1

        self.curr_score = 0

        self.hp_point = 2

        self.load_knight_sprite()

        self.curr_sprite = 0
        self.image = self.knight_right_sprites[self.curr_sprite]

        self.rect = pygame.Rect(0, 0, self.knight_width, self.knight_height)

    def load_knight_sprite(self):
        knight_width, knight_height = 16, 28
        
        path_knight_right = os.path.join(base_path["path_knight"],self.knight_gender+"/","knight_"+self.knight_gender+"_run_right.png")
        path_knight_left = os.path.join(base_path["path_knight"],self.knight_gender+"/","knight_"+self.knight_gender+"_run_left.png")

        self.knight_left_sprites = import_and_cut_tileset_into_tiles(path_knight_left, knight_width, knight_height, self.starting_pos)
        self.knight_right_sprites = import_and_cut_tileset_into_tiles(path_knight_right, knight_width, knight_height, self.starting_pos)

    def update(self):
        if self.direction == vec(-1, 0) or self.last_right_or_left_direction == vec(-1, 0):
            self.image = self.knight_left_sprites[int(self.curr_sprite)]
        elif self.direction == vec(1, 0) or self.last_right_or_left_direction == vec(1, 0):
            self.image = self.knight_right_sprites[int(self.curr_sprite)]

        if self.able_to_move:
            self.pix_pos.x += self.direction.x * self.speed
            self.pix_pos.y += self.direction.y * self.speed

            self.rect.x = self.pix_pos.x
            self.rect.y = self.pix_pos.y

        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.verify_collision()

        self.on_item()

        self.curr_sprite += 0.1
        if self.curr_sprite >= len(self.knight_left_sprites): self.curr_sprite = 0

        # Set a posição do grid em referência a posição do pixel
        self.grid_pos = pix_2_grid_pos(self.pix_pos)

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

    def move(self, direction):
        if direction == vec(-1, 0) or direction == vec(1, 0):
            self.last_right_or_left_direction = direction
        self.stored_direction = direction 

    def get_pix_pos(self):
        return grid_2_pix_pos(self.grid_pos)

    def time_to_move(self):
        if (self.pix_pos.x + CELL_WIDTH) % CELL_WIDTH == 0: 
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0): return 1
        if (self.pix_pos.y + CELL_HEIGHT) % CELL_HEIGHT == 0: 
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0): return 1
        return 0

    def verify_collision(self):
        # collision_tolerance = 10

        for gate in self.level.coord_monster_house_gate:
            if self.rect.collidepoint(((gate.x - self.direction.x) * CELL_WIDTH) + INITIAL_POSITION_X_GAME, ((gate.y - self.direction.y) * CELL_HEIGHT) + INITIAL_POSITION_Y_GAME):
                print("Não passarão")
                return 0

        for wall in self.level.coord_wall:
            if self.rect.collidepoint(((wall.x - self.direction.x) * CELL_WIDTH) + INITIAL_POSITION_X_GAME, ((wall.y - self.direction.y) * CELL_HEIGHT) + INITIAL_POSITION_Y_GAME):
                print("Não passarão")
                return 0
        return 1

    def on_item(self):
        for i_gem in range(len(self.level.rect_gem)):
            if self.rect.colliderect(self.level.rect_gem[i_gem]):
                self.get_gem(i_gem)
                break
        
        for i_sword in range(len(self.level.rect_sword)):
            if self.rect.colliderect(self.level.rect_sword[i_sword]):
                self.get_sword(i_sword)
                break

    def get_gem(self, index_gem):
        del self.level.rect_gem[index_gem]
        self.curr_score += 10

    def get_sword(self, index_sword):
        del self.level.rect_sword[index_sword]
        self.curr_score += 100

    '''def on_sword(self):
        for i_sword in range(len())'''