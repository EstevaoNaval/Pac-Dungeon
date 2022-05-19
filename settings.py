from turtle import width
import pygame
from pygame.locals import *

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
DARKGREY = (40,40,40)

# Basic game constants
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 448,640 # 16px X 28 tiles, 16px X 36 tiles + 16 X 4 tiles para placar
INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME = 0, 32
TITLE = "Pac-Dungeon"
BG_COLOR = DARKGREY

# Tile grid
TILESIZE = 16
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH/TILESIZE, SCREEN_HEIGHT/TILESIZE

# KNIGHT
NUM_KNIGHT_HP = 2

# MONSTER