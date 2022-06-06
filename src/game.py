from logging import _Level
from platform import python_branch
import pygame
import settings
import knight
import tilemap
import support
import menu
from level import Level

class Game:
    def __init__(self):
        settings.GAME_STATE = "start"
    
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.is_running = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: self.state = 'playing'