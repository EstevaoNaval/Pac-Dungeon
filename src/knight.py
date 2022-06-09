from math import floor
import pygame
from settings import CELL_HEIGHT, CELL_WIDTH, INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME, SCREEN_HEIGHT, TOP_BOTTOM_BUFFER, WHITE, screen
from game_data import knight

vec = pygame.math.Vector2

class Knight(pygame.sprite.Sprite):
    def __init__(self, level, pos, knight_gender):
        self.level = level
        
        self.starting_pos = [pos.x,pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()

        self.speed = 2
        self.direction = vec(1,0)
        self.stored_direction = None
        self.able_to_move = 1

        self.curr_score = 0

        self.hp_point = 3

    def load_knight_sprite(self):
        pass

    def update(self):
        if self.able_to_move:
            self.pix_pos +=  self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        
        # Set a posição do grid em referência a posição do pixel
        self.grid_pos.x = floor((self.pix_pos.x - INITIAL_POSITION_X_GAME) / CELL_WIDTH)
        self.grid_pos.y = floor((self.pix_pos.y - INITIAL_POSITION_Y_GAME) / CELL_HEIGHT)

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.pix_pos.x), int(self.pix_pos.y)), CELL_WIDTH//2-2)
        

        # Drawing player lives
        for x in range(self.hp_point):
            pygame.draw.circle(screen, WHITE, (30 + 20*x, SCREEN_HEIGHT - 15), 7)

        # Drawing the grid pos rect
        # pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                         self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos.x * CELL_WIDTH) + INITIAL_POSITION_X_GAME, (self.grid_pos.y * CELL_HEIGHT) + INITIAL_POSITION_Y_GAME)

    def time_to_move(self):
        if (self.pix_pos.x + CELL_WIDTH//2) % CELL_WIDTH == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0): return 1
        if (self.pix_pos.y + CELL_HEIGHT//2) % CELL_HEIGHT == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0): return 1
        return 0
    
    def can_move(self):
        for tile_not_pass in self.level.coord_monster_house_gate:
            if vec(self.grid_pos+self.direction) == tile_not_pass:
                print("Não passarão!!!")
                return 0
        for tile_not_pass in self.level.coord_wall:
            if vec(self.grid_pos+self.direction) == tile_not_pass:
                print("Não passarão!!!")
                return 0
        return 1