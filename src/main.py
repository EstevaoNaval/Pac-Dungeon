from sys import exit
import pygame
from pygame.locals import *
from settings import *

pygame.init()

def draw(self):
    pass

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    background_image = pygame.image.load(r"./map/level_01/tilemap_level_01.png")
    
    running = 1
    while running:
        clock.tick(FPS)

        screen.fill(DARKGREY)
        screen.blit(background_image, (INITIAL_POSITION_X_GAME,INITIAL_POSITION_Y_GAME))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit()

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__': main()