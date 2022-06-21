import pygame
from support import *
from knight import Knight
from item import Item, ValuableItem
from settings import *
from game_data import *
from sys import exit
from os import path
# from main import *

vec = pygame.math.Vector2

class Level:
    def __init__(self,num_level):
        self.clock = pygame.time.Clock()

        self.num_level = num_level

        self.is_playing = 1
        self.is_running = 1
        self.state = 'playing'

        self.rect_wall = []
        self.rect_monster_house_gate = []

        self.rect_gem = []
        self.sword = []
        self.valuable_item = []
        
        self.e_pos = []
        self.knight_pos = None

        self.load()

        self.knight = Knight(self, vec(self.knight_pos), 'M')
        self.group_knight = pygame.sprite.Group(self.knight)
        
        # self.make_enemies()
        self.monster = []

    def run(self):
        self.clock.tick(FPS)

        while self.is_playing:
            '''if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()'''
            if self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game_over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.is_playing = 0
    
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def draw_grid(self):
        for x in range(MAZE_WIDTH//CELL_WIDTH):
            pygame.draw.line(self.tilemap_upper_wall, WHITE, (x*CELL_WIDTH, 0), (x*CELL_WIDTH, MAZE_HEIGHT))
        for y in range(MAZE_HEIGHT//CELL_HEIGHT):
            pygame.draw.line(self.tilemap_upper_wall,WHITE, (0, y*CELL_HEIGHT), (MAZE_WIDTH, y*CELL_HEIGHT))
        # for coin in self.coins:
        #     pygame.draw.rect(self.background, (167, 179, 34), (coin.x*self.cell_width,
        #                                                        coin.y*self.cell_height, self.cell_width, self.cell_height))

    def load(self):
        # TODO: Referenciar o level_01 através da class Game
        self.tilemap_floor = pygame.image.load(path.join(base_path["path_tilemap"], "level_"+self.num_level,
        "tilemap_floor_level_"+self.num_level+".png"))
        self.tilemap_floor = pygame.transform.scale(self.tilemap_floor, (MAZE_WIDTH, MAZE_HEIGHT))

        self.tilemap_bottom_wall = pygame.image.load(path.join(base_path["path_tilemap"], "level_"+self.num_level,
        "tilemap_bottom_wall_level_"+self.num_level+".png"))
        self.tilemap_bottom_wall = pygame.transform.scale(self.tilemap_bottom_wall, (MAZE_WIDTH, MAZE_HEIGHT))

        self.tilemap_upper_wall = pygame.image.load(path.join(base_path["path_tilemap"], "level_"+self.num_level,
        "tilemap_upper_wall_level_"+self.num_level+".png"))
        self.tilemap_upper_wall = pygame.transform.scale(self.tilemap_upper_wall, (MAZE_WIDTH, MAZE_HEIGHT))

        self.matrix_tilemap = import_csv_to_matrix(path.join(base_path["path_tilemap"], "level_"+self.num_level,
        "tilemap_level_"+self.num_level+".csv"))

        for x in range(len(self.matrix_tilemap)):
            for y in range(len(self.matrix_tilemap[0])):
                code_tileset_map = int(self.matrix_tilemap[x][y])
                if (code_tileset_map == -1):
                    pix_pos = grid_2_pix_pos(vec(y, x))
                    self.rect_gem.append(Rect(pix_pos.x, pix_pos.y, CELL_WIDTH, CELL_HEIGHT))
                if ((code_tileset_map >= 11 and code_tileset_map < 70) or code_tileset_map >= 80):
                    pix_pos = grid_2_pix_pos(vec(y, x))
                    self.rect_wall.append(Rect(pix_pos.x, pix_pos.y, CELL_WIDTH, CELL_HEIGHT))
                if (code_tileset_map == -10):
                    pix_pos = grid_2_pix_pos(vec(y, x))
                    self.rect_monster_house_gate.append(Rect(pix_pos.x, pix_pos.y, CELL_WIDTH, CELL_HEIGHT))
                if (code_tileset_map == -5):
                    self.knight_pos = [y, x]

    def draw_coins(self):
        for gem in self.rect_gem:
            pygame.draw.circle(screen, (190,187,160), [gem.x + CELL_WIDTH//2, gem.y + CELL_HEIGHT//2], 3)   

    def start_draw(self):
        # TODO
        pass

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = 0
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.knight.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.knight.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.knight.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.knight.move(vec(0, 1))
    
    def playing_update(self):
        self.group_knight.update()
        print(self.knight.pix_pos)
    
    def playing_draw(self):
        screen.fill(DARKGREY)
        
        screen.blit(self.tilemap_floor, (INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME))
        screen.blit(self.tilemap_bottom_wall, (INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME))

        self.draw_coins()
        self.group_knight.draw(screen)
        

        screen.blit(self.tilemap_upper_wall, (INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME))

        # self.draw_grid()

        self.draw_text('GAME SCORE: {}'.format(self.knight.curr_score), screen, [SCREEN_WIDTH//60+2, 0], SIZE_FONT, WHITE, PATH_FONT)
        self.draw_text('HI-SCORE: 0', screen, [SCREEN_WIDTH//2+60, 0], SIZE_FONT, WHITE, PATH_FONT)

        pygame.display.flip()

        
