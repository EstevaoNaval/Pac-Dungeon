import pygame
from monster import Monster
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
    def __init__(self, main, num_level, gender_knight):
        self.main = main

        self.sound_obj = pygame.mixer.Sound(".//src//assets//sound//bg_sound.mp3")
        
        self.clock = pygame.time.Clock()
        self.curr_time = 0
        self.last_time = 0

        self.gender_knight = gender_knight

        self.num_level = num_level

        self.is_playing = 1
        self.is_running = 1
        self.state = 'start'

        self.coord_path_monster_go_through_wall = []
        self.coord_wall = []
        self.coord_monster_house_gate = []

        self.coord_tunnel = []

        self.rect_pill = []
        self.rect_gem = []
        self.valuable_item = []
        
        self.monsters = [] 
        self.monster_pos = []

        self.knight_pos = None

        self.load()

        self.knight = Knight(self, self.knight_pos, gender_knight)
        self.group_knight = pygame.sprite.Group(self.knight)
        
        self.monster_type = self.choose_monster_type()
        self.group_monster = pygame.sprite.Group()
        self.make_monster()

    def delta_time(self):
        '''
        Returns the time passed between
        the last and the current frame - SECONDS
        '''
        return self.clock.get_time()/1000

    def run(self):    
        while self.is_playing:
            self.clock.tick(FPS)
            print("{}".format(self.clock.get_fps()))

            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game_over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            elif self.state == 'win':
                self.win_events()
                self.win_update()
                self.win_draw()
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
        self.sound_obj.play()
        self.import_hi_score()

        self.tilemap_floor = pygame.image.load(path.join(base_path["path_tilemap"], "level_{}//".format(self.num_level), 
        "tilemap_floor_level_{}.png".format(self.num_level))).convert_alpha()
        self.tilemap_floor = pygame.transform.scale(self.tilemap_floor, (MAZE_WIDTH, MAZE_HEIGHT))

        self.tilemap_bottom_wall = pygame.image.load(path.join(base_path["path_tilemap"], "level_{}//".format(self.num_level), 
        "tilemap_bottom_wall_level_{}.png".format(self.num_level))).convert_alpha()
        self.tilemap_bottom_wall = pygame.transform.scale(self.tilemap_bottom_wall, (MAZE_WIDTH, MAZE_HEIGHT))

        self.tilemap_upper_wall = pygame.image.load(path.join(base_path["path_tilemap"], "level_{}//".format(self.num_level), 
        "tilemap_upper_wall_level_{}.png".format(self.num_level))).convert_alpha()
        self.tilemap_upper_wall = pygame.transform.scale(self.tilemap_upper_wall, (MAZE_WIDTH, MAZE_HEIGHT))

        self.load_pass_blocker()

        self.load_gem()

    def load_pass_blocker(self):
        self.matrix_tilemap = import_csv_to_matrix(path.join(base_path["path_tilemap"], "level_"+self.num_level,
        "tilemap_level_"+self.num_level+".csv"))

        for x in range(len(self.matrix_tilemap)):
            for y in range(len(self.matrix_tilemap[0])):
                code_tileset_map = int(self.matrix_tilemap[x][y])
                if (code_tileset_map == -1 or (code_tileset_map >= -6 and code_tileset_map <= -5) or code_tileset_map == -11):
                    pix_pos = grid_2_pix_pos([y, x])
                    self.rect_pill.append(Rect(pix_pos[0], pix_pos[1], CELL_WIDTH, CELL_HEIGHT))
                if (code_tileset_map == -3):
                    pix_pos = grid_2_pix_pos([y, x])
                    self.rect_gem.append(Rect(pix_pos[0], pix_pos[1], CELL_WIDTH, CELL_HEIGHT))
                if ((code_tileset_map >= 11 and code_tileset_map < 70) or code_tileset_map >= 80):
                    self.coord_wall.append([y,x])
                if (code_tileset_map == -10):
                    self.coord_monster_house_gate.append([y,x])
                if (code_tileset_map == -11):
                    self.coord_path_monster_go_through_wall.append([y,x])
                if (code_tileset_map == -12):
                    self.coord_tunnel.append([y,x])
                if (code_tileset_map == -5):
                    self.knight_pos = [y, x]
                if (code_tileset_map >= -9 and code_tileset_map <= -6):
                    self.monster_pos.append([y,x])

    def load_gem(self):
        self.gem = pygame.image.load(path.join(base_path["path_gem"], "gem_{}.png".format(self.num_level))).convert_alpha()
        self.gem = pygame.transform.scale(self.gem, (16, 16))

    def choose_monster_type(self):
        if self.num_level == '1': monster_type = 'zombie'
        elif self.num_level == '2': monster_type = 'ogre'
        elif self.num_level == '3': monster_type = 'dark_knight'
        else: monster_type = 'hades'
        return monster_type

    def make_monster(self):
        for idx, pos in enumerate(self.monster_pos):
            self.monsters.append(Monster(self, pos, idx+1, self.monster_type))
            self.group_monster.add(self.monsters[idx])

    def draw_item(self):
        for pill in self.rect_pill:
            pygame.draw.circle(screen, GRAYISH_YELLOW, [pill.x + CELL_WIDTH//2, pill.y + CELL_HEIGHT//2], 3)

        for gem in self.rect_gem:
            # pygame.draw.circle(screen, GRAYISH_YELLOW, [gem.x + CELL_WIDTH//2, gem.y + CELL_HEIGHT//2], 5)
            screen.blit(self.gem, (gem.x, gem.y))

    def draw_health_point(self):
        for hp_point in range(self.knight.hp_point):
            # self.knight.knight_right_sprites[0]
            screen.blit(self.knight.knight_right_sprites[0], (INITIAL_POSITION_X_GAME + hp_point * CELL_WIDTH + 4 * CELL_WIDTH, INITIAL_POSITION_Y_GAME + MAZE_HEIGHT))

    def start_draw(self):
        screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50], SIZE_FONT, (170, 132, 58), PATH_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50], SIZE_FONT, (44, 167, 198), PATH_FONT, centered=True)
        self.draw_text('HIGH SCORE', screen, [4, 0], SIZE_FONT, (255, 255, 255), PATH_FONT)
        pygame.display.update()
        pass

    def start_update(self):
        pass

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_playing = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_playing = 0
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
        self.last_time = self.curr_time
        self.curr_time = pygame.time.get_ticks()

        self.group_knight.update()
        self.group_monster.update()

        print("Speed: {}".format(self.monsters[0].speed))

        for monster in self.monsters:
            '''if self.knight.grid_pos == monster.grid_pos:
                self.remove_life()'''
            if self.knight.rect.colliderect(monster.rect):
                self.remove_life()

    def remove_life(self):
        self.knight.hp_point -= 1
        if self.knight.hp_point == 0:
            if self.knight.curr_score > int(self.hi_score):
                self.write_hi_score()

            self.sound_obj.stop()
            self.state = "game_over"
        else:
            self.knight.grid_pos = self.knight.starting_pos
            self.knight.pix_pos = grid_2_pix_pos(self.knight.grid_pos)
            self.knight.direction *= 0
            for monster in self.monsters:
                monster.grid_pos = monster.starting_pos
                monster.pix_pos = grid_2_pix_pos(monster.grid_pos)
                monster.direction *= 0 
    
    def playing_draw(self):
        screen.fill(DARKGREY)
        
        screen.blit(self.tilemap_floor, (INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME))
        screen.blit(self.tilemap_bottom_wall, (INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME))

        self.draw_item()
        self.group_knight.draw(screen)
        self.group_monster.draw(screen)

        screen.blit(self.tilemap_upper_wall, (INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME))

        # self.draw_grid()

        self.draw_text('GAME SCORE: {}'.format(self.knight.curr_score), screen, [SCREEN_WIDTH//60+2, 0], SIZE_FONT, WHITE, PATH_FONT)
        self.draw_text('HI-SCORE: {}'.format(self.hi_score), screen, [SCREEN_WIDTH//2+30, 0], SIZE_FONT, WHITE, PATH_FONT)

        self.draw_text('LIFE: ', screen, [SCREEN_WIDTH//60 + 2, INITIAL_POSITION_Y_GAME + MAZE_HEIGHT + CELL_HEIGHT//2], SIZE_FONT, WHITE, PATH_FONT)
        self.draw_health_point()

        pygame.display.flip()

    def win_update(self):
        pass

    def win_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_SPACE:
                self.is_playing = 0

    def win_draw(self):
        screen.fill(BLACK)
        win_text = "Congratulations!!! You win phase the {}".format(self.level.main.step)
        quit_text = "Press space to QUIT"
        self.draw_text(win_text, screen, [SCREEN_WIDTH//2, 100],  52, RED, PATH_FONT, centered=True)
        # self.draw_text(again_text, screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2],  36, (190, 190, 190), PATH_FONT, centered=True)
        self.draw_text(quit_text, screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//1.5],  36, (190, 190, 190), PATH_FONT, centered=True)
        pygame.display.update()
  
    def win(self):
        if len(self.rect_pill) == 0:
            self.state = "win"
    
    def reset(self):
        self.knight.hp_point = 2
        self.knight.curr_score = 0
        self.knight.grid_pos = self.knight_pos
        self.knight.pix_pos = grid_2_pix_pos(self.knight.grid_pos)
        self.knight.direction *= 0
        for index_monster in range(len(self.monsters)):  
            self.monsters[index_monster].grid_pos = self.monsters[index_monster].starting_pos
            self.monsters[index_monster].pix_pos = grid_2_pix_pos(self.monsters[index_monster].grid_pos)
            self.monsters[index_monster].direction *= 0

        self.load()
        self.state = "playing"

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_playing = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_playing = 0

    def game_over_update(self):
        pass

    def import_hi_score(self):
        with open(".//score.txt", mode="r+") as file:
            self.hi_score = file.readline()

    def write_hi_score(self):
        with open(".//score.txt", mode="w+") as file:
            file.write(str(self.knight.curr_score))

    def game_over_draw(self):
        screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", screen, [SCREEN_WIDTH//2, 100],  52, RED, PATH_FONT, centered=True)
        self.draw_text(again_text, screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2],  36, (190, 190, 190), PATH_FONT, centered=True)
        self.draw_text(quit_text, screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//1.5],  36, (190, 190, 190), PATH_FONT, centered=True)
        pygame.display.update()
        
