import pygame
from pygame.locals import *

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
DARKGREY = (40,40,40)
BG_COLOR = DARKGREY

# Tile grid
TILESIZE = 16
NUM_TILE_MAZE_X, NUM_TILE_MAZE_Y = 28, 36

# Basic game constants
FPS = 320
TOP_BOTTOM_BUFFER = 32
INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME = 0, 32
TITLE = "Pac-Dungeon"
GAME_STATE = "menu"

# Text
SIZE_FONT = 32
PATH_FONT = "./assets/font/ARCADEPI.TTF" 

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 448, 640 # 16px X 28 tiles, 16px X 36 tiles + 16 X 4 tiles para placar
MAZE_WIDTH, MAZE_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT - 64
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CELL_WIDTH, CELL_HEIGHT = MAZE_WIDTH // NUM_TILE_MAZE_X, MAZE_HEIGHT // NUM_TILE_MAZE_Y

# knight
NUM_KNIGHT_HP = 2

# monster