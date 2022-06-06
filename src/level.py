import pygame
from support import *
from knight import Knight
from item import Item, ValuableItem
from settings import *
from game_data import *
# from main import *

vec = pygame.math.Vector2

class Level:
    def __init__(self):
        self.clock = pygame.time.Clock()

        # self.level = level

        self.is_playing = 1
        self.is_running = 1
        self.state = 'playing'

        self.walls = []

        self.gems = []
        self.sword = []
        self.valuable_item = []
        
        self.e_pos = []
        self.p_pos = None

        self.load()

        self.knight = Knight(self, vec(self.p_pos))
        
        # self.make_enemies()
        self.enemies = []

    def run(self):
        self.clock.tick()

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

    def load(self):
        # TODO: Referenciar o level_01 através da class Game
        self.tilemap_floor = pygame.image.load(level_01['tilemap_floor_png'])
        self.tilemap_floor = pygame.transform.scale(self.tilemap_floor, (MAZE_WIDTH, MAZE_HEIGHT))

        self.tilemap_bottom_wall = pygame.image.load(level_01['tilemap_bottom_wall_png'])
        self.tilemap_bottom_wall = pygame.transform.scale(self.tilemap_bottom_wall, (MAZE_WIDTH, MAZE_HEIGHT))

        self.tilemap_upper_wall = pygame.image.load(level_01['tilemap_upper_wall_png'])
        self.tilemap_upper_wall = pygame.transform.scale(self.tilemap_upper_wall, (MAZE_WIDTH, MAZE_HEIGHT))

        self.matrix_tilemap_upper_wall = import_csv_to_matrix(level_01['tilemap_upper_wall_csv'])
        self.matrix_tilemap_bottom_wall = import_csv_to_matrix(level_01['tilemap_bottom_wall_csv'])

        self.p_pos = [13,19]

    def draw_grid(self):
        for x in range(SCREEN_WIDTH//CELL_WIDTH):
            pygame.draw.line(self.background, DARKGREY, (x*CELL_WIDTH, 0), (x*self.cell_width, SCREEN_HEIGHT))
        for x in range(SCREEN_HEIGHT//self.cell_height):
            pygame.draw.line(self.background, DARKGREY, (0, x*CELL_HEIGHT), (SCREEN_WIDTH, x*CELL_HEIGHT))
        # for coin in self.coins:
        #     pygame.draw.rect(self.background, (167, 179, 34), (coin.x*self.cell_width,
        #     coin.y*self.cell_height, self.cell_width, self.cell_height))
    

    def start_draw(self):
        # TODO
        pass

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = 0
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
        self.knight.update()
        print(self.knight.pix_pos)
    
    def playing_draw(self):
        screen.fill(DARKGREY)
        
        screen.blit(self.tilemap_floor, (INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME))
        screen.blit(self.tilemap_bottom_wall, (INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME))

        self.knight.draw()

        screen.blit(self.tilemap_upper_wall, (INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME))

        # self.draw_grid()

        self.draw_text('GAME SCORE: {}'.format(self.knight.curr_score), screen, [60, 0], SIZE_FONT, WHITE, PATH_FONT)
        self.draw_text('HI-SCORE: 0', screen, [SCREEN_WIDTH//2+60, 0], SIZE_FONT, WHITE, PATH_FONT)

        pygame.display.update()

        
