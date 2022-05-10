import pygame
from pygame.locals import *
from settings import *

pygame.init()

def main():
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    running = 1
    while running:
        clock.tick(FPS)

        pygame.display.update()
    
    pygame.quit()

if __name__ == '__main__': main()